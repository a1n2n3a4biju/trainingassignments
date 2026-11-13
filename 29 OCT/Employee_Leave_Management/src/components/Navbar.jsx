
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";

function Navbar() {

  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="navbar">

      <div className="navbar-brand">
        <Link to="/">LeaveFlow</Link>
      </div>

      <nav className="navbar-links">
        <Link to="/">Dashboard</Link>
        <Link to="/apply-leave">Apply Leave</Link>
        <Link to="/my-requests">My Requests</Link>

        {user?.role === "MANAGER" && (
          <Link to="/manager-dashboard">Manager Dashboard</Link>
        )}

        {user?.role === "HR_ADMIN" && (
          <Link to="/manager-dashboard">Manager Dashboard</Link>
        )}
      </nav>

      <div className="navbar-user">

        {user && (
          <>
            <span>
              Welcome, {user.username}
            </span>

            <span>
              ({user.role})
            </span>

            <button onClick={handleLogout}>
              Logout
            </button>
          </>
        )}

      </div>

    </header>
  );
}

export default Navbar;
