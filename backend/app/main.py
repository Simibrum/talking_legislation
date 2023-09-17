"""Code for backend API."""

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from starlette.websockets import WebSocketState
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from common_logic.data_source import LegislationDataSource
from config import logger

app = FastAPI()

executor = ThreadPoolExecutor()

PA1977 = LegislationDataSource('https://www.legislation.gov.uk/ukpga/1977/37/contents/')
PA1977.load_data()


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

def post_process_result(result: dict) -> dict:
    """Post process the function result."""
    # This could be moved into the data source object
    documents = result['source_documents']
    sources = []
    for doc in documents:
        sources.append({
            "text": doc.page_content,
            "citation": doc.metadata["section"] + " " + doc.metadata["title"] + " - " + doc.metadata["source"]
        })
    result['sources'] = sources
    result.pop('source_documents')
    result['state'] = "SUCCESS"
    return result

async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received data: {data}")
            query_data = json.loads(data)  # Assume you're receiving JSON and it contains a 'query' field
            query = query_data.get('query')
            logger.debug(f"Received query: {query}")

            # Prepare preliminary response
            response = {
                "query": query,
                "result": None,
                "sources": [],
                "state": "PROCESSING"
            }
            logger.debug(f"Sending initial response: {response}")
            await websocket.send_json(response)

            # Run the slow function asynchronously
            task = asyncio.create_task(run_in_executor(PA1977.get_answers_and_documents, query))

            # Wait for it to complete and get the result
            result = await task

            logger.info(f"Sending final response: {result}")
            result = post_process_result(result)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    finally:
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.close()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

