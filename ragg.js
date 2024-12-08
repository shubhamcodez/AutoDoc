// rag.js
import { LMStudioClient } from "@lmstudio/sdk";
import { promises as fs } from 'fs';
import { dirname, join } from 'path';

export class AutoDoc {
    constructor() {
        this.client = new LMStudioClient();
        this.files = [];
        this.documentHandles = [];
        this.nomic = null;
        this.llama = null;
    }

    async initialize() {
        try {
            console.log("Initializing models...");
            
            // Initialize models in parallel
            [this.nomic, this.llama] = await Promise.all([
                this.client.embedding.getOrLoad("text-embedding-nomic-embed-text-v1.5"),
                this.client.llm.getOrLoad("llama-3.2-3b-qnn")
            ]);

            console.log("Models initialized successfully!");
            return true;
        } catch (error) {
            console.error("Error initializing models:", error);
            throw error;
        }
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

            // Process each file
            for (const filename of docFiles) {
                const fullPath = join(documentPath, filename);
                const fileContent = await fs.readFile(fullPath);
                
                const documentHandle = await this.client.files.uploadTempFile(
                    filename,
                    fileContent
                );
                
                this.documentHandles.push(documentHandle);
            }

            console.log("All files processed successfully!");
            return true;
            
        } catch (error) {
            console.error('Error processing files:', error);
            throw error;
        }
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
            
            let fullResponse = '';
            const prediction = this.llama.respond([
                {
                    role: "user",
                    content: prompt,
                }],
                {
                    contextOverflowPolicy: "stopAtLimit",
                    maxPredictedTokens: 500,
                    stopStrings: ["\n"],
                    temperature: 0.3,
                }
            );

            for await (const { content } of prediction) {
                fullResponse += content;
            }
            
            return fullResponse;

        } catch (error) {
            console.error('Error during retrieval and response:', error);
            throw error;
        }
    }

    async cleanup() {
        try {
            // Add any cleanup logic for LMStudio client
            this.documentHandles = [];
            this.files = [];
        } catch (error) {
            console.error('Error during cleanup:', error);
            throw error;
        }
    }
}