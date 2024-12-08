import { promises as fs } from 'fs';
import { createInterface } from 'readline';
import { dirname, join } from 'path';
import { LMStudioClient } from "@lmstudio/sdk";
import cliProgress from 'cli-progress';

// Create progress bar
const progressBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);

class AutoDoc {
    constructor() {
        this.client = new LMStudioClient();
        this.rl = createInterface({ 
            input: process.stdin, 
            output: process.stdout 
        });
        this.files = [];
        this.documentHandles = [];
        this.nomic = null;
        this.llama = null;
    }

    async initialize() {
        try {
            console.log("################ AutoDoc ################");
            console.log("Initializing models...");
            
            // Initialize models in parallel
            [this.nomic, this.llama] = await Promise.all([
                this.client.embedding.getOrLoad("text-embedding-nomic-embed-text-v1.5"),
                this.client.llm.getOrLoad("qwen2.5-coder-7b-instruct")
            ]);

            console.log("Models initialized successfully!");
        } catch (error) {
            console.error("Error initializing models:", error);
            throw error;
        }
    }

    async getModuleInput() {
        return new Promise((resolve) => {
            this.rl.question("Please enter the modules you'd like the documentation for: ", (answer) => {
                resolve(answer.trim());
            });
        });
    }

    async processDocuments(documentPath) {
        try {
            // Read all files in the directory
            this.files = await fs.readdir(documentPath);
            
            // Filter for both .md and .txt files
            const docFiles = this.files.filter(file => file.endsWith('.md') || file.endsWith('.txt'));
            
            if (docFiles.length === 0) {
                throw new Error('No documentation files (.md or .txt) found in the specified directory');
            }

            console.log(`Processing ${docFiles.length} documentation files...`);
            progressBar.start(docFiles.length, 0);

            // Process each file
            for (const filename of docFiles) {
                const fullPath = join(documentPath, filename);
                const fileContent = await fs.readFile(fullPath);
                
                const documentHandle = await this.client.files.uploadTempFile(
                    filename,
                    fileContent
                );
                
                this.documentHandles.push(documentHandle);
                progressBar.increment();
            }

            progressBar.stop();
            console.log("All files processed successfully!");
            
        } catch (error) {
            progressBar.stop();
            console.error('Error processing files:', error);
            throw error;
        }
    }

    async askQuestion() {
        return new Promise((resolve) => {
            this.rl.question("Please ask a question about the module: ", (answer) => {
                resolve(answer.trim());
            });
        });
    }

    async retrieveAndRespond(question) {
        try {
            console.log("\nRetrieving relevant documentation...");
            
            const results = await this.client.retrieval.retrieve(
                `Get documentation about ${question}`, 
                this.documentHandles, 
                { embeddingModel: this.nomic }
            );

            if (!results.entries.length) {
                throw new Error('No relevant documentation found');
            }

            const prompt = `\
Answer the user's query with the following citation:
----- Citation -----
${results.entries[0].content}
----- End of Citation -----
User's question is ${question}`;

            console.log("\nGenerating response...");
            
            const prediction = this.llama.respond([
                {
                    role: "user",
                    content: prompt,
                }],
                {
                    contextOverflowPolicy: "stopAtLimit",
                    maxPredictedTokens: 500,
                    stopStrings: ["\n"],
                    temperature: 0.4,
                }
            );

            console.log("\nAnswer:");
            for await (const { content } of prediction) {
                process.stdout.write(content);
            }
            console.log("\n"); // Add newline after response

        } catch (error) {
            console.error('Error during retrieval and response:', error);
            throw error;
        }
    }

    async cleanup() {
        try {
            // Cleanup logic here (e.g., closing connections, removing temp files)
            this.rl.close();
            // Add any additional cleanup needed for LMStudio client
        } catch (error) {
            console.error('Error during cleanup:', error);
        }
    }

    async run() {
        try {
            await this.initialize();
            
            const module = await this.getModuleInput();
            const documentPath = `Documentation/${module}`;
            
            await this.processDocuments(documentPath);
            
            let continueAsking = true;
            while (continueAsking) {
                const question = await this.askQuestion();
                
                if (question.toLowerCase() === 'exit') {
                    continueAsking = false;
                    continue;
                }

                try {
                    await this.retrieveAndRespond(question);
                    
                    // Add error handling for the continue prompt
                    const continueResponse = await new Promise((resolve) => {
                        this.rl.question("\nWould you like to ask another question? (yes/no): ", (answer) => {
                            resolve(answer.trim().toLowerCase());
                        });
                    });

                    // Check if the response is specifically 'yes', otherwise exit
                    if (continueResponse !== 'yes') {
                        console.log("Exiting...");
                        continueAsking = false;
                    } else {
                        console.log("\nPlease ask your next question...");
                    }
                } catch (error) {
                    console.error('Error processing question:', error);
                    // Ask if they want to continue even if there was an error
                    const continueAfterError = await new Promise((resolve) => {
                        this.rl.question("\nWould you like to try another question? (yes/no): ", (answer) => {
                            resolve(answer.trim().toLowerCase());
                        });
                    });
                    if (continueAfterError !== 'yes') {
                        console.log("Exiting...");
                        continueAsking = false;
                    }
                }
            }

        } catch (error) {
            console.error('Error in main process:', error);
        } finally {
            await this.cleanup();
        }
    }
}

// Run the application
const autoDoc = new AutoDoc();
autoDoc.run().catch(console.error);