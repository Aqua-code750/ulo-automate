from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import models
from database import get_db

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowResponse(WorkflowBase):
    id: int

    class Config:
        orm_mode = True

@router.post("/", response_model=WorkflowResponse)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = models.Workflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@router.get("/", response_model=List[WorkflowResponse])
def read_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workflows = db.query(models.Workflow).offset(skip).limit(limit).all()
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def read_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(workflow_id: int, workflow_update: WorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    update_data = workflow_update.dict()
    for key, value in update_data.items():
        setattr(db_workflow, key, value)
        
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

class GenerateRequest(BaseModel):
    prompt: str

@router.post("/generate", response_model=Dict[str, Any])
def generate_workflow(request: GenerateRequest):
    from ai_generator import generate_workflow_from_text
    workflow_data = generate_workflow_from_text(request.prompt)
    return workflow_data

class RunResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    runtime_ms: int
    cost: int
    
    class Config:
        orm_mode = True

@router.get("/analytics/runs", response_model=List[RunResponse])
def get_analytics(db: Session = Depends(get_db)):
    runs = db.query(models.WorkflowRun).all()
    return runs
