
import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {

    // Restore login information if the page is refreshed
    const [token, setToken] = useState(
        sessionStorage.getItem("access_token")
    );

    const [user, setUser] = useState(() => {
        const savedUser = sessionStorage.getItem("user");

        return savedUser ? JSON.parse(savedUser) : null;
    });


    // Login function
    const login = async (username, password) => {

        const response = await fetch(
            "http://127.0.0.1:8000/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Login failed");
        }

        // Save token and user information
        sessionStorage.setItem(
            "access_token",
            data.access_token
        );

        sessionStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );

        setToken(data.access_token);
        setUser(data.user);

        return data.user;
    };


    // Logout function
    const logout = () => {

        sessionStorage.removeItem("access_token");
        sessionStorage.removeItem("user");

        setToken(null);
        setUser(null);
    };


    return (
        <AuthContext.Provider
            value={{
                token,
                user,
                login,
                logout,
                isAuthenticated: Boolean(token && user)
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}


// Custom hook to access authentication information
export function useAuth() {
    return useContext(AuthContext);
}
