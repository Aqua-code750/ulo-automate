import os
import json
import google.generativeai as genai

# Setup Gemini model
# In production, use os.environ.get("GEMINI_API_KEY")
API_KEY = os.environ.get("GEMINI_API_KEY", "")

if API_KEY:
    genai.configure(api_key=API_KEY)

# Define the generation config for JSON output
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

def generate_workflow_from_text(prompt: str):
    if not API_KEY:
        # Return a dummy workflow for testing without API key
        return {
            "name": "Generated Workflow",
            "description": f"Workflow for: {prompt}",
            "nodes": [
                {
                    "id": "1",
                    "type": "ai",
                    "position": {"x": 100, "y": 100},
                    "data": {"label": "Trigger", "details": prompt}
                },
                {
                    "id": "2",
                    "type": "logic",
                    "position": {"x": 100, "y": 250},
                    "data": {"label": "Process data"}
                }
            ],
            "edges": [
                {"id": "e1-2", "source": "1", "target": "2"}
            ]
        }
        
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash", # Use a standard model
        generation_config=generation_config,
    )
    
    system_instruction = """
    You are an AI that generates workflow automation schemas based on user requests.
    Output a JSON object with 'name', 'description', 'nodes', and 'edges'.
    Nodes should have 'id' (string), 'type' (string: ai, logic, data, browser, desktop, communication, productivity), 'position' ({x, y}), and 'data' (object with 'label' and other details).
    Edges should have 'id', 'source' (node id), and 'target' (node id).
    Space out the nodes visually so they don't overlap (increase y by 150 for each step).
    """
    
    response = model.generate_content(
        f"{system_instruction}\n\nUser request: {prompt}"
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return {"nodes": [], "edges": []}
