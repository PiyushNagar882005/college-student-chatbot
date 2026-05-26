// ==========================================
// Backend URL Configuration
// ==========================================
// This file dynamically determines the backend URL
// Works both in development (localhost) and production (Render)

const getBackendURL = () => {
    // In development (localhost)
    if (window.location.hostname === 'localhost' || 
        window.location.hostname === '127.0.0.1' ||
        window.location.hostname.includes('localhost:')) {
        return 'http://localhost:5000';
    }
    
    // In production (Render or other hosting)
    // Use the same origin as frontend (no hardcoded backend URL)
    return window.location.origin;
};

// Export for use in other files
const BACKEND_URL = getBackendURL();

console.log('Backend URL:', BACKEND_URL);
