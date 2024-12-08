// server.js
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { AutoDoc } from './ragg.js';
import cors from 'cors';

const app = express();
app.use(cors());

const server = createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*",  // Be more specific in production
        methods: ["GET", "POST"]
    }
});

// Store AutoDoc instances for different clients
const clientSessions = new Map();

io.on('connection', (socket) => {
    console.log('Client connected:', socket.id);
    
    socket.on('initializeModule', async ({ module }) => {
        try {
            console.log(`Initializing module ${module} for client ${socket.id}`);
            
            // Create new AutoDoc instance for this client
            const autoDoc = new AutoDoc();
            await autoDoc.initialize();
            
            // Store the instance
            clientSessions.set(socket.id, {
                autoDoc,
                module
            });
            
            // Process documents for the specified module
            await autoDoc.processDocuments(`Documentation/${module}`);
            
            socket.emit('initializationComplete');
            
        } catch (error) {
            console.error('Initialization error:', error);
            socket.emit('error', { 
                message: `Failed to initialize documentation system: ${error.message}` 
            });
        }
    });

    socket.on('askQuestion', async ({ module, question }) => {
        try {
            console.log(`Processing question for module ${module} from client ${socket.id}`);
            
            const session = clientSessions.get(socket.id);
            if (!session || !session.autoDoc) {
                throw new Error('Session not initialized');
            }

            // Signal the start of streaming
            socket.emit('streamStart');

            // Retrieve relevant documentation
            const results = await session.autoDoc.client.retrieval.retrieve(
                `Get documentation about ${question}`, 
                session.autoDoc.documentHandles, 
                { embeddingModel: session.autoDoc.nomic }
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

            // Stream the response using llama model
            const prediction = session.autoDoc.llama.respond([
                {
                    role: "user",
                    content: prompt,
                }],
                {
                    contextOverflowPolicy: "stopAtLimit",
                    maxPredictedTokens: 500,
                    temperature: 0.3,
                }
            );

            // Stream each chunk to the client
            for await (const { content } of prediction) {
                socket.emit('streamChunk', { content });
            }

            // Signal the end of streaming
            socket.emit('streamEnd');
            
        } catch (error) {
            console.error('Question processing error:', error);
            socket.emit('error', { 
                message: `Failed to process question: ${error.message}` 
            });
        }
    });

    socket.on('disconnect', async () => {
        // Clean up AutoDoc instance when client disconnects
        const session = clientSessions.get(socket.id);
        if (session && session.autoDoc) {
            await session.autoDoc.cleanup();
            clientSessions.delete(socket.id);
        }
        console.log('Client disconnected:', socket.id);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});