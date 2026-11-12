
MICROSOFT AGENT FRAMEWORK
IT INCIDENT ROUTING SYSTEM
Authentication: Azure Foundry API Key

Azure Foundry configuration loaded.
Endpoint: https://annabiju-foundryms.openai.azure.com/openai/v1
Deployment: gpt-4.1

Total incidents loaded: 4

Azure Foundry client initialized.
Graph workflow built successfully.

============================================================
Processing Incident: INC101
Description: The corporate email service is unavailable for every employee across the company.


[Triage Agent] Analyzing incident...
[Triage Agent] Severity: HIGH

[Escalation Agent] Handling HIGH-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC101
Severity: HIGH
Assigned Agent: EscalationAgent

1. **Incident Summary**: Complete outage of corporate email service affecting all employees company-wide.

2. **Responsible Support Team**: Messaging/Email Infrastructure Team.

3. **Immediate Containment Actions**:
   - Verify outage and scope.
   - Check email server health and connectivity.
   - Examine recent changes or updates.
   - Restart email services only if safe to do so.

4. **Escalation Procedure**:
   - Notify Messaging/Email Infrastructure Team lead.
   - Escalate to IT Operations Manager and relevant vendor support if not resolved within 30 minutes.
   - Engage senior engineers and incident response team.

5. **Communication Recommendations**:
   - Communicate outage via alternative channels (e.g., intranet, SMS, Teams).
   - Provide ETA and updates every 30 minutes.
   - Issue a company-wide incident status notification and follow-up post-resolution.
------------------------------------------------------------

============================================================
Processing Incident: INC102
Description: One employee's wireless mouse stopped working.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: LOW

[Resolution Agent] Handling LOW-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC102
Severity: LOW
Assigned Agent: ResolutionAgent

Troubleshooting Steps for Wireless Mouse Not Working:

1. **Check the Batteries:**  
   Make sure the wireless mouse has fresh batteries. Replace them if necessary.

2. **Turn the Mouse Off and On:**  
   Switch the mouse off, wait a few seconds, then turn it back on.

3. **Verify the USB Receiver:**  
   Unplug the mouse’s USB receiver from your computer and plug it back in. Try a different USB port if available.

4. **Restart Your Computer:**  
   Sometimes, restarting your computer can fix connection issues.

5. **Test the Mouse on Another Device:**  
   If possible, try using the mouse on another computer to see if it works there.

**When to Escalate:**  
If none of these steps restore functionality, please contact the IT help desk for further assistance.
------------------------------------------------------------

============================================================
Processing Incident: INC103
Description: The company-wide payment processing system is down and transactions are failing.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: HIGH

[Escalation Agent] Handling HIGH-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC103
Severity: HIGH
Assigned Agent: EscalationAgent

1. Incident Summary:  
The payment processing system used company-wide is currently down, causing all transactions to fail.

2. Responsible Support Team:  
Payments/Finance IT Support team

3. Immediate Containment Actions:  
- Disable external access to the payment portal to prevent further failed transactions.  
- Alert system users to pause any payment attempts.  
- Begin system health diagnostics and error log review.

4. Escalation Procedure:  
- Notify Payments IT management and engage application specialists.  
- Escalate to platform/database administrators if root cause is unclear.  
- If vendor involvement is required (e.g., third-party payment gateway), initiate critical support request.

5. Communication Recommendations:  
- Send urgent communication to all affected users and stakeholders.  
- Provide regular status updates (every 30 minutes or as new information becomes available).  
- Communicate clearly regarding estimated resolution time and alternative payment options if available.
------------------------------------------------------------

============================================================
Processing Incident: INC104
Description: One employee cannot print to the nearby office printer.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: LOW

[Resolution Agent] Handling LOW-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC104
Severity: LOW
Assigned Agent: ResolutionAgent

**Troubleshooting Steps for Printing Issue**

1. **Check Printer Power and Connection**  
   Make sure the printer is turned on and securely connected to power. If it’s a wired printer, check the cable connection to your computer.

2. **Select Correct Printer**  
   When printing, confirm you are choosing the correct printer from the list of available printers in your print dialog.

3. **Clear Print Queue**  
   Go to ‘Devices and Printers’ (or ‘Printers & Scanners’) on your computer. Find your printer and clear any stuck print jobs in the queue.

4. **Restart Computer and Printer**  
   Reboot your computer and turn the printer off and back on to reset the connection.

5. **Try Printing from Another Program**  
   Attempt to print from a different application (like Notepad or Word) to see if the issue persists.

**When to Escalate:**  
If these steps do not solve the issue or if other employees also cannot print, escalate the incident to the help desk for further assistance.
------------------------------------------------------------

============================================================
ALL INCIDENTS PROCESSED
============================================================


