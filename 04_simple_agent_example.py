import streamlit as st
from agents.agent import Agent
from agents.tools import Tool, Parameter

# Funciones
def sumar(a: int, b: int) -> int:
    return a + b

def multiplicar(a: int, b: int) -> int:
    return a * b

def restar(a: int, b: int) -> int:
    return a - b

# Tools
sumar_tool = Tool(
    name="sumar",
    func=sumar,
    description="Sumar dos números",
    arguments=[
        Parameter(name="a", description="Primer número", type=int, required=True),
        Parameter(name="b", description="Segundo número", type=int, required=True)
    ]
)

multiplicar_tool = Tool(
    name="multiplicar",
    func=multiplicar,
    description="Multiplicar dos números",
    arguments=[
        Parameter(name="a", description="Primer número", type=int, required=True),
        Parameter(name="b", description="Segundo número", type=int, required=True)
    ]
)

restar_tool = Tool(
    name="restar",
    func=restar,
    description="Restar dos números",
    arguments=[
        Parameter(name="a", description="Primer número", type=int, required=True),
        Parameter(name="b", description="Segundo número", type=int, required=True)
    ]
)

# Definir lista de herramientas y esquema
tools = [sumar_tool, multiplicar_tool, restar_tool]

if "agent" not in st.session_state:
    st.session_state["agent"] = Agent(tools)

st.title("🤖 Simple Agent Example")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Como te puedo ayudar?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if goal := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": goal})
    st.chat_message("user").write(goal)
    agent = st.session_state["agent"]
    
    final_answer = agent.execute_chain_of_thought(goal)

    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    st.chat_message("assistant").write(final_answer)