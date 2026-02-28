import React, { useState, useEffect } from 'react';
import api from '@/api/api';

export default function TestAPI() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const testAPI = async () => {
      try {
        console.log('Testing API call...');
        console.log('Token:', localStorage.getItem('token'));
        
        // Test basic auth
        const meResponse = await api.get('/auth/me');
        console.log('Auth /me response:', meResponse.data);
        
        // Test company profile
        const profileResponse = await api.get('/api/company/profile');
        console.log('Company profile response:', profileResponse.data);
        setData(profileResponse.data);
        
      } catch (err) {
        console.error('API Test Error:', err);
        console.error('Error response:', err.response);
        setError(err.response?.data?.detail || err.message);
      } finally {
        setLoading(false);
      }
    };

    testAPI();
  }, []);

  if (loading) return <div className="p-4">Testing API...</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">API Test</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {data && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          <h2 className="font-bold mb-2">Success! Company Data:</h2>
          <pre className="text-sm overflow-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
