# 🌟 Agentic-HR-Assistant

An intelligent, enterprise-style Human Resources automation platform built with LangChain, LangGraph, Groq, Streamlit, and SQLite. The system combines conversational AI, role-based access control, autonomous workflow execution, and real-time analytics to streamline HR operations such as onboarding, leave management, ticket handling, employee support, and organizational reporting.

---

## ✨ Main Features

### 🔐 Role-Based Access Control (RBAC)
- Secure separation between Employee and HR Admin environments.
- Employees can access self-service HR functionalities.
- HR Administrators gain access to organization-wide management tools, dashboards, and analytics.

### 🤖 Intelligent Conversational Agent
- Powered by LangChain, LangGraph, and Groq Llama models.
- Understands natural language queries and converts them into database actions.
- Supports contextual conversations and multi-step reasoning.

### ⚡ Complex Agentic Workflows

#### Smart Employee Onboarding
A single onboarding request automatically:
- Creates an employee profile.
- Generates IT provisioning tickets.
- Triggers payroll setup workflows.
- Executes multiple tasks concurrently through agentic orchestration.

#### Context-Aware Leave Management
- Processes leave requests intelligently.
- Detects department coverage conflicts.
- Warns HR when multiple employees from the same team are already on leave.
- Helps maintain workforce availability before approving requests.

### 📊 Dynamic Data Center
- Live SQLite database integration.
- Real-time employee, leave, onboarding, and ticket records.
- Interactive Streamlit tables powered by Pandas.
- Dashboard metric cards for quick organizational insights.

### 🛡️ Defensive Tool Calling
- Built-in validation and error handling.
- Self-correcting agent workflows.
- Safe execution of CRUD database operations.
- Reduced risk of invalid updates or data corruption.

### 📈 System Analytics
- Automated visual reports and dashboards.
- Ticket status analytics.
- Leave request trend analysis.
- Interactive charts and organizational metrics.

### 💎 Modern Enterprise UI
- Built using Streamlit with custom styling.
- Clean dashboard experience.
- Interactive chat interface for natural HR interactions.

---

## 🛠️ Technology Stack

| Category | Technologies |
|-----------|-------------|
| Frontend / UI | Streamlit, Custom Enterprise CSS |
| AI Orchestration | LangChain, LangGraph, React Agents |
| LLM Provider | Groq (Llama-3.1-8B, Llama-3-70B) |
| Database | SQLite3 |
| Data Processing | Pandas |
| Visualization | Matplotlib |
| Backend Language | Python |
| Agent Features | Tool Calling, Multi-Step Workflows, State Management |

---

## 🧪 Testing the Agent

The application includes a Reset Database option in the sidebar, allowing testers to restore the system to a clean state before running demonstrations.

### Employee Prompts

 What is the WFH policy? 

 Apply for leave starting next Monday for 3 days due to sickness. 

 Show my leave history. 

 Create a support ticket because my laptop is not working. 

### HR Admin Prompts

 Onboard a new employee named Alice Johnson as a UX Designer. 

 Fetch the leave history for Bob. 

 Update ticket ID 1 to Resolved. 

 Show ticket analytics for the organization. 

 How many employees are currently on leave? 

---

## 🚀 Future Enhancements

- RAG-powered Employee Policy Assistant.
- Email and Calendar Integration.
- Multi-Agent HR Ecosystem.
- Department-Level Workforce Forecasting.
- Predictive Leave Analytics.
- Cloud Database Support (PostgreSQL/MySQL).
- Authentication and Enterprise SSO.

---

## 📸 Demo

Run the application locally and explore both Employee and HR Admin modes.

The platform demonstrates how modern AI agents can automate complex HR operations while maintaining security, reliability, and real-time visibility across organizational workflows

---

## 👨‍💻 Author

**Ch Sai Kaushik**  
B.Tech CSE (Data Science), VIT Vellore

⭐ If you found this project useful, consider giving it a star on GitHub.
