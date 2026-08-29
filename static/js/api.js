// Web Intern REST API Client Wrapper
const API = {
  getAuthToken() {
    return localStorage.getItem('access_token');
  },

  setAuthToken(token) {
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  },

  getCurrentUser() {
    const raw = localStorage.getItem('user_profile');
    try {
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  },

  setCurrentUser(user) {
    if (user) {
      localStorage.setItem('user_profile', JSON.stringify(user));
    } else {
      localStorage.removeItem('user_profile');
    }
  },

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    const token = this.getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      method: options.method || 'GET',
      headers,
      ...options
    };

    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(endpoint, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || data.message || 'Request failed');
      }
      return data;
    } catch (err) {
      console.error(`[API Error ${endpoint}]:`, err);
      throw err;
    }
  }
};
