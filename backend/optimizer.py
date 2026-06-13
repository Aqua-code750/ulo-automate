import json
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from ai_generator import generation_config, API_KEY

router = APIRouter(prefix="/api/workflows", tags=["optimizer"])

class OptimizeRequest(BaseModel):
    workflow: Dict[str, Any]

@router.post("/optimize", response_model=Dict[str, Any])
def optimize_workflow(request: OptimizeRequest):
    if not API_KEY:
        # Dummy optimization
        optimized = request.workflow.copy()
        optimized["description"] = "Optimized: " + optimized.get("description", "")
        return optimized

    import google.generativeai as genai
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
    )
    
    system_instruction = """
    You are an AI Workflow Optimizer.
    Analyze the provided JSON workflow.
    Suggest faster paths, combine redundant nodes, or pick better models.
    Return the optimized workflow JSON matching the same schema (nodes and edges).
    """
    
    response = model.generate_content(
        f"{system_instruction}\n\nCurrent workflow: {json.dumps(request.workflow)}"
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        print(f"Error optimizing workflow: {e}")
        return request.workflow
