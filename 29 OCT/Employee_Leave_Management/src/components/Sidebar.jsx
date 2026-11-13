
import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <h3>Menu</h3>

      <nav className="sidebar-nav">
        <NavLink to="/" end>
          Dashboard
        </NavLink>

        <NavLink to="/apply-leave">
          Apply Leave
        </NavLink>

        <NavLink to="/my-requests">
          My Leave Requests
        </NavLink>
        <NavLink to="/leave-summary">
            Leave Summary
            </NavLink>
            <NavLink to="/leave-history">
            Leave History
            </NavLink>
            <NavLink to="/manager-dashboard">
    Manager Dashboard
</NavLink>
      </nav>

    </aside>
  );
}

export default Sidebar;
