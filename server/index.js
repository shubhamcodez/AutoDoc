const express = require('express');
const cors = require('cors');
const axios = require('axios');
const simpleGit = require('simple-git');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();

app.use(cors());
app.use(express.json());

const CLIENT_ID = 'Ov23liushxQmCUhgQGLM';
const CLIENT_SECRET = '26d6b9cfb5e3ff8f3fb890aa21d23308ed6433eb'; 
const CLONE_PATH = 'E:/Clones';

// Create Clones directory if it doesn't exist
if (!fs.existsSync(CLONE_PATH)) {
  fs.mkdirSync(CLONE_PATH, { recursive: true });
}

app.post('/auth/github/callback', async (req, res) => {
  const { code } = req.body;
  console.log('Received code:', code);

  try {
    console.log('Attempting to exchange code for token...');
    const tokenResponse = await axios.post(
      'https://github.com/login/oauth/access_token',
      {
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
        code,
      },
      {
        headers: {
          Accept: 'application/json',
        },
      }
    );

    console.log('Token response received:', tokenResponse.data);
    res.json(tokenResponse.data);
  } catch (error) {
    console.error('Error details:', error.response?.data || error.message);
    res.status(500).json({ error: 'Failed to exchange code for token' });
  }
});

app.post('/clone-repository', async (req, res) => {
  const { repository } = req.body;
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    // Create a directory for the repository if it doesn't exist
    const repoPath = path.join(CLONE_PATH, repository.split('/')[1]);
    
    // Remove existing directory if it exists
    if (fs.existsSync(repoPath)) {
      fs.rmSync(repoPath, { recursive: true, force: true });
    }

    // Initialize git with authentication
    const git = simpleGit();
    
    // Clone the repository
    const repoUrl = `https://${token}@github.com/${repository}.git`;
    console.log(`Cloning ${repository} to ${repoPath}...`);
    
    await git.clone(repoUrl, repoPath);
    console.log('Clone completed successfully');

    res.json({ 
      success: true, 
      repository,
      path: repoPath
    });
  } catch (error) {
    console.error('Error cloning repository:', error);
    res.status(500).json({ 
      error: 'Failed to clone repository',
      details: error.message 
    });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});