
import { useEffect, useState } from "react";
import { apiFetch } from "../api";

function LeaveHistory() {
    const [leaveRequests, setLeaveRequests] = useState([]);
    const [filter, setFilter] = useState("All");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // Fetch leave history from FastAPI
    useEffect(() => {
        async function fetchLeaveHistory() {
            try {
                const response = await apiFetch("/leave-requests");

                if (!response.ok) {
                    throw new Error("Failed to fetch leave history");
                }

                const data = await response.json();

                setLeaveRequests(data);

            } catch (err) {
                console.error("Error fetching leave history:", err);
                setError(err.message);

            } finally {
                setLoading(false);
            }
        }

        fetchLeaveHistory();
    }, []);

    // Filter leave requests based on status
    const filteredRequests = leaveRequests.filter((request) => {
        if (filter === "All") {
            return true;
        }

        return (
            request.status?.toUpperCase() === filter.toUpperCase()
        );
    });

    if (loading) {
        return <h2>Loading leave history...</h2>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    return (
        <div style={{ padding: "25px" }}>

            <h1 style={{ color: "#245582" }}>
                Leave History
            </h1>

            <p style={{ fontSize: "18px" }}>
                View and filter all your previous leave requests.
            </p>

            {/* Filter Buttons */}
            <div style={filterContainerStyle}>

                {["All", "Pending", "Approved", "Rejected"].map(
                    (status) => (
                        <button
                            key={status}
                            onClick={() => setFilter(status)}
                            style={{
                                ...filterButtonStyle,
                                backgroundColor:
                                    filter === status ? "#245582" : "#e2e8f0",
                                color:
                                    filter === status ? "#ffffff" : "#333333"
                            }}
                        >
                            {status}
                        </button>
                    )
                )}

            </div>

            {/* Leave History Table */}
            <div style={{ overflowX: "auto", marginTop: "25px" }}>

                <table style={tableStyle}>

                    <thead>
                        <tr>
                            <th style={headerStyle}>Leave Type</th>
                            <th style={headerStyle}>Start Date</th>
                            <th style={headerStyle}>End Date</th>
                            <th style={headerStyle}>Total Days</th>
                            <th style={headerStyle}>Reason</th>
                            <th style={headerStyle}>Status</th>
                        </tr>
                    </thead>

                    <tbody>

                        {filteredRequests.length > 0 ? (

                            filteredRequests.map((request) => (

                                <tr key={request.id}>

                                    <td style={cellStyle}>
                                        {request.leave_type}
                                    </td>

                                    <td style={cellStyle}>
                                        {request.start_date}
                                    </td>

                                    <td style={cellStyle}>
                                        {request.end_date}
                                    </td>

                                    <td style={cellStyle}>
                                        {request.total_days}
                                    </td>

                                    <td style={cellStyle}>
                                        {request.reason}
                                    </td>

                                    <td style={cellStyle}>
                                        <span
                                            style={{
                                                ...statusStyle,
                                                backgroundColor:
                                                    request.status?.toUpperCase() === "APPROVED"
                                                        ? "#dcfce7"
                                                        : request.status?.toUpperCase() === "REJECTED"
                                                        ? "#fee2e2"
                                                        : "#fef3c7",
                                                color:
                                                    request.status?.toUpperCase() === "APPROVED"
                                                        ? "#166534"
                                                        : request.status?.toUpperCase() === "REJECTED"
                                                        ? "#991b1b"
                                                        : "#92400e"
                                            }}
                                        >
                                            {request.status}
                                        </span>
                                    </td>

                                </tr>

                            ))

                        ) : (

                            <tr>
                                <td
                                    colSpan="6"
                                    style={cellStyle}
                                >
                                    No leave requests found.
                                </td>
                            </tr>

                        )}

                    </tbody>

                </table>

            </div>

        </div>
    );
}

// Filter button styles
const filterContainerStyle = {
    display: "flex",
    gap: "12px",
    flexWrap: "wrap",
    marginTop: "25px"
};

const filterButtonStyle = {
    padding: "10px 22px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: "bold"
};

// Table styles
const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
    backgroundColor: "#ffffff"
};

const headerStyle = {
    backgroundColor: "#245582",
    color: "#ffffff",
    padding: "14px",
    textAlign: "left"
};

const cellStyle = {
    padding: "14px",
    borderBottom: "1px solid #dddddd",
    textAlign: "left"
};

// Status badge styles
const statusStyle = {
    padding: "6px 12px",
    borderRadius: "15px",
    fontWeight: "bold",
    fontSize: "12px"
};

export default LeaveHistory;
