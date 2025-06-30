// Configuration for the frontend application
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://127.0.0.1:8000/api' 
        : '/api',
    
    // Environment detection
    isDevelopment: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
    
    // API endpoints
    ENDPOINTS: {
        LOGIN: '/token/',
        REGISTER: '/register/',
        REFRESH_TOKEN: '/token/refresh/',
        BLOGS: '/blogs/',
        COMMENTS: '/comments/',
        FOLLOW: '/followpage',
        UNFOLLOW: '/unfollowpage'
    },
    
    // Pagination
    PAGE_SIZE: 10,
    
    // Local storage keys
    STORAGE_KEYS: {
        ACCESS_TOKEN: 'access_token',
        REFRESH_TOKEN: 'refresh_token',
        USER_DATA: 'user_data'
    }
};

// Export for use in other files
window.CONFIG = CONFIG;