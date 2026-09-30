from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,SystemMessage

import os

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"],
                "transport":"stdio",
            },
            "weather":{
                "url":"http://127.0.0.1:8000/mcp", #here we are doing slash mcp as it will captrue all the mcps from this url
                "transport":"streamable-http",
            }
        }
    )

    tools = await client.get_tools()
    model = init_chat_model("groq:qwen/qwen3.8-27b")
    agent = create_agent(
        model=model,
        tools=tools
    )

    response = await agent.ainvoke({"messages": [HumanMessage(content="what is the weather and temperature now in new york?")]})
    print(response["messages"][-1].content)

asyncio.run(main())