// API Configuration
const API_BASE_URL = window.CONFIG?.API_BASE_URL || 'http://127.0.0.1:8000/api';

class APIClient {
    constructor() {
        this.token = localStorage.getItem(window.CONFIG?.STORAGE_KEYS?.ACCESS_TOKEN || 'access_token');
        this.baseURL = API_BASE_URL;
    }

    // Get headers with authentication
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (includeAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // Handle API responses
    async handleResponse(response) {
        if (response.status === 401) {
            // Token expired, try to refresh
            const refreshed = await this.refreshToken();
            if (!refreshed) {
                this.logout();
                if (window.location.pathname !== '/login.html') {
                    window.location.href = 'login.html';
                }
                return null;
            }
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            throw new Error(error.detail || error.message || 'An error occurred');
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        }
        
        return response.text();
    }

    // Authentication methods
    async login(username, password) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.LOGIN || '/token/'}`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ username, password })
            });

            const data = await this.handleResponse(response);
            if (data) {
                const accessKey = window.CONFIG?.STORAGE_KEYS?.ACCESS_TOKEN || 'access_token';
                const refreshKey = window.CONFIG?.STORAGE_KEYS?.REFRESH_TOKEN || 'refresh_token';
                
                localStorage.setItem(accessKey, data.access);
                localStorage.setItem(refreshKey, data.refresh);
                this.token = data.access;
                return data;
            }
        } catch (error) {
            throw error;
        }
    }

    async register(userData) {
        try {
            const formData = new FormData();
            Object.keys(userData).forEach(key => {
                if (userData[key] !== null && userData[key] !== undefined && userData[key] !== '') {
                    formData.append(key, userData[key]);
                }
            });

            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.REGISTER || '/register/'}`, {
                method: 'POST',
                body: formData
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async refreshToken() {
        try {
            const refreshKey = window.CONFIG?.STORAGE_KEYS?.REFRESH_TOKEN || 'refresh_token';
            const refreshToken = localStorage.getItem(refreshKey);
            if (!refreshToken) return false;

            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.REFRESH_TOKEN || '/token/refresh/'}`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                const accessKey = window.CONFIG?.STORAGE_KEYS?.ACCESS_TOKEN || 'access_token';
                localStorage.setItem(accessKey, data.access);
                this.token = data.access;
                return true;
            }
            return false;
        } catch (error) {
            console.error('Token refresh failed:', error);
            return false;
        }
    }

    logout() {
        const accessKey = window.CONFIG?.STORAGE_KEYS?.ACCESS_TOKEN || 'access_token';
        const refreshKey = window.CONFIG?.STORAGE_KEYS?.REFRESH_TOKEN || 'refresh_token';
        const userKey = window.CONFIG?.STORAGE_KEYS?.USER_DATA || 'user_data';
        
        localStorage.removeItem(accessKey);
        localStorage.removeItem(refreshKey);
        localStorage.removeItem(userKey);
        this.token = null;
    }

    isAuthenticated() {
        return !!this.token;
    }

    // Blog methods
    async getBlogs(search = '', page = 1) {
        try {
            let url = `${this.baseURL}${window.CONFIG?.ENDPOINTS?.BLOGS || '/blogs/'}?page=${page}`;
            if (search) {
                url += `&search=${encodeURIComponent(search)}`;
            }

            const response = await fetch(url, {
                headers: this.getHeaders()
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async getBlog(id) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.BLOGS || '/blogs/'}${id}/`, {
                headers: this.getHeaders()
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async createBlog(blogData) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.BLOGS || '/blogs/'}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(blogData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async updateBlog(id, blogData) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.BLOGS || '/blogs/'}${id}/`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(blogData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async deleteBlog(id) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.BLOGS || '/blogs/'}${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders()
            });

            if (response.status === 204) {
                return true;
            }
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    // Comment methods
    async getComments(blogId = null, page = 1) {
        try {
            let url = `${this.baseURL}${window.CONFIG?.ENDPOINTS?.COMMENTS || '/comments/'}?page=${page}`;
            if (blogId) {
                url += `&blog=${blogId}`;
            }

            const response = await fetch(url, {
                headers: this.getHeaders()
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async createComment(commentData) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.COMMENTS || '/comments/'}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(commentData)
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async deleteComment(id) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.COMMENTS || '/comments/'}${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders()
            });

            if (response.status === 204) {
                return true;
            }
            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    // Follow methods
    async followUser(userId) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.FOLLOW || '/followpage'}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({ following: userId })
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async unfollowUser(userId) {
        try {
            const response = await fetch(`${this.baseURL}${window.CONFIG?.ENDPOINTS?.UNFOLLOW || '/unfollowpage'}`, {
                method: 'DELETE',
                headers: this.getHeaders(),
                body: JSON.stringify({ user_id: userId })
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }
}

// Create global API client instance
const api = new APIClient();