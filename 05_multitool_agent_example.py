import streamlit as st
from agents.agent import Agent

from agents.tools.fs import SearchDirectory, ListDirectory, ViewFile
from agents.tools.llm import QueryFile
from agents.tools.github import GetUserInfo, GetRepositories, CloneRepo, CreateIssue, GetIssueDetails, GetIssues

if "agent" not in st.session_state:
    st.session_state["agent"] = Agent(
        [
            GetUserInfo(), 
            GetRepositories(),
            CloneRepo(),
            CreateIssue(),
            GetIssueDetails(),
            GetIssues(),
            ListDirectory(),
            SearchDirectory(),
            ViewFile(),
            QueryFile(),
        ]
    )

st.title("🤖 Multi Tool Agent Example")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if goal := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": goal})
    st.chat_message("user").write(goal)
    agent = st.session_state["agent"]
    
    final_answer = agent.execute_chain_of_thought(goal)

    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    st.chat_message("assistant").write(final_answer)