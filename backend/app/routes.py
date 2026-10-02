from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm import generate_response, generate_json, stream_response

from fastapi.responses import StreamingResponse

router=APIRouter()

class Message(BaseModel):
    role:str
    content:str

class ChatRequest(BaseModel):
    message:str
    history:list[Message]=[]

class ChatResponse(BaseModel):
    response:str

@router.post("/chat",response_model=ChatResponse)
async def chat(request:ChatRequest):
    prompt=""

    for message in request.history:
        prompt+=f"{message.role}: {message.content}\n"
    
    prompt+=f"user: {request.message}\nassistant:"

    response=await generate_response(prompt)

    return ChatResponse(
        response=response
    )

class SummarizeRequest(BaseModel):
    text:str

@router.post("/summarize",response_model=ChatResponse)
async def summarize(request:SummarizeRequest):
    prompt=f"""
    Summarize the following text clearly and concisely.
    Keep only the important information.
    Use bullet points when appropriate.
    TEXT:
    {request.text}
    """

    response=await generate_response(prompt)

    return ChatResponse(response=response)

class RewriteRequest(BaseModel):
    text:str
    style:str

@router.post("/rewrite",response_model=ChatResponse)
async def rewrite(request:RewriteRequest):
    prompt=f"""
        Rewrite the following text in a {request.style} style.
        Keep the original meaning.
        Do not add new information.
        TEXT:
        {request.text}    
    """
    response=await generate_response(prompt)
    return ChatResponse(response=response)

class ExtractRequest(BaseModel):
    text:str

@router.post("/extract")
async def extract(request:ExtractRequest):
    prompt=f"""
        Extract structured information from the text.
Return ONLY valid JSON using exactly this structure:
{{
  "people": [],
  "tasks": [
    {{
      "task": "",
      "owner": "",
      "deadline": ""
    }}
  ],
  "events": []
}}
Rules:
- Include only information explicitly stated in the text.
- Do not invent names or details.
- Use "User" when the text refers to "I" or "my".
- Put deadlines directly with their corresponding task.
- Put meetings and scheduled events in "events".
- Return valid JSON only.
TEXT:
{request.text}
    """
    result=await generate_json(prompt)
    return result

class GenerateRequest(BaseModel):
    instruction:str

@router.post("/generate",response_model=ChatResponse)
async def generate(request:GenerateRequest):
    prompt=f"""
        Follow the user's instruction and generate the requested content.
        USER INSTRUCTION:
        {request.instruction}
    """
    response=await generate_response(prompt)
    return ChatResponse(response=response)

@router.post("/chat/stream")
async def chat_stream(request:ChatRequest):
    prompt=""
    for message in request.history:
        prompt+=f"{message.role}: {message.content}\n"
    prompt+=f"user: {request.message}\nassistant:"
    return StreamingResponse(
        stream_response(prompt),
        media_type="text/plain",
    )