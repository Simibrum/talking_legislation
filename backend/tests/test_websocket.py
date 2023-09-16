from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from app.main import app  # Replace with your actual import

client = TestClient(app)


def test_websocket_connection():
    with client.websocket_connect("/ws") as websocket:
        data = {"query": "What is the meaning of life?"}
        websocket.send_json(data)
        response = websocket.receive_json()
        assert response["message"] == f"Processing query: {data['query']}"

