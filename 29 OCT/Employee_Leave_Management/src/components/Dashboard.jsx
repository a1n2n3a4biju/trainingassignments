
function Dashboard() {
  return (
    <>
      <section className="welcome">
        <h2>Welcome to LeaveFlow</h2>
        <p>
          Manage your leave applications, check your leave balance,
          and track your requests in one place.
        </p>
      </section>

      <section className="dashboard">
        <div className="dashboard-card">
          <h3>Available Leave</h3>
          <p className="number">12 Days</p>
        </div>

        <div className="dashboard-card">
          <h3>Pending Requests</h3>
          <p className="number">2</p>
        </div>

        <div className="dashboard-card">
          <h3>Approved Requests</h3>
          <p className="number">5</p>
        </div>
      </section>

      <section className="actions">
        <h2>Quick Actions</h2>
        <button>Apply for Leave</button>
        <button>My Leave Requests</button>
      </section>
    </>
  );
}

export default Dashboard;
