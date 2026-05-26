# AI-Powered HR Assistant 

An intelligent, end-to-end HR automation agent built using Python, LangChain, Groq, and a minimalist SQLite backend. The system utilizes tool-calling to autonomously detect intent, extract entities, and execute HR workflows.

## Features
* **Leave Management:** AI extracts days and reasons to log leaves.
* **Ticket Routing:** Automatically classifies issues (payroll, tech, leave) and generates tickets.
* **Onboarding Automation:** Creates employee profiles via natural language.
* **Interview Scheduling:** Extracts datetime entities to set up calendar logs.
* **Glassmorphism UI:** Clean, fluid Streamlit frontend.

## Setup Instructions

1.  **Clone/Create the Repository:** Ensure the folder structure matches the project outline.
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables:** Create a `.env` file in the root directory and add your Groq API Key:
    ```env
    GROQ_API_KEY=your_api_key_here
    ```
4.  **Run the Application:**
    Execute the main runner to initialize the database and launch the UI:
    ```bash
    python main.py
    ```

## Example Prompts to Test
* *“Add employee Rahul as a Python Developer.”*
* *“Apply leave for Rahul for 3 days due to fever.”*
* *“Show my leave history.” (Assuming you are Rahul)*
* *“My salary is delayed.” (Triggers payroll ticket)*
* *“Schedule an interview with John Doe for Friday at 3 PM.”*