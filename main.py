import os
import uuid
from dotenv import load_dotenv
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from rich.console import Console

from tools import __all__ as tool_lists
from utils import print_message


st.set_page_config(page_title="Cyber Researcher", page_icon=":robot:")
st.title("Cyber Researcher")


load_dotenv()


main_llm_base_url = os.getenv("MAIN_LLM_BASE_URL")
main_llm_api_key = os.getenv("MAIN_LLM_API_KEY")
main_llm_model_name = os.getenv("MAIN_LLM_MODEL_NAME")

if not all([main_llm_base_url, main_llm_api_key, main_llm_model_name]):
    st.error("Missing one or more required environment variables.")
    st.stop()

temperature = os.getenv("TEMPERATURE", 0.1)

model = ChatOpenAI(
    base_url=main_llm_base_url,
    api_key=main_llm_api_key,
    model=main_llm_model_name,
    temperature=temperature,
)

system_prompt = """
You are a meticulous research analyst. When given a topic:
1. Break down the query into key components and identify what needs clarification.
2. Use the internet_search tool with precise, well-constructed queries to gather accurate, up-to-date information.
3. Cross-check facts across multiple sources when possible.
4. Synthesize findings into a clear, well-structured report with sections: Overview, Key Features, Use Cases, and Recent Developments.
5. Cite key insights and avoid speculation. If information is unclear, note that as a limitation.
Always aim for depth, accuracy, and readability.
"""

checkpointer = InMemorySaver()


if "messages" not in st.session_state:
    st.session_state['messages'] = []
if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = str(uuid.uuid4())


config: RunnableConfig = {"configurable": {
    "thread_id": st.session_state['thread_id']}}
print(f"Thread ID: {st.session_state['thread_id']}")


# create the agent with session state
if "agent" not in st.session_state:
    st.session_state['agent'] = create_deep_agent(
        model=model,
        tools=tool_lists,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        backend=FilesystemBackend(root_dir="./sandbox", virtual_mode=True),
    )


if "printed_messages" not in st.session_state:
    st.session_state['printed_messages'] = 0


# ------------------------------------------
# Sidebar
with st.sidebar:
    st.header("Cyber Analyst Agent")
    st.markdown("""
    This agent performs in-depth research by:
    - Breaking down queries
    - Searching the web
    - Synthesizing findings
    - Providing structured reports
    """)

    st.divider()

    st.subheader("Model Configuration")
    st.markdown(f"""
    - **Model**: `{main_llm_model_name}`
    - **Temperature**: `{temperature}`
    """)

    st.divider()

    if st.button("Start a New Session", width="stretch"):
        st.session_state['messages'] = []
        st.session_state['printed_messages'] = 0
        st.session_state['thread_id'] = str(uuid.uuid4())
        st.session_state['agent'] = create_deep_agent(
            model=model,
            tools=tool_lists,
            system_prompt=system_prompt,
            checkpointer=checkpointer,
            backend=FilesystemBackend(root_dir="./sandbox", virtual_mode=True),
        )
        st.rerun()

    st.caption("Session ID: `" + st.session_state['thread_id'][:16] + "...`")

# show the history messages
for msg in st.session_state['messages']:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.markdown(msg.content)


if prompt := st.chat_input("Ask me anything about a topic..."):
    human_msg = HumanMessage(content=prompt)
    st.session_state['messages'].append(human_msg)
    console = Console()
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_container = st.empty()
            full_response = ""

            try:
                for step in st.session_state['agent'].stream(
                    {"messages": [human_msg]},
                    config=config,
                    stream_mode="values",
                ):
                    messages: list[BaseMessage] = step["messages"]
                    latest_msg = messages[-1]
                    # check if the latest message is an AI message and has content to displayeresponse_container
                    for msg in messages[st.session_state['printed_messages']:]:
                        msg: BaseMessage
                        print_message(console=console, msg=msg)

                    st.session_state['printed_messages'] = len(messages)

                    if isinstance(latest_msg, AIMessage) and latest_msg.content:
                        full_response = latest_msg.content
                        response_container.markdown(full_response)

                # save the AI message to the session state
                ai_msg = AIMessage(content=full_response)
                st.session_state['messages'].append(ai_msg)

            except Exception as e:
                st.error(f"Error: {str(e)}")
