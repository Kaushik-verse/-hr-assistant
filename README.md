# 🌟 Agentic-HR-Assistant

An intelligent, autonomous Human Resources automation agent built with **LangGraph**, **Groq**, and **Python**. Aura handles natural language HR requests, extracts structured entities, and executes workflows like leave management, employee onboarding, IT ticket routing, and interview scheduling using advanced LLM tool-calling.

## 🚀 Key Features

### 🧠 Agentic AI Capabilities
* **Stateful Conversations:** Built on **LangGraph**, the agent remembers context across multiple turns (e.g., if you mention a leave reason, it will only ask for the missing dates).
* **Autonomous Tool Routing:** Utilizes `llama-3.3-70b-versatile` to intelligently select and execute the correct database tools based on user intent.
* **Missing Information Detection:** Automatically pauses workflows to politely ask the user for required parameters if they are missing from the initial prompt.

### 💼 Automated Workflows
* **Leave Management:** Logs employee time-off and retrieves historical leave records.
* **Smart Ticketing:** Classifies user complaints autonomously into `payroll`, `technical`, `leave`, or `onboarding` buckets.
* **Onboarding & Scheduling:** Creates new employee profiles and schedules interviews via natural language datetime extraction.

### 🖥️ Frontend & Dashboard
* **Glassmorphism UI:** A sleek, modern chat interface built with Streamlit and custom CSS.
* **Live Admin Dashboard:** A dedicated secondary tab that queries the SQLite database in real-time, allowing admins to view all generated records in interactive dataframes.

---

## 🛠️ Tech Stack

* **Framework:** LangGraph / LangChain
* **LLM Provider:** Groq (`llama-3.3-70b-versatile` for high-speed, high-accuracy tool calling)
* **Frontend:** Streamlit
* **Database:** SQLite3
* **Package Manager:** `uv` (Lightning-fast Python environment management)

---

## 📂 Project Structure

```text
hr-assistant/
├── agents/
│   └── hr_agent.py       # LangGraph React Agent and prompt engineering
├── tools/
│   └── mcp_tools.py      # Python tools for DB execution (Leave, Tickets, etc.)
├── database/
│   ├── db_setup.py       # SQLite schema initialization
│   └── hr_database.db    # Auto-generated database file
├── ui/
│   └── app.py            # Streamlit Dual-Tab Frontend (Chat & Dashboard)
├── .env                  # Environment variables (Groq API Key)
├── main.py               # Application entry point
├── pyproject.toml        # Modern uv dependency management
└── README.md

```

---

## ⚙️ Installation & Setup

This project uses [uv](https://github.com/astral-sh/uv) for modern, fast dependency management.

**1. Install `uv` (macOS/Linux):**

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
# OR using Homebrew: brew install uv

```

**2. Clone the repository:**

```bash
git clone [https://github.com/yourusername/hr-assistant.git](https://github.com/yourusername/hr-assistant.git)
cd hr-assistant

```

**3. Set up your environment variables:**
Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=your_actual_api_key_here

```

**4. Run the application:**
`uv` will automatically resolve dependencies, create an isolated environment, and launch the app in one command:

```bash
uv run main.py

```

---

## 🧪 Example Prompts to Test

Once the Streamlit UI is running, try pasting these prompts to test the agent's capabilities:

### The "Happy Paths" (Complete Information)

* *"Onboard a new employee named Ujjwal Asati as a Backend Developer."*
* *"Apply for 5 days of leave for Kaushik due to a family trip."*
* *"Schedule an interview with Aryan Hundia for next Wednesday at 2:00 PM."*
* *"Show me the leave history for Kaushik."*

### The "Edge Cases" (Testing Agent Memory & Logic)

* **Intent Classification:** *"My salary for last month hasn't been credited to my bank account yet."* (Agent should automatically create a `payroll` ticket).
* **Missing Parameters:** *"I need to set up an interview with a candidate named Vishnu."* (Agent should pause and ask what day/time you want to schedule it for).
* **Contextual Memory:** 1. *"I need to apply for leave because of a migraine."*
2. *"Just 2 days, and my name is Kaushik."* (Agent should combine both messages and execute the tool).

---

## 🔮 Future Roadmap

* [ ] **RAG Integration:** Connect to a vector database to allow the bot to answer questions based on a PDF Employee Handbook.
* [ ] **Multi-Agent Architecture:** Split the main agent into a Supervisor Router, a Payroll Specialist, and an IT Support Specialist.
* [ ] **Email Automation:** Integrate SendGrid to send actual calendar invites when the scheduling tool is triggered.

```

```
