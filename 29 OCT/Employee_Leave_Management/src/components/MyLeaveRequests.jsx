
import { useEffect, useState } from "react";
import { apiFetch } from "../api";

function MyLeaveRequests() {
  const [leaveRequests, setLeaveRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchLeaveRequests() {
      try {
        const response = await apiFetch("/leave-requests");

        if (!response.ok) {
          throw new Error("Failed to fetch leave requests");
        }

        const data = await response.json();
        setLeaveRequests(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchLeaveRequests();
  }, []);

  if (loading) {
    return <p>Loading leave requests...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <section className="requests-container">
      <h2>My Leave Requests</h2>
      <p>View your submitted leave applications below.</p>

      <div className="table-wrapper">
        <table className="leave-table">
          <thead>
            <tr>
              <th>Leave Type</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Reason</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {leaveRequests.length === 0 ? (
              <tr>
                <td colSpan="5">No leave requests found.</td>
              </tr>
            ) : (
              leaveRequests.map((request) => (
                <tr key={request.id}>
                  <td>{request.leave_type}</td>
                  <td>{request.start_date}</td>
                  <td>{request.end_date}</td>
                  <td>{request.reason}</td>
                  <td>
                    <span
                      className={`status ${request.status.toLowerCase()}`}
                    >
                      {request.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default MyLeaveRequests;
