// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';

class APIClient {
    constructor() {
        this.token = localStorage.getItem('access_token');
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
                window.location.href = 'login.html';
                return null;
            }
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            throw new Error(error.detail || error.message || 'An error occurred');
        }

        return response.json();
    }

    // Authentication methods
    async login(username, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/token/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ username, password })
            });

            const data = await this.handleResponse(response);
            if (data) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
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
                if (userData[key] !== null && userData[key] !== undefined) {
                    formData.append(key, userData[key]);
                }
            });

            const response = await fetch(`${API_BASE_URL}/register/`, {
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
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) return false;

            const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
                method: 'POST',
                headers: this.getHeaders(false),
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access);
                this.token = data.access;
                return true;
            }
            return false;
        } catch (error) {
            return false;
        }
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        this.token = null;
    }

    isAuthenticated() {
        return !!this.token;
    }

    // Blog methods
    async getBlogs(search = '', page = 1) {
        try {
            let url = `${API_BASE_URL}/blogs/?page=${page}`;
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
            const response = await fetch(`${API_BASE_URL}/blogs/${id}/`, {
                headers: this.getHeaders()
            });

            return await this.handleResponse(response);
        } catch (error) {
            throw error;
        }
    }

    async createBlog(blogData) {
        try {
            const response = await fetch(`${API_BASE_URL}/blogs/`, {
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
            const response = await fetch(`${API_BASE_URL}/blogs/${id}/`, {
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
            const response = await fetch(`${API_BASE_URL}/blogs/${id}/`, {
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
            let url = `${API_BASE_URL}/comments/?page=${page}`;
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
            const response = await fetch(`${API_BASE_URL}/comments/`, {
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
            const response = await fetch(`${API_BASE_URL}/comments/${id}/`, {
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
            const response = await fetch(`${API_BASE_URL}/followpage`, {
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
            const response = await fetch(`${API_BASE_URL}/unfollowpage`, {
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