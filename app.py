from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
from typing import Dict
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq
from src.prompt import prompt
from store_index import vectorstore_from_docs

# Initialize FastAPI app
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize LLM and RAG chain once at startup
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

retriever = vectorstore_from_docs.as_retriever()
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, list] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket] = []  # Initialize empty chat history

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

async def generate_rag_response(user_message: str) -> str:
    """Generate response using RAG chain"""
    try:
        
        response = rag_chain.invoke({"input": user_message})
        return response["answer"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    chat_history = manager.active_connections[websocket]
    
    try:
        while True:
            # Receive and parse message
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                await manager.send_message(websocket, "Error: Invalid message format")
                continue
                
            user_message = message_data.get("message", "").strip()
            if not user_message:
                continue
                
            # Store user message in history
            chat_history.append({"role": "user", "content": user_message})
            
            # Echo user message
            await manager.send_message(websocket, f"User: {user_message}")
            
            # Generate and send RAG response
            bot_response = await generate_rag_response(user_message)
            chat_history.append({"role": "assistant", "content": bot_response})
            prefix = "Bot: " if not bot_response.startswith("Error:") else ""
            await manager.send_message(websocket, f"{prefix}{bot_response}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_message(websocket, f"Error: Unexpected error - {str(e)}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")