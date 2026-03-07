import asyncio
import sys
import traceback

async def test_init():
    print("Testing checkpointer init...")
    try:
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
        print("Imported AsyncPostgresSaver")
        from psycopg_pool import AsyncConnectionPool
        print("Imported AsyncConnectionPool")
        
        # We don't need to connect, just checking if imports work.
        print("Imports successful!")
    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_init())
