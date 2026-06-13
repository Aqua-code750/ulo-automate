from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    nodes = Column(JSON, default=list)
    edges = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, index=True)
    status = Column(String, default="running") # running, success, failed
    runtime_ms = Column(Integer, default=0)
    cost = Column(Integer, default=0) # token cost or currency
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

