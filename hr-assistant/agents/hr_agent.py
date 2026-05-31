import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from tools.mcp_tools import hr_tools

load_dotenv()


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
system_prompt = """You are an Enterprise HR Assistant.

CRITICAL OPERATIONAL RULES:
1. You will receive the user's role (Employee or HR Admin) and name in the prompt system context.
2. If an 'Employee' tries to use administrative tools (approve_leave, update_ticket_status, submit_performance_review, create_employee, schedule_interview), DENY the request politely.
3. NEVER guess, assume, or hallucinate Database IDs. 
4. If a user asks you to execute dependent operations in a single prompt (e.g., "Apply for leave for Bob and then approve it"), you CANNOT run 'approve_leave' with placeholders like 'result_from_previous_function' or guess an ID. You must first run 'apply_leave'. If the tool response doesn't explicitly return the new entry ID, you MUST run 'get_leave_history' to lookup the real ID before calling 'approve_leave'.
5. If a tool returns an error stating an ID or integer parameter is invalid, interpret the error, find the correct information using lookup tools, and try again seamlessly.
6. Output exact confirmation tracking messages provided by tools.
7. Maintain a highly professional, concise enterprise tone.
"""

agent_executor = create_react_agent(llm, hr_tools, prompt=system_prompt)


def chat_with_hr(user_input: str, user_role: str, user_name: str, chat_history: list = []) -> str:
    formatted_history = []

    # Process history pairs securely
    for role, content in chat_history:
        if role == "user":
            formatted_history.append(HumanMessage(content=content))
        else:
            formatted_history.append(AIMessage(content=content))

    # Inject explicit Role-Based Access Control (RBAC) and profile state
    contextual_prompt = f"[System Context: Current User is '{user_name}', Role authorized is '{user_role}'] \nUser Request: {user_input}"
    formatted_history.append(HumanMessage(content=contextual_prompt))

    # Invoke graph engine
    response = agent_executor.invoke({"messages": formatted_history})
    return response["messages"][-1].content
