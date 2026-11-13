
import { useEffect, useState } from "react";
import { apiFetch } from "../api";

function ManagerDashboard() {
    const [leaveRequests, setLeaveRequests] = useState([]);
    const [comments, setComments] = useState({});
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState("");

    // Fetch leave requests
    async function fetchLeaveRequests() {
        try {
            const response = await apiFetch("/leave-requests");

            if (!response.ok) {
                throw new Error("Failed to fetch leave requests");
            }

            const data = await response.json();
            setLeaveRequests(data);

        } catch (error) {
            setMessage(error.message);

        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchLeaveRequests();
    }, []);

    // Approve or reject a leave request
    async function handleDecision(requestId, decision) {
        try {
            const response = await apiFetch(
                `/leave-requests/${requestId}/decision`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        decision: decision,
                        comments: comments[requestId] || ""
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Decision failed");
            }

            setMessage(data.message);

            // Refresh requests after the decision
            await fetchLeaveRequests();

        } catch (error) {
            setMessage(error.message);
        }
    }

    if (loading) {
        return <h2>Loading manager dashboard...</h2>;
    }

    // Show only pending requests
    const pendingRequests = leaveRequests.filter(
        request => request.status?.toUpperCase() === "PENDING"
    );

    return (
        <div style={{ padding: "25px" }}>

            <h1 style={{ color: "#245582" }}>
                Manager Dashboard
            </h1>

            <p>Review employee leave requests.</p>

            {message && <p role="status">{message}</p>}

            <h2>Pending Leave Requests</h2>

            {pendingRequests.length === 0 ? (
                <p>No pending leave requests.</p>
            ) : (

                pendingRequests.map(request => (

                    <div key={request.id} style={cardStyle}>

                        <h3>
                            {request.first_name} {request.last_name}
                        </h3>

                        <p>
                            <strong>Leave Type:</strong>{" "}
                            {request.leave_type}
                        </p>

                        <p>
                            <strong>Start Date:</strong>{" "}
                            {request.start_date}
                        </p>

                        <p>
                            <strong>End Date:</strong>{" "}
                            {request.end_date}
                        </p>

                        <p>
                            <strong>Total Days:</strong>{" "}
                            {request.total_days}
                        </p>

                        <p>
                            <strong>Reason:</strong>{" "}
                            {request.reason}
                        </p>

                        <textarea
                            placeholder="Enter manager comments..."
                            value={comments[request.id] || ""}
                            onChange={event =>
                                setComments({
                                    ...comments,
                                    [request.id]: event.target.value
                                })
                            }
                            style={textareaStyle}
                        />

                        <div style={{ display: "flex", gap: "12px" }}>

                            <button
                                onClick={() =>
                                    handleDecision(request.id, "APPROVED")
                                }
                                style={approveButtonStyle}
                            >
                                Approve
                            </button>

                            <button
                                onClick={() =>
                                    handleDecision(request.id, "REJECTED")
                                }
                                style={rejectButtonStyle}
                            >
                                Reject
                            </button>

                        </div>

                    </div>

                ))
            )}

        </div>
    );
}

const cardStyle = {
    backgroundColor: "#f1f5f9",
    padding: "25px",
    borderRadius: "12px",
    marginTop: "20px",
    marginBottom: "20px"
};

const textareaStyle = {
    width: "100%",
    minHeight: "70px",
    padding: "10px",
    marginBottom: "15px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    boxSizing: "border-box"
};

const approveButtonStyle = {
    backgroundColor: "#16a34a",
    color: "white",
    padding: "10px 20px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
};

const rejectButtonStyle = {
    backgroundColor: "#dc2626",
    color: "white",
    padding: "10px 20px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
};

export default ManagerDashboard;
