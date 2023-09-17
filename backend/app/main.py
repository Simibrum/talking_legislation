"""Code for backend API."""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from starlette.websockets import WebSocketState
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from backend.common_logic.data_source import LegislationDataSource

app = FastAPI()

executor = ThreadPoolExecutor()

PA1977 = LegislationDataSource('https://www.legislation.gov.uk/ukpga/1977/37/contents/')


def slow_function(query: str) -> dict:
    import time
    time.sleep(5)  # Simulate slow logic
    # Simulate a result
    result = f"Your query was: {query}"
    sources = [
        {"text": "Source 1", "citation": "Citation 1"},
        {"text": "Source 2", "citation": "Citation 2"},
        {"text": "Source 3", "citation": "Citation 3"}
    ]

    # Prepare the response
    response = {
        "query": query,
        "result": result,
        "sources": sources,
        "state": "SUCCESS"
    }
    return response


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

            # Prepare preliminary response
            response = {
                "query": query,
                "result": None,
                "sources": [],
                "state": "PROCESSING"
            }

            await websocket.send_json(response)

            # Run the slow function asynchronously
            task = asyncio.create_task(run_in_executor(PA1977.get_answers_and_documents, query))

            # Wait for it to complete and get the result
            result = await task

            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    finally:
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.close()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

