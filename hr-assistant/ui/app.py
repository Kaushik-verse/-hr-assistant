import streamlit as st
import sqlite3
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.hr_agent import chat_with_hr
from database.db_setup import init_db, reset_db

init_db()

st.set_page_config(page_title="Aura HR | Enterprise", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    h1, h2, h3 { color: #0F172A !important; font-family: 'Inter', sans-serif; }
    p, .stMarkdown { color: #334155; }
    .stChatMessage { background-color: #FFFFFF !important; border: 1px solid #E2E8F0; border-radius: 6px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); }
    div[data-testid="stChatInput"] { background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 6px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid #E2E8F0; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; color: #64748B; font-weight: 500; }
    .stTabs [aria-selected="true"] { color: #0F172A !important; border-bottom: 2px solid #0F172A !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# Callback to clear chat on role switch
def reset_chat():
    st.session_state.messages = []


with st.sidebar:
    st.title("Aura HR")
    st.caption("Enterprise Intelligence Hub")
    st.divider()

    st.markdown("### Authentication")
    current_role = st.selectbox("Login Profile:", ["Employee", "HR Admin"], on_change=reset_chat)
    current_user = st.text_input("Username:", value="Jane Doe" if current_role == "Employee" else "Admin User")

    st.divider()
    st.markdown("### System Actions")

    if st.button("🔄 Sync Database", use_container_width=True):
        st.rerun()

    if st.button("⚠️ Reset Database", use_container_width=True):
        reset_db()
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("© 2026 Aura Enterprise Solutions")


def fetch_data(query, params=()):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'hr_database.db'))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


# Dynamic Tab Generation based on Role
if current_role == "HR Admin":
    tabs = st.tabs(["Conversational Agent", "Enterprise Data", "Analytics"])
else:
    tabs = st.tabs(["Conversational Agent", "My Dashboard"])

# ==========================================
# TAB 1: AI CHAT (Available to both)
# ==========================================
with tabs[0]:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about company policies, generate a ticket, or query leave balances..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI Response (Correctly un-indented from the user block)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing request..."):
                history_tuples = [(msg["role"], msg["content"]) for msg in st.session_state.messages[:-1]]

                try:
                    # Try to call the AI
                    response = chat_with_hr(prompt, user_role=current_role, user_name=current_user,
                                            chat_history=history_tuples)
                    st.markdown(response)

                    # Only append to history if successful!
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    # Catch the API error and show a clean UI alert instead of crashing
                    if "Rate limit" in str(e) or "429" in str(e):
                        st.error(
                            "⚠️ AI Engine is currently at maximum capacity. Please wait a few minutes and try again.")
                    else:
                        st.error(f"⚠️ System Error: {str(e)}")
# ==========================================
# TAB 2 & 3: ROLE-SPECIFIC VIEWS
# ==========================================
if current_role == "HR Admin":
    with tabs[1]:
        st.subheader("Global Database Overview")
        tables = {
            "Employees": "SELECT * FROM employees",
            "Leave Requests": "SELECT * FROM leaves",
            "Support Tickets": "SELECT * FROM tickets",
            "Interviews": "SELECT * FROM interviews",
            "Performance Reviews": "SELECT * FROM performance_reviews"
        }
        for title, query in tables.items():
            with st.expander(title, expanded=(title == "Leave Requests")):
                data = fetch_data(query)
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                else:
                    st.info("No records found.")

    with tabs[2]:
        st.subheader("System Analytics")
        col1, col2 = st.columns(2)
        with col1:
            ticket_data = fetch_data("SELECT category, COUNT(*) as count FROM tickets GROUP BY category")
            if ticket_data:
                st.markdown("**Tickets by Category**")
                st.bar_chart(pd.DataFrame(ticket_data).set_index("category"))
            else:
                st.info("Not enough ticket data for chart.")
        with col2:
            leave_data = fetch_data("SELECT status, COUNT(*) as count FROM leaves GROUP BY status")
            if leave_data:
                st.markdown("**Leaves by Status**")
                st.bar_chart(pd.DataFrame(leave_data).set_index("status"))
            else:
                st.info("Not enough leave data for chart.")

elif current_role == "Employee":
    with tabs[1]:
        st.subheader(f"Dashboard for {current_user}")

        my_leaves = fetch_data("SELECT id, days, reason, status FROM leaves WHERE employee_name = ?", (current_user,))
        st.markdown("**My Leave Requests**")
        if my_leaves:
            st.dataframe(pd.DataFrame(my_leaves), use_container_width=True, hide_index=True)
        else:
            st.info("You have no pending or past leave requests.")
