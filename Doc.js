const fs = require('fs').promises;
const readline = require('readline');
const path = require('path');
const { LMStudioClient } = require("@lmstudio/sdk");
const cliProgress = require('cli-progress');

const client = new LMStudioClient();

// Create a new progress bar instance
const progressBar = new cliProgress.SingleBar({
    format: 'Processing Files [{bar}] {percentage}% | {value}/{total} Files',
    barCompleteChar: '\u2588',
    barIncompleteChar: '\u2591',
    hideCursor: true,
}, cliProgress.Presets.legacy);

// Function to split text into chunks of approximately 300 tokens
function splitIntoChunks(text, chunkSize = 300) {
    // Rough approximation: 1 token ≈ 4 characters for English text
    const charactersPerChunk = chunkSize * 4;
    
    // Split the text into lines first to avoid breaking in the middle of a line
    const lines = text.split('\n');
    const chunks = [];
    let currentChunk = '';
    
    for (const line of lines) {
        // If adding this line would exceed the chunk size, start a new chunk
        if (currentChunk.length + line.length > charactersPerChunk && currentChunk.length > 0) {
            chunks.push(currentChunk.trim());
            currentChunk = '';
        }
        currentChunk += line + '\n';
    }
    
    // Add the last chunk if it's not empty
    if (currentChunk.trim()) {
        chunks.push(currentChunk.trim());
    }
    
    return chunks;
}

async function generateDocumentationForChunk(chunk, importPath, chunkIndex, totalChunks) {
    const prompt = `Hi, can you help me with creating documentation of code today?
Here's my code (Part ${chunkIndex + 1}/${totalChunks}):
${chunk}

Give complete documentation for a module giving import using submodules.txt content and syntaxes containing parameters. 
Only use the functions that exist.
The import path for this file is: ${importPath}`;

    const llama = await client.llm.load("llama-3.2-3b-qnn");
    const { content } = await llama.respond([
        {role: "system", content: "Help the user by completing his tasks with high accuracy." },
        {role: "user",content: prompt}],
        {
            contextOverflowPolicy: "stopAtLimit",
            maxPredictedTokens: 200,
            stopStrings: ["\n"],
            temperature: 0.03,

          },
    );
    
    return content;
}

async function generateDocumentationForFile(fileName, moduleName, submodulePath, totalFiles, currentFileIndex) {
    try {
        const documentationBasePath = path.join(__dirname, "Documentation");
        const modulePath = path.join(documentationBasePath, moduleName);
        const documentFilePath = path.join(modulePath, "Document.md");

        // Get the import path by replacing directory separators with dots and removing .py extension
        const importPath = `${moduleName.toLowerCase()}.${submodulePath.replace(/\//g, '.').replace('.py', '')}`;

        // Convert the file path to look for .txt instead of .py
        const txtFilePath = path.join(modulePath, path.basename(fileName).replace('.py', '.txt'));

        console.log(`Processing file: ${fileName}`);
        console.log(`Looking for txt file at: ${txtFilePath}`);

        try {
            // Check if the file exists
            await fs.access(txtFilePath);
        } catch (err) {
            console.error(`File not found: ${txtFilePath}`);
            return;  // Skip if file doesn't exist
        }

        // Read the content of the corresponding .txt file
        const fileContent = await fs.readFile(txtFilePath, "utf-8");

        // Split the content into chunks
        const chunks = splitIntoChunks(fileContent);
        console.log(`File split into ${chunks.length} chunks`);

        // Add a section header using the submodule path
        const sectionHeader = `## ${submodulePath}\n\n`;
        await fs.appendFile(documentFilePath, sectionHeader);

        // Process each chunk and append to documentation
        for (let i = 0; i < chunks.length; i++) {
            console.log(`Processing chunk ${i + 1}/${chunks.length} for ${fileName}`);
            const content = await generateDocumentationForChunk(chunks[i], importPath, i, chunks.length);
            
            // Add a chunk indicator if there are multiple chunks
            const chunkHeader = chunks.length > 1 ? `### Part ${i + 1}/${chunks.length}\n\n` : '';
            await fs.appendFile(documentFilePath, `${chunkHeader}${content}\n\n`);
        }

        // Add a separator after the complete file documentation
        await fs.appendFile(documentFilePath, `---\n\n`);
        console.log(`Documentation generated for: ${fileName}`);
        
        // Update progress
        progressBar.update(currentFileIndex);

    } catch (error) {
        console.error(`Error processing ${fileName}:`, error.message);
    }
}

async function generateAllDocumentation() {
    try {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        // Get module name from user
        const moduleName = await new Promise((resolve) =>
            rl.question("Please enter the module name (e.g., GoTrade): ", resolve)
        );
        rl.close();

        const documentationBasePath = path.join(__dirname, "Documentation");
        const modulePath = path.join(documentationBasePath, moduleName);
        const submodulesFilePath = path.join(modulePath, "submodules.txt");

        // Ensure the module directory exists
        try {
            await fs.access(modulePath);
        } catch (err) {
            console.error(`Module directory not found: ${modulePath}`);
            return;
        }

        // Read and parse submodules.txt
        let submodules;
        try {
            submodules = await fs.readFile(submodulesFilePath, "utf-8");
        } catch (err) {
            console.error(`submodules.txt not found at: ${submodulesFilePath}`);
            return;
        }

        const submoduleFiles = submodules.split(/\r?\n/).filter(Boolean);

        // Initialize Document.md with header
        const documentFilePath = path.join(modulePath, "Document.md");
        const header = `# ${moduleName} Module Documentation\n\nGenerated on: ${new Date().toLocaleString()}\n\n`;
        await fs.writeFile(documentFilePath, header);

        console.log(`Starting documentation generation for ${submoduleFiles.length} files...`);
        
        // Initialize progress bar
        progressBar.start(submoduleFiles.length, 0);

        // Process each file
        for (let i = 0; i < submoduleFiles.length; i++) {
            const submodulePath = submoduleFiles[i];
            const fileName = path.basename(submodulePath);
            await generateDocumentationForFile(
                fileName,
                moduleName,
                submodulePath,
                submoduleFiles.length,
                i + 1
            );
        }

        progressBar.stop();
        console.log(`\nDocumentation generation completed!`);
        console.log(`Output file: ${documentFilePath}`);

    } catch (error) {
        console.error("An error occurred:", error.message);
        progressBar.stop();
    }
}

// Run the script
generateAllDocumentation();