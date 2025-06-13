import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 🔐 Hardcoded Gemini API Key
GEMINI_API_KEY = "AIzaSyCL6YH9Oji5IWPNIriG_FejN2IzKZfE1LE"

# 🤖 Set up Gemini Flash LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    verbose=False
)

# 🔎 Tool: DuckDuckGo Search
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search.run,
        description="Use this tool to search the internet for recent or real-time facts."
    )
]

# 🧠 Initialize the Agent (with tool and Gemini Flash)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# 🎨 Streamlit App UI
st.set_page_config(page_title="🌐 Real-Time Q&A with Gemini Flash", page_icon="💬")
st.title("🌐 Ask Real-Time Questions with Gemini Flash 💡")
st.markdown("Ask me anything about current events or trending topics. I’ll search the internet and answer using **Gemini Flash** and **DuckDuckGo**!")

# 📥 User input
question = st.text_input("📥 Your Question:", placeholder="e.g., What happened in Ahmedabad today?")

# 🚀 Ask button
if st.button("🔍 Ask"):
    if not question.strip():
        st.warning("⚠️ Please enter a question before clicking Ask.")
    else:
        try:
            with st.spinner("Thinking... 🧠"):
                answer = agent.run(question)
            st.success("✅ Answer:")
            st.markdown(f"**{answer}**")
        except Exception as e:
            st.error("❌ Sorry, something went wrong while generating the answer.")
            st.exception(e)  # optional: remove in production for clean UI
