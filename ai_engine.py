import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

class AIEngine:
    def __init__(self):
        """Loads environment variables and configures the Gemini API."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")
        
        genai.configure(api_key=api_key)
        # Using flash for fast, cheap text processing
        #self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_training_module(self, sop_text: str) -> dict:
        """Sends the SOP to Gemini and returns a structured JSON dictionary."""
        prompt = f"""
        Act as an expert corporate trainer. Analyze the following Standard Operating Procedure (SOP) and generate a training module.
        You MUST return ONLY a valid JSON object. Do not include markdown formatting like ```json or ```.
        
        Required JSON Structure:
        {{
            "title": "A short title for the SOP",
            "summary": "A 2-3 sentence overview.",
            "steps": ["Step 1 description", "Step 2 description", "Step 3 description"],
            "quiz": [
                {{
                    "question": "A multiple choice question about the SOP",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "The exact string of the correct option"
                }}
            ]
        }}
        
        Ensure there are exactly 3 quiz questions.
        
        SOP Text to analyze:
        {sop_text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # Clean up potential markdown backticks from the LLM response
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            return json.loads(raw_text.strip())
            
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI output into JSON."}
        except Exception as e:
            return {"error": str(e)}