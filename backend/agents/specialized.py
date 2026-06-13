import os
import google.generativeai as genai
from .base import BaseAgent

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

class GeminiAgent(BaseAgent):
    def __init__(self, name: str, role: str, system_instruction: str):
        super().__init__(name, role)
        self.system_instruction = system_instruction
        self.model = None
        if API_KEY:
            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=self.system_instruction
            )

    def execute(self, task: str, context: dict = None) -> str:
        prompt = f"Task: {task}\n"
        if context:
            prompt += f"Context: {context}\n"
        
        self.add_to_memory({"role": "user", "content": prompt})
        
        if not self.model:
            response_text = f"[{self.name}] Simulated response for: {task}"
        else:
            try:
                response = self.model.generate_content(prompt)
                response_text = response.text
            except Exception as e:
                response_text = f"Error: {str(e)}"
                
        self.add_to_memory({"role": "model", "content": response_text})
        return response_text

class ResearchAgent(GeminiAgent):
    def __init__(self):
        super().__init__("ResearchAgent", "Researcher", "You are an expert researcher. Find detailed, factual information.")

class CodingAgent(GeminiAgent):
    def __init__(self):
        super().__init__("CodingAgent", "Programmer", "You are an expert programmer. Write clean, efficient code.")

class AnalysisAgent(GeminiAgent):
    def __init__(self):
        super().__init__("AnalysisAgent", "Analyst", "You are a data analyst. Extract insights from provided data.")

class PlanningAgent(GeminiAgent):
    def __init__(self):
        super().__init__("PlanningAgent", "Planner", "You are a project planner. Break down complex tasks into steps.")
