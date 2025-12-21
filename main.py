import os
import uuid
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from rich.console import Console

from tools import __all__ as tool_lists
from utils import print_message

# Load environment variables
load_dotenv()

# Define model configuration from environment
main_llm_base_url = os.getenv("MAIN_LLM_BASE_URL")
main_llm_api_key = os.getenv("MAIN_LLM_API_KEY")
main_llm_model_name = os.getenv("MAIN_LLM_MODEL_NAME")

# Check if all required environment variables exist
if not all([main_llm_base_url, main_llm_api_key, main_llm_model_name]):
    raise EnvironmentError(
        "Missing one or more required environment variables: MAIN_LLM_BASE_URL, MAIN_LLM_API_KEY, MAIN_LLM_MODEL_NAME"
    )

# Initialize the ChatOpenAI model
model = ChatOpenAI(
    base_url=main_llm_base_url,
    api_key=main_llm_api_key,
    model=main_llm_model_name,
)


system_prompt = """
You are a meticulous research analyst. When given a topxic:
1. Break down the query into key components and identify what needs clarification.
2. Use the internet_search tool with precise, well-constructed queries to gather accurate, up-to-date information.
3. Cross-check facts across multiple sources when possible.
4. Synthesize findings into a clear, well-structured report with sections: Overview, Key Features, Use Cases, and Recent Developments.
5. Cite key insights and avoid speculation. If information is unclear, note that as a limitation.
Always aim for depth, accuracy, and readability.
"""

checkpointer = InMemorySaver()
agent = create_deep_agent(
    model=model,
    tools=tool_lists,
    system_prompt=system_prompt,
    checkpointer=checkpointer,
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)


console = Console()


config: RunnableConfig = {"configurable": {"thread_id": uuid.uuid4()}}

while True:
    try:
        # get user input and exit if needed
        user_input = console.input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            console.print("Goodbye!", style="bold yellow")
            break

        for step in agent.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="values",
        ):
            console.print("\n")
            console.rule("Current State", style="bold blue")

            for msg in step["messages"]:
                msg: BaseMessage
                print_message(console=console, msg=msg)

    except KeyboardInterrupt:
        console.print("Goodbye!", style="bold blue")
        break
