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

// Function to recursively get all files from a directory
function getAllFiles(dirPath) {
  const files = fs.readdirSync(dirPath);
  let fileList = [];

  files.forEach(file => {
    if (file === 'node_modules' || file === '.git' || file === 'AutoData') {
      return; // Skip these directories
    }
    const fullPath = path.join(dirPath, file);
    if (fs.statSync(fullPath).isDirectory()) {
      fileList = fileList.concat(getAllFiles(fullPath));
    } else {
      fileList.push(fullPath);
    }
  });
  return fileList;
}

// Function to generate file paths list
function generateFilePathsList(repoPath, files) {
  const repoName = path.basename(repoPath);
  const paths = files.map(filePath => {
    const relativePath = path.relative(repoPath, filePath);
    // Convert Windows path separators to forward slashes
    return `${repoName}/${relativePath.replace(/\\/g, '/')}`;
  });
  return paths.join('\n');
}

// Function to convert files to text
function convertToText(repoPath) {
  try {
    // Create AutoData directory
    const autoDataPath = path.join(repoPath, 'AutoData');
    if (!fs.existsSync(autoDataPath)) {
      fs.mkdirSync(autoDataPath, { recursive: true });
    }

    // Get all files
    const files = getAllFiles(repoPath);

    // Create file_paths.txt
    const filePathsList = generateFilePathsList(repoPath, files);
    fs.writeFileSync(path.join(autoDataPath, 'file_paths.txt'), filePathsList);

    // Process each file
    files.forEach(filePath => {
      try {
        // Skip binary files
        const ext = path.extname(filePath).toLowerCase();
        const skipExtensions = ['.jpg', '.png', '.gif', '.pdf', '.zip', '.exe', '.jar'];
        
        // Get relative path and create flat file name
        const relativePath = path.relative(repoPath, filePath);
        const flatFileName = relativePath.replace(/\\/g, '_').replace(/\//g, '_');
        const outputFile = path.join(autoDataPath, flatFileName + '.txt');

        if (skipExtensions.includes(ext)) {
          fs.writeFileSync(outputFile, `[Binary file: ${ext}]`);
        } else {
          // Read and write text content
          const content = fs.readFileSync(filePath, 'utf-8');
          // Add original file path as a comment at the top of the file
          const contentWithPath = `// Original path: ${relativePath.replace(/\\/g, '/')}\n\n${content}`;
          fs.writeFileSync(outputFile, contentWithPath);
        }
      } catch (err) {
        console.error(`Error processing file ${filePath}:`, err);
      }
    });

    return true;
  } catch (error) {
    console.error('Error in convertToText:', error);
    return false;
  }
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

    // Convert repository files to text and create file_paths.txt
    console.log('Converting files to text and generating paths...');
    const conversionSuccess = convertToText(repoPath);
    console.log('Conversion completed:', conversionSuccess ? 'success' : 'failed');

    res.json({ 
      success: true, 
      repository,
      path: repoPath,
      textConversion: conversionSuccess
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