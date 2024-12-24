import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import GithubAuth from "./components/GithubAuth";

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-7xl mx-auto">
          <header className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900">AutoDoc</h1>
            <p className="text-gray-600 mt-2">Your Automated Documentation Platform</p>
          </header>
          
          <main>
            <Routes>
              <Route 
                path="/" 
                element={
                  <div className="bg-white rounded-lg shadow-sm p-6">
                    <GithubAuth />
                  </div>
                } 
              />
              <Route path="/auth/callback" element={<GithubAuth />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;