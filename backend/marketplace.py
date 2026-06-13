from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

# Mock Marketplace Data
MOCK_TEMPLATES = [
    {
        "id": "tpl-1",
        "name": "Daily Email Summarizer",
        "author": "ulo-team",
        "description": "Every morning summarize my emails, create tasks, and generate a daily report.",
        "nodes": [
            {"id": "t1", "type": "ai", "data": {"label": "Summarizer"}},
            {"id": "t2", "type": "productivity", "data": {"label": "Create Tasks"}}
        ],
        "edges": [{"id": "e1", "source": "t1", "target": "t2"}],
        "rating": 4.8,
        "downloads": 1205
    },
    {
        "id": "tpl-2",
        "name": "YouTube Content Pipeline",
        "author": "community",
        "description": "Analyze trending topics and draft YouTube scripts.",
        "nodes": [
            {"id": "t1", "type": "browser", "data": {"label": "Scrape Trends"}},
            {"id": "t2", "type": "ai", "data": {"label": "Draft Script"}}
        ],
        "edges": [{"id": "e1", "source": "t1", "target": "t2"}],
        "rating": 4.5,
        "downloads": 850
    }
]

@router.get("/templates", response_model=List[Dict[str, Any]])
def get_templates():
    return MOCK_TEMPLATES

@router.post("/install/{template_id}")
def install_template(template_id: str):
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        return {"error": "Template not found"}
    # In a real app, this would clone the workflow into the user's local database
    return {"status": "success", "message": f"Installed {template['name']}", "workflow": template}
