import json
from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from topics import get_topics



text:str = "What is Text Summarization?"

app = FastAPI()

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

    



@app.post("/topics")
async def predict_route(text):
    try:
        result = get_topics(text)
        print(result)
        # result = json.dumps(result)
        return {"result":result}
    except Exception as e:
        raise e

    

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
