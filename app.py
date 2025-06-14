import streamlit as st
import json
from main import run_research_agent

st.set_page_config(page_title="Deep Research Agent", layout="wide")

st.title("🧠 Deep Research Agent")
st.caption("Your AI-powered research assistant. Enter a query to start.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to research today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("👩‍💻 Conducting deep research..."):
            result_json = run_research_agent(prompt)
            try:
                results = json.loads(result_json)

                if "error" in results:
                    st.error(f"An error occurred: {results['error']}")
                    response_content = f"Sorry, I encountered an error: {results['error']}"
                else:
                    st.success("Research complete!")
                    
                    final_answer = results.get("final_answer", "No final answer found.")
                    sub_queries = results.get("sub_queries", [])
                    sources = results.get("sources", [])

                    # Format the response
                    response_content = f"""### 📝 Final Answer
{final_answer}

---

#### ❓ Sub-Queries Generated:
"""
                    for q in sub_queries:
                        response_content += f"- {q}\n"
                    
                    response_content += "\n#### 📚 Sources Used:\n"
                    for i, source in enumerate(sources):
                        response_content += f"{i+1}. **{source['title']}** - [{source['url']}]({source['url']})\n"

                    st.markdown(response_content)

            except json.JSONDecodeError:
                st.error("Failed to parse the research results.")
                response_content = "Sorry, I received an invalid response from the research agent."

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})
