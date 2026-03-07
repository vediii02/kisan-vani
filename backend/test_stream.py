import asyncio
from services.voice.llm import get_agent_executor, init_checkpointer
from langchain_core.messages import HumanMessage

async def extract_stream():
    await init_checkpointer()
    executor = await get_agent_executor(1, 1)
    
    stream = executor.astream(
        {"messages": [HumanMessage(content="hi")]},
        {"configurable": {"thread_id": "test_stream_123"}},
        stream_mode="messages"
    )
    
    async for chunk, metadata in stream:
        print(f"[{metadata.get('langgraph_node')}] Type: {type(chunk)} | Content: {getattr(chunk, 'content', chunk)}")

if __name__ == "__main__":
    asyncio.run(extract_stream())
