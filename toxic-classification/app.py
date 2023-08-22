import json
from fastapi import FastAPI
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from toxicClassifier.pipeline.prediction import PredictionPipeline




text:str = "What is Text Summarization?"

app = FastAPI()

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")



@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")
    



@app.post("/predict")
async def predict_route(text):
    try:
        obj = PredictionPipeline()
        result = obj.predict(text)
        print(result)
        result = json.dumps(result)
        result = json.loads(result)
        return result
        # return {"result":result}
    except Exception as e:
        raise e
    

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
