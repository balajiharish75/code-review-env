from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn

from src.environment import CodeReviewEnv
from src.models import Observation, Action

app = FastAPI()
env: Optional[CodeReviewEnv] = None


class ResetRequest(BaseModel):
    task_name: Optional[str] = "review_syntax"
    max_steps: Optional[int] = 5


class StepRequest(BaseModel):
    review: str


@app.post("/reset")
def reset(req: ResetRequest) -> Dict[str, Any]:
    global env
    env = CodeReviewEnv(task_name=req.task_name or "review_syntax", max_steps=req.max_steps or 5)
    obs = env.reset()
    return {
        "observation": obs.model_dump(),
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(req: StepRequest) -> Dict[str, Any]:
    global env
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    obs, reward, done, info = env.step(Action(review=req.review))
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state() -> Dict[str, Any]:
    global env
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized")
    return env.state()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
