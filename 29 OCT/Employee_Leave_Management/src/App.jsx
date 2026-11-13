import ManagerDashboard from "./components/ManagerDashboard";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import ApplyLeave from "./components/ApplyLeave";
import MyLeaveRequests from "./components/MyLeaveRequests";
import LeaveSummary from "./components/LeaveSummary";
import LeaveHistory from "./components/LeaveHistory";
import Login from "./components/Login";
import ProtectedRoute from "./ProtectedRoute";

import { LeaveProvider } from "./LeaveContext";

function App() {
  return (
    <BrowserRouter>
      <LeaveProvider>
        <div className="app">
          <Navbar />

          <main className="main-content">
            <div className="page-layout">
              <Sidebar />

              <div className="page-content">
                
<Routes>

    {/* Public route */}
    <Route path="/login" element={<Login />} />

    {/* Employee pages */}
    <Route
        path="/"
        element={
            <ProtectedRoute allowedRoles={["EMPLOYEE", "MANAGER", "HR_ADMIN"]}>
                <Dashboard />
            </ProtectedRoute>
        }
    />

    <Route
        path="/apply-leave"
        element={
            <ProtectedRoute allowedRoles={["EMPLOYEE", "MANAGER", "HR_ADMIN"]}>
                <ApplyLeave />
            </ProtectedRoute>
        }
    />

    <Route
        path="/my-requests"
        element={
            <ProtectedRoute allowedRoles={["EMPLOYEE", "MANAGER", "HR_ADMIN"]}>
                <MyLeaveRequests />
            </ProtectedRoute>
        }
    />

    <Route
        path="/leave-summary"
        element={
            <ProtectedRoute allowedRoles={["EMPLOYEE", "MANAGER", "HR_ADMIN"]}>
                <LeaveSummary />
            </ProtectedRoute>
        }
    />

    <Route
        path="/leave-history"
        element={
            <ProtectedRoute allowedRoles={["EMPLOYEE", "MANAGER", "HR_ADMIN"]}>
                <LeaveHistory />
            </ProtectedRoute>
        }
    />

    {/* Manager page */}
    <Route
        path="/manager-dashboard"
        element={
            <ProtectedRoute allowedRoles={["MANAGER", "HR_ADMIN"]}>
                <ManagerDashboard />
            </ProtectedRoute>
        }
    />

    {/* Unauthorized page */}
    <Route
        path="/unauthorized"
        element={<h2>You are not authorized to access this page.</h2>}
    />

</Routes>

               
              </div>
            </div>
          </main>
        </div>
      </LeaveProvider>
    </BrowserRouter>
  );
}

export default App;
