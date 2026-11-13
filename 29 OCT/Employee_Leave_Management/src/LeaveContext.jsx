
import { createContext, useContext, useState } from "react";

const LeaveContext = createContext();

export function LeaveProvider({ children }) {
  const [leaveRequests, setLeaveRequests] = useState([]);

  function addLeaveRequest(request) {
    const newRequest = {
      id: Date.now(),
      ...request,
      status: "Pending",
    };

    setLeaveRequests((previousRequests) => [
      ...previousRequests,
      newRequest,
    ]);
  }

  return (
    <LeaveContext.Provider value={{ leaveRequests, addLeaveRequest }}>
      {children}
    </LeaveContext.Provider>
  );
}

export function useLeave() {
  return useContext(LeaveContext);
}
