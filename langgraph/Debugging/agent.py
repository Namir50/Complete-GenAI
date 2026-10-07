from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.messages import HumanMessage,SystemMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START,END
from tavily import TavilyClient
from typing import TypedDict,Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
import os
from langgraph.types import Command, interrupt

load_dotenv()

llm = init_chat_model(model="groq:openai/gpt-oss-20b")

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "langgraph-debugging" #langsmith  project name

@tool
def add(a:float, b:float):
    """add two numbers"""
    return a +b

tools = [add]

llm_binded = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list,add_messages]

def llm_functionality(state:State):
    return {"messages":[llm_binded.invoke(state['messages'])]}

tool_node = ToolNode(tools=tools)

builder = StateGraph(State)

builder.add_node("tool_calling_llm",llm_functionality)
builder.add_node("tools",tool_node)

builder.add_edge(START,"tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition
)
builder.add_edge("tools", "tool_calling_llm")

graph = builder.compile()