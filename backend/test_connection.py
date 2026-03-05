import asyncio
from database import engine

async def test():
    try:
        async with engine.connect() as conn:
            print("✅ Connected to walk_n_style database successfully!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Check: 1) pgAdmin is running  2) Password in .env is correct  3) DB name is walk_n_style")

asyncio.run(test())