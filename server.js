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

            // Use the retrieveAndRespond method from your RAG system
            const response = await session.autoDoc.retrieveAndRespond(question);
            
            socket.emit('ragResponse', { content: response });
            
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