
import { useEffect, useState } from "react";
import { apiFetch } from "../api";

function LeaveSummary() {
    const [leaveRequests, setLeaveRequests] = useState([]);
    const [leaveBalances, setLeaveBalances] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // Fetch leave requests and leave balances
    useEffect(() => {
        async function fetchSummaryData() {
            try {
                const [requestsResponse, balancesResponse] =
                    await Promise.all([
                        apiFetch("/leave-requests"),
                        apiFetch("/leave-balances")
                    ]);

                if (!requestsResponse.ok || !balancesResponse.ok) {
                    throw new Error("Failed to fetch leave summary data");
                }

                const requestsData = await requestsResponse.json();
                const balancesData = await balancesResponse.json();

                setLeaveRequests(requestsData);
                setLeaveBalances(balancesData);

            } catch (err) {
                console.error("Error fetching summary:", err);
                setError(err.message);

            } finally {
                setLoading(false);
            }
        }

        fetchSummaryData();
    }, []);

    // Calculate leave request counts
    const pendingCount = leaveRequests.filter(
        request => request.status?.toUpperCase() === "PENDING"
    ).length;

    const approvedCount = leaveRequests.filter(
        request => request.status?.toUpperCase() === "APPROVED"
    ).length;

    const rejectedCount = leaveRequests.filter(
        request => request.status?.toUpperCase() === "REJECTED"
    ).length;

    // Get Annual Leave balance
    const annualLeaveBalance = leaveBalances.find(
        balance => balance.leave_type === "Annual Leave"
    );

    const remainingAnnualLeave =
        annualLeaveBalance?.remaining_days ?? 0;

    if (loading) {
        return <h2>Loading leave summary...</h2>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    return (
        <div style={{ padding: "25px" }}>
            <h1 style={{ color: "#245582" }}>Leave Summary</h1>

            <p style={{ fontSize: "18px" }}>
                Here is an overview of your leave requests.
            </p>

            {/* Summary Cards */}
            <div style={cardGridStyle}>

                <div style={cardStyle}>
                    <h3>Annual Leave Balance</h3>
                    <h1>{remainingAnnualLeave} days</h1>
                </div>

                <div style={cardStyle}>
                    <h3>Pending Requests</h3>
                    <h1>{pendingCount}</h1>
                </div>

                <div style={cardStyle}>
                    <h3>Approved Requests</h3>
                    <h1>{approvedCount}</h1>
                </div>

                <div style={cardStyle}>
                    <h3>Rejected Requests</h3>
                    <h1>{rejectedCount}</h1>
                </div>

            </div>

            {/* All Leave Balances */}
            <h2 style={{ marginTop: "40px", color: "#245582" }}>
                My Leave Balances
            </h2>

            <div style={balanceGridStyle}>

                {leaveBalances.map((balance) => (
                    <div
                        key={`${balance.leave_type}-${balance.year}`}
                        style={balanceCardStyle}
                    >
                        <h3>{balance.leave_type}</h3>

                        <p>
                            Total Allocated: {balance.total_allocated} days
                        </p>

                        <p>
                            Used: {balance.used_days} days
                        </p>

                        <h2>
                            Remaining: {balance.remaining_days} days
                        </h2>
                    </div>
                ))}

            </div>
        </div>
    );
}

// Summary card styles
const cardGridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "30px",
    marginTop: "30px"
};

const cardStyle = {
    backgroundColor: "#f1f5f9",
    padding: "25px 35px",
    borderRadius: "12px",
    borderLeft: "6px solid #245582"
};

// Leave balance card styles
const balanceGridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px",
    marginTop: "20px"
};

const balanceCardStyle = {
    backgroundColor: "#ffffff",
    padding: "20px",
    borderRadius: "12px",
    border: "1px solid #dbe3ec",
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
};

export default LeaveSummary;
