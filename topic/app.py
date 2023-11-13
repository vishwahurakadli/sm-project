import json
from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from topics import get_topics



text:str = "What is Text Summarization?"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

    



@app.get("/topics")
async def predict_route(text):
    try:
        result = get_topics(text)
        print("****result****",result)
        # result = json.dumps(result)
        return {"result":result}
    except Exception as e:
        raise e

    

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
