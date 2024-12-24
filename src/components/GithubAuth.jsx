import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Github } from 'lucide-react';

const GithubAuth = () => {
  const [repositories, setRepositories] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [cloneStatus, setCloneStatus] = useState({});
  const navigate = useNavigate();

  const CLIENT_ID = 'Ov23liushxQmCUhgQGLM';
  const REDIRECT_URI = 'http://localhost:5173/auth/callback';
  
  const handleLogin = () => {
    const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=repo,user`;
    window.location.href = githubAuthUrl;
  };

  const handleCallback = async (code) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('http://localhost:3000/auth/github/callback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });
      
      if (!response.ok) {
        throw new Error('Authentication failed');
      }

      const data = await response.json();
      
      if (data.access_token) {
        localStorage.setItem('github_token', data.access_token);
        setIsAuthenticated(true);
        await fetchRepositories(data.access_token);
        navigate('/');
      }
    } catch (error) {
      setError(error.message);
      console.error('Authentication error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchRepositories = async (token) => {
    try {
      setLoading(true);
      const response = await fetch('https://api.github.com/user/repos', {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: 'application/vnd.github.v3+json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch repositories');
      }

      const repos = await response.json();
      setRepositories(repos.filter(repo => !repo.fork));
    } catch (error) {
      setError(error.message);
      console.error('Error fetching repositories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCloneRepository = async (repoName) => {
    try {
      setCloneStatus(prev => ({ ...prev, [repoName]: 'cloning' }));
      setError(null);
      
      const response = await fetch('http://localhost:3000/clone-repository', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('github_token')}`,
        },
        body: JSON.stringify({ repository: repoName }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to clone repository');
      }

      const data = await response.json();
      if (data.success) {
        setCloneStatus(prev => ({ ...prev, [repoName]: 'success' }));
        console.log('Repository cloned successfully to:', data.path);
      }
    } catch (error) {
      setCloneStatus(prev => ({ ...prev, [repoName]: 'error' }));
      setError(error.message);
      console.error('Error cloning repository:', error);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('github_token');
    if (token) {
      setIsAuthenticated(true);
      fetchRepositories(token);
    }

    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    if (code) {
      handleCallback(code);
    }
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  const getCloneButtonStyle = (repoName) => {
    switch (cloneStatus[repoName]) {
      case 'cloning':
        return 'bg-yellow-500 hover:bg-yellow-600';
      case 'success':
        return 'bg-green-500 hover:bg-green-600';
      case 'error':
        return 'bg-red-500 hover:bg-red-600';
      default:
        return 'bg-blue-600 hover:bg-blue-700';
    }
  };

  const getCloneButtonText = (repoName) => {
    switch (cloneStatus[repoName]) {
      case 'cloning':
        return 'Cloning...';
      case 'success':
        return 'Cloned';
      case 'error':
        return 'Failed';
      default:
        return 'Clone';
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-600 rounded-md">
          {error}
        </div>
      )}

      {!isAuthenticated ? (
        <div className="text-center">
          <button
            onClick={handleLogin}
            className="inline-flex items-center px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-800 transition-colors"
          >
            <Github className="mr-2 h-5 w-5" />
            Connect with GitHub
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-900">Your Repositories</h2>
            <button
              onClick={() => {
                localStorage.removeItem('github_token');
                setIsAuthenticated(false);
                setRepositories([]);
                setCloneStatus({});
              }}
              className="px-4 py-2 text-sm text-red-600 hover:text-red-700"
            >
              Logout
            </button>
          </div>

          <div className="grid gap-4">
            {repositories.map((repo) => (
              <div
                key={repo.id}
                className="p-4 border rounded-lg bg-white shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {repo.name}
                      {repo.private && (
                        <span className="ml-2 px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
                          Private
                        </span>
                      )}
                    </h3>
                    <p className="text-sm text-gray-500">{repo.description || 'No description provided'}</p>
                    <div className="mt-1 text-xs text-gray-400">
                      Last updated: {new Date(repo.updated_at).toLocaleDateString()}
                    </div>
                  </div>
                  <button
                    onClick={() => handleCloneRepository(repo.full_name)}
                    disabled={cloneStatus[repo.full_name] === 'cloning'}
                    className={`px-3 py-1 text-white rounded transition-colors ${getCloneButtonStyle(repo.full_name)}`}
                  >
                    {getCloneButtonText(repo.full_name)}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default GithubAuth;