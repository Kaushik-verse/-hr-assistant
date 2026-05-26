import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from tools.mcp_tools import hr_tools

load_dotenv()

# Initialize Groq Model
# Change the model from 8b-instant to 70b-versatile
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

system_prompt = """You are an intelligent, highly efficient HR Assistant. 
Your job is to assist employees with HR workflows by triggering the appropriate tools.

CRITICAL RULES FOR TOOL CALLING:
1. Never guess or make up parameters. If a tool requires a parameter (like an employee name) and the user didn't provide it, politely ask for ONLY the missing specific information.
2. Acknowledge the information the user ALREADY provided so you don't ask for it twice.
3. After you successfully execute a tool, you MUST output the exact confirmation or result provided by the tool back to the user. Do not silently move on.

Categories for tickets MUST be one of: 'payroll', 'technical', 'leave', 'onboarding'.
Always respond with a friendly, professional tone.
"""

# Create the LangGraph agent
# This replaces both the ChatPromptTemplate and the AgentExecutor
agent_executor = create_react_agent(llm, hr_tools, prompt=system_prompt)

def chat_with_hr(user_input: str, chat_history: list = []) -> str:
    """Function to process user input and return the agent's response."""

    # Format the Streamlit history into LangChain Message objects
    formatted_history = []
    for role, content in chat_history:
        if role == "user":
            formatted_history.append(HumanMessage(content=content))
        elif role == "assistant":
            formatted_history.append(AIMessage(content=content))

    # Add the current user input to the end of the history
    formatted_history.append(HumanMessage(content=user_input))

    # Invoke the LangGraph agent
    response = agent_executor.invoke({"messages": formatted_history})

    # The output is the content of the very last message in the state
    return response["messages"][-1].content