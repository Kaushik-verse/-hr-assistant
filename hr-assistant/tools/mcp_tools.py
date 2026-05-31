from langchain_core.tools import tool
from database.db_setup import execute_query


@tool
def create_employee(name: str, role: str) -> str:
    """Executes the full onboarding workflow: creates employee, IT ticket, and Payroll ticket."""
    # 1. Create the Employee
    execute_query("INSERT INTO employees (name, role) VALUES (?, ?)", (name, role))

    # 2. Automatically generate an IT Ticket
    it_issue = f"Provision new laptop, email, and system access for {name} ({role})"
    execute_query("INSERT INTO tickets (category, issue) VALUES (?, ?)", ("technical", it_issue))

    # 3. Automatically generate a Payroll Ticket
    payroll_issue = f"Setup direct deposit and tax compliance forms for {name}"
    execute_query("INSERT INTO tickets (category, issue) VALUES (?, ?)", ("payroll", payroll_issue))

    return f"Workflow Complete: Onboarded {name}. IT and Payroll tickets were automatically generated in the background."


@tool
def apply_leave(employee_name: str, start_date: str, days: str, reason: str) -> str:
    """Applies for leave and checks for team coverage conflicts. Requires a start_date string (e.g., 'May 1st')."""
    # Defensive parameter validation
    if not str(days).isdigit():
        return f"Error: The 'days' argument must be a clean numeric integer (e.g., '3'). Got: '{days}'."

    active_leaves = execute_query("SELECT COUNT(*) FROM leaves WHERE status = 'Approved'")

    conflict_warning = ""
    if active_leaves and active_leaves[0][0] >= 2:
        conflict_warning = "\n⚠️ WARNING: Low team coverage detected. Multiple team members are already on leave. Approval may be delayed."

    execute_query("INSERT INTO leaves (employee_name, start_date, days, reason) VALUES (?, ?, ?, ?)",
                  (employee_name, start_date, int(days), reason))

    return f"Success: Leave applied for {employee_name} starting {start_date} ({days} days).{conflict_warning}"


@tool
def get_leave_history(employee_name: str) -> str:
    """Retrieves leave history and IDs for a specific employee."""
    records = execute_query("SELECT id, start_date, days, reason, status FROM leaves WHERE employee_name = ?",
                            (employee_name,))
    if not records:
        return f"No leave history found for {employee_name}."
    history = "\n".join(
        [f"ID: {r[0]} | Starts {r[1]} for {r[2]} days. Reason: '{r[3]}' (Status: {r[4]})" for r in records])
    return f"Leave History for {employee_name}:\n{history}"


@tool
def approve_leave(leave_id: str, status: str) -> str:
    """Updates the status of a leave request (e.g., 'Approved', 'Rejected'). Requires HR Admin."""
    # Defensive parameter validation preventing crashes
    if not str(leave_id).isdigit():
        return f"Error: Invalid leave_id '{leave_id}'. You must provide a real numeric ID. Use get_leave_history to find it first."

    execute_query("UPDATE leaves SET status = ? WHERE id = ?", (status, int(leave_id)))
    return f"Success: Leave ID {leave_id} updated to {status}."


@tool
def create_ticket(category: str, issue: str) -> str:
    """Creates an HR support ticket. Categories: 'payroll', 'technical', 'leave', 'onboarding'."""
    valid = ['payroll', 'technical', 'leave', 'onboarding']
    category = category.lower() if category.lower() in valid else 'technical'
    execute_query("INSERT INTO tickets (category, issue) VALUES (?, ?)", (category, issue))
    return f"Success: {category.capitalize()} ticket created."


@tool
def update_ticket_status(ticket_id: str, status: str) -> str:
    """Updates an HR ticket status (e.g., 'In Progress', 'Resolved'). Requires HR Admin."""
    # Defensive parameter validation
    if not str(ticket_id).isdigit():
        return f"Error: Invalid ticket_id '{ticket_id}'. You must provide a clean numeric ID."

    execute_query("UPDATE tickets SET status = ? WHERE id = ?", (status, int(ticket_id)))
    return f"Success: Ticket ID {ticket_id} updated to {status}."


@tool
def schedule_interview(candidate_name: str, scheduled_time: str) -> str:
    """Schedules a candidate interview."""
    execute_query("INSERT INTO interviews (candidate_name, scheduled_time) VALUES (?, ?)",
                  (candidate_name, scheduled_time))
    return f"Success: Interview scheduled for {candidate_name} on {scheduled_time}."


@tool
def submit_performance_review(employee_name: str, reviewer: str, rating: str, comments: str) -> str:
    """Submits a performance review (Rating 1-5)."""
    # Defensive parameter validation
    if not str(rating).isdigit():
        return f"Error: 'rating' must be a clean numeric digit between 1 and 5. Got: '{rating}'."

    execute_query("INSERT INTO performance_reviews (employee_name, reviewer, rating, comments) VALUES (?, ?, ?, ?)",
                  (employee_name, reviewer, int(rating), comments))
    return f"Success: Review submitted for {employee_name}."


@tool
def get_company_policy(topic: str) -> str:
    """Retrieves company policies. Topics: 'wfh', 'leave', 'expenses'."""
    policies = {
        "wfh": "Employees are allowed 2 days of Work From Home per week subject to manager approval.",
        "leave": "Employees get 20 days of paid time off per year. Sick leave is unlimited.",
        "expenses": "Meals during travel are reimbursed up to $50/day with receipts."
    }
    return policies.get(topic.lower(), "Policy not found. Please contact HR directly.")


hr_tools = [create_employee, apply_leave, get_leave_history, approve_leave,
            create_ticket, update_ticket_status, schedule_interview,
            submit_performance_review, get_company_policy]
