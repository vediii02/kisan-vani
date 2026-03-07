import asyncio
import os
import sys
from uuid import uuid4

# Add app to path
sys.path.append(os.getcwd())

from services.voice.llm import get_agent_executor, init_checkpointer
from services.voice.session_context import set_current_organisation_id, set_current_company_id
from langchain_core.messages import HumanMessage

async def test_turn(text: str):
    await init_checkpointer()
    org_id = 1
    comp_id = 1
    set_current_organisation_id(org_id)
    set_current_company_id(comp_id)
    thread_id = str(uuid4())
    executor = await get_agent_executor(org_id, comp_id)
    
    print(f"User: {text}")
    sys.stdout.write("Agent: ")
    sys.stdout.flush()
    
    stream = executor.astream(
        {"messages": [HumanMessage(content=text)]},
        {"configurable": {"thread_id": thread_id}},
        stream_mode="messages"
    )
    
    async for message, metadata in stream:
        is_ai = hasattr(message, 'content') and 'ai' in message.type.lower()
        if is_ai and message.content:
            is_tool = getattr(message, "tool_calls", None) or getattr(message, "tool_call_chunks", None)
            if not is_tool:
                sys.stdout.write(message.content)
                sys.stdout.flush()
    print()

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "__CALL_STARTED__"
    asyncio.run(test_turn(text))
