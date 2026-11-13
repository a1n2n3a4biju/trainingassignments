
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

function ProtectedRoute({ children, allowedRoles }) {

    const { isAuthenticated, user } = useAuth();

    // Check whether the user is logged in
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    // Check whether the user's role is allowed
    if (
        allowedRoles &&
        !allowedRoles.includes(user.role)
    ) {
        return <Navigate to="/unauthorized" replace />;
    }

    // Allow access to the requested page
    return children;
}

export default ProtectedRoute;
