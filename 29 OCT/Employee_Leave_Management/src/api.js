
const API_BASE_URL = "http://127.0.0.1:8000";

export async function apiFetch(endpoint, options = {}) {

    // Retrieve JWT token from sessionStorage
    const token = sessionStorage.getItem("access_token");

    // Prepare request headers
    const headers = {
        ...options.headers,
    };

    // Add JWT authentication header
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    // Send request to FastAPI
    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,
            headers,
        }
    );

    // Handle authentication failure
    if (response.status === 401) {
        sessionStorage.removeItem("access_token");
        sessionStorage.removeItem("user");

        window.location.href = "/login";

        throw new Error("Session expired. Please log in again.");
    }

    return response;
}
