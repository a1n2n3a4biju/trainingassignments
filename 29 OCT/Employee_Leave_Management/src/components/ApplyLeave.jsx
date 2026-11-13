
import { useState } from "react";
import { apiFetch } from "../api";

function ApplyLeave() {
  const [formData, setFormData] = useState({
    leaveType: "",
    startDate: "",
    endDate: "",
    reason: "",
  });

  const [message, setMessage] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });

    setMessage("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (
      !formData.leaveType ||
      !formData.startDate ||
      !formData.endDate ||
      !formData.reason.trim()
    ) {
      setMessage("Please fill in all fields.");
      return;
    }

    if (formData.endDate < formData.startDate) {
      setMessage("End date cannot be before the start date.");
      return;
    }

    try {
      const response = await apiFetch("/leave-requests", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          leave_type: formData.leaveType,
          start_date: formData.startDate,
          end_date: formData.endDate,
          reason: formData.reason.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to submit leave request."
        );
      }

      setMessage("Leave request submitted successfully!");

      setFormData({
        leaveType: "",
        startDate: "",
        endDate: "",
        reason: "",
      });

      console.log("Backend response:", data);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <section className="leave-form-container">
      <h2>Apply for Leave</h2>
      <p>Fill in the details below to submit your leave request.</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="leaveType">Leave Type</label>

          <select
            id="leaveType"
            name="leaveType"
            value={formData.leaveType}
            onChange={handleChange}
          >
            <option value="">Select leave type</option>
            <option value="Annual Leave">Annual Leave</option>
            <option value="Sick Leave">Sick Leave</option>
            <option value="Casual Leave">Casual Leave</option>
            <option value="Unpaid Leave">Unpaid Leave</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="startDate">Start Date</label>

          <input
            id="startDate"
            type="date"
            name="startDate"
            value={formData.startDate}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="endDate">End Date</label>

          <input
            id="endDate"
            type="date"
            name="endDate"
            value={formData.endDate}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="reason">Reason for Leave</label>

          <textarea
            id="reason"
            name="reason"
            rows="4"
            placeholder="Enter your reason for leave"
            value={formData.reason}
            onChange={handleChange}
          />
        </div>

        {message && <p role="status">{message}</p>}

        <button type="submit">Submit Leave Request</button>
      </form>
    </section>
  );
}

export default ApplyLeave;
