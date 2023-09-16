"""Code for backend API."""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

executor = ThreadPoolExecutor()


def slow_function(query: str) -> str:
    import time
    time.sleep(5)  # Simulate slow logic
    return f"Processed query: {query}"


async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            query_data = json.loads(data)  # Assume you're receiving JSON and it contains a 'query' field
            query = query_data.get('query')

            await websocket.send_text(f"Processing query: {query}")

            # Run the slow function asynchronously
            task = asyncio.create_task(run_in_executor(slow_function, query))

            # Wait for it to complete and get the result
            result = await task

            await websocket.send_text(f"Result: {result}")
    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

