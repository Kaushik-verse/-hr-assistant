from langchain_core.tools import tool
from database.db_setup import execute_query
from pydantic import BaseModel, Field


# We use LangChain's @tool to make these compatible with the Groq agent immediately.
# In a pure FastMCP standalone architecture, you would wrap these with @mcp.tool().

@tool
def create_employee(name: str, role: str) -> str:
    """Creates a new employee onboarding record."""
    execute_query("INSERT INTO employees (name, role) VALUES (?, ?)", (name, role))
    return f"Success: Onboarding record created for {name} as {role}."


@tool
def apply_leave(employee_name: str, days: int, reason: str) -> str:
    """Applies for leave for an employee."""
    execute_query(
        "INSERT INTO leaves (employee_name, days, reason) VALUES (?, ?, ?)",
        (employee_name, days, reason)
    )
    return f"Success: Leave applied for {employee_name} for {days} days. Reason: {reason}."


@tool
def get_leave_history(employee_name: str) -> str:
    """Retrieves the leave history for a specific employee."""
    records = execute_query("SELECT days, reason, status FROM leaves WHERE employee_name = ?", (employee_name,))
    if not records:
        return f"No leave history found for {employee_name}."

    history = "\n".join([f"- {r[0]} days for '{r[1]}' (Status: {r[2]})" for r in records])
    return f"Leave History for {employee_name}:\n{history}"


@tool
def create_ticket(category: str, issue: str) -> str:
    """
    Creates an HR support ticket.
    Category MUST be one of: 'payroll', 'technical', 'leave', 'onboarding'.
    """
    valid_categories = ['payroll', 'technical', 'leave', 'onboarding']
    if category.lower() not in valid_categories:
        category = 'technical'  # default fallback

    execute_query("INSERT INTO tickets (category, issue) VALUES (?, ?)", (category.lower(), issue))
    return f"Success: {category.capitalize()} ticket created for issue: '{issue}'."


@tool
def schedule_interview(candidate_name: str, scheduled_time: str) -> str:
    """Schedules an interview with a candidate. Time should be a descriptive string (e.g., 'Friday at 3 PM')."""
    execute_query(
        "INSERT INTO interviews (candidate_name, scheduled_time) VALUES (?, ?)",
        (candidate_name, scheduled_time)
    )
    return f"Success: Interview scheduled for {candidate_name} on {scheduled_time}."


# Export list of tools for the agent
hr_tools = [create_employee, apply_leave, get_leave_history, create_ticket, schedule_interview]