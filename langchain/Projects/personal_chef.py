from typing import Any, Dict
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Initialize Tavily Client
tavily_client = TavilyClient()


@tool
def web_search(query: str) -> Dict[str, Any]:
    """search the web for information"""
    return tavily_client.search(query)


# System prompt defining the Personal Chef behavior
system_prompt = """ You are a personal chef. The user will give you a list of ingredients they have left over their house.
                    Using that web search tool, search the web for recipes that can be made with the left ingredients.
                    Return recipe suggestions and eventually the recipe instructions to the user, if requested."""

# Create the agent with Google GenAI model and tools
agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[web_search],
    system_prompt=system_prompt,
)

config = {"configurable": {"thread_id": "1"}}

if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=" i have some left over chicken, some spices and salt left, what can i make?"
                )
            ]
        },
        config,
    )

    last_message = response["messages"][-1]
    if isinstance(last_message.content, list) and len(last_message.content) > 0:
        if isinstance(last_message.content[0], dict) and "text" in last_message.content[0]:
            print(last_message.content[0]["text"])
        else:
            print(last_message.content)
    else:
        print(last_message.content)
