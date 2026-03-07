import asyncio
from typing import Annotated, Literal, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    stage: str

def greeting_node(state: AgentState):
    print("Greeting Node executed")
    return {"messages": [AIMessage(content="Hello!")]}

def router(state: AgentState) -> str:
    print(f"Router checking stage: {state.get('stage')}")
    if state.get("stage") == "greeting":
        return "greeting"
    return END

async def main():
    workflow = StateGraph(AgentState)
    workflow.add_node("greeting", greeting_node)
    workflow.add_conditional_edges(START, router, {"greeting": "greeting", END: END})
    workflow.add_edge("greeting", END)
    
    app = workflow.compile()
    
    state = {"messages": [HumanMessage(content="Hi")], "stage": "greeting"}
    config = {"configurable": {"thread_id": "test"}}
    
    async for event in app.astream(state, config=config):
        print(event)

if __name__ == "__main__":
    asyncio.run(main())
