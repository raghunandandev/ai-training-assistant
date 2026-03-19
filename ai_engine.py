import google.generativeai as genai
import os
import json
import streamlit as st
from dotenv import load_dotenv

class AIEngine:
    def __init__(self):
        """Configures the Gemini API for both local and cloud deployment."""
        
        # 1. Try to get the key from Streamlit Cloud Secrets
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            # 2. If that fails (meaning you are testing locally), load the .env file
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            
        # 3. Final safety check
        if not api_key:
            raise ValueError("API Key not found in Streamlit Secrets or .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_training_module(self, sop_text: str) -> dict:
        """Sends the SOP to Gemini and returns a structured JSON dictionary."""
        prompt = f"""
        Act as an expert Corporate Instructional Designer. Analyze the following Standard Operating Procedure (SOP) and engineer a high-impact training module.
        You MUST return ONLY a valid JSON object. Do not include markdown formatting.
        
        Required JSON Structure:
        {{
            "metadata": {{
                "title": "A highly professional title for the SOP",
                "estimated_time_minutes": "Estimated time to complete this process (integer)",
                "complexity": "Beginner, Intermediate, or Advanced",
                "tools_required": ["List of any software, tools, or physical items needed"]
            }},
            "executive_summary": "A sharp, 2-sentence business overview of why this SOP exists.",
            "phases": [
                {{
                    "phase_name": "Name of the phase (e.g., Preparation, Execution)",
                    "steps": ["Step 1", "Step 2"],
                    "critical_warning": "One major mistake to avoid in this phase (if any)"
                }}
            ],
            "scenario_quiz": [
                {{
                    "scenario": "A brief, realistic 2-sentence real-world situation where things go wrong or a decision is needed based on the SOP.",
                    "question": "What is the correct action to take?",
                    "options": ["A", "B", "C", "D"],
                    "answer": "The exact string of the correct option",
                    "explanation": "A 1-sentence explanation of WHY this is the right answer."
                }}
            ]
        }}
        
        Ensure there are exactly 3 scenario-based questions.
        
        SOP Text:
        {sop_text}
        """
        # prompt = f"""
        # Act as an expert corporate trainer. Analyze the following Standard Operating Procedure (SOP) and generate a training module.
        # You MUST return ONLY a valid JSON object. Do not include markdown formatting like ```json or ```.
        
        # Required JSON Structure:
        # {{
        #     "title": "A short title for the SOP",
        #     "summary": "A 2-3 sentence overview.",
        #     "steps": ["Step 1 description", "Step 2 description", "Step 3 description"],
        #     "quiz": [
        #         {{
        #             "question": "A multiple choice question about the SOP",
        #             "options": ["Option A", "Option B", "Option C", "Option D"],
        #             "answer": "The exact string of the correct option"
        #         }}
        #     ]
        # }}
        
        # Ensure there are exactly 3 quiz questions.
        
        # SOP Text to analyze:
        # {sop_text}
        # """
        
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






# import google.generativeai as genai
# import os
# import json
# from dotenv import load_dotenv

# class AIEngine:
#     def __init__(self):
#         """Loads environment variables and configures the Gemini API."""
#         load_dotenv()
#         api_key = os.getenv("GEMINI_API_KEY")
#         if not api_key:
#             raise ValueError("GEMINI_API_KEY not found in .env file.")
        
#         genai.configure(api_key=api_key)
#         # Using flash for fast, cheap text processing
#         #self.model = genai.GenerativeModel('gemini-1.5-flash')
#         self.model = genai.GenerativeModel('gemini-2.5-flash')

#     def generate_training_module(self, sop_text: str) -> dict:
#         """Sends the SOP to Gemini and returns a structured JSON dictionary."""
#         prompt = f"""
#         Act as an expert corporate trainer. Analyze the following Standard Operating Procedure (SOP) and generate a training module.
#         You MUST return ONLY a valid JSON object. Do not include markdown formatting like ```json or ```.
        
#         Required JSON Structure:
#         {{
#             "title": "A short title for the SOP",
#             "summary": "A 2-3 sentence overview.",
#             "steps": ["Step 1 description", "Step 2 description", "Step 3 description"],
#             "quiz": [
#                 {{
#                     "question": "A multiple choice question about the SOP",
#                     "options": ["Option A", "Option B", "Option C", "Option D"],
#                     "answer": "The exact string of the correct option"
#                 }}
#             ]
#         }}
        
#         Ensure there are exactly 3 quiz questions.
        
#         SOP Text to analyze:
#         {sop_text}
#         """
        
#         try:
#             response = self.model.generate_content(prompt)
#             raw_text = response.text.strip()
            
#             # Clean up potential markdown backticks from the LLM response
#             if raw_text.startswith("```json"):
#                 raw_text = raw_text[7:]
#             if raw_text.startswith("```"):
#                 raw_text = raw_text[3:]
#             if raw_text.endswith("```"):
#                 raw_text = raw_text[:-3]
                
#             return json.loads(raw_text.strip())
            
#         except json.JSONDecodeError:
#             return {"error": "Failed to parse AI output into JSON."}
#         except Exception as e:
#             return {"error": str(e)}