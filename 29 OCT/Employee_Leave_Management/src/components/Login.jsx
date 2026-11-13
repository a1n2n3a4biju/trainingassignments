
import { useState } from "react";
import { useAuth } from "../AuthContext";
import { useNavigate } from "react-router-dom";

function Login() {

    const { login } = useAuth();
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    const handleLogin = async (e) => {

        e.preventDefault();

        setError("");
        setLoading(true);

        try {

            // Call the login function from AuthContext
            const loggedInUser = await login(username, password);

            console.log("Login successful:", loggedInUser);

            // Navigate based on user role
            if (loggedInUser.role === "EMPLOYEE") {
                navigate("/");
            }
            else if (loggedInUser.role === "MANAGER") {
                navigate("/manager-dashboard");
            }
            else if (loggedInUser.role === "HR_ADMIN") {
                navigate("/");
            }

        } catch (err) {

            setError(err.message);

        } finally {

            setLoading(false);

        }
    };


    return (

        <div className="login-container">

            <div className="login-card">

                <h2>Employee Leave Management</h2>

                <p>Please sign in to continue</p>

                <form onSubmit={handleLogin}>

                    <div className="form-group">

                        <label>Username</label>

                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                        />

                    </div>


                    <div className="form-group">

                        <label>Password</label>

                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                        />

                    </div>


                    {error && (
                        <p className="login-error">{error}</p>
                    )}


                    <button type="submit" disabled={loading}>

                        {loading ? "Signing in..." : "Login"}

                    </button>

                </form>

            </div>

        </div>

    );
}

export default Login;
