import requests
import os
import json
from dotenv import load_dotenv  


load_dotenv()

class BusinessInsightsAssistant:
    def __init__(self, api_key=None):
        """Initialize the assistant with Gemini API key."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")  
        if not self.api_key:
            raise ValueError("Error: GEMINI_API_KEY is not set. Please set it before running.")

        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        self.functions = ["finance", "marketing", "operations", "sales"]

    def preprocess_query(self, query):
        """Extract context and business function from the query."""
        query = query.lower()
        for func in self.functions:
            if func in query:
                return {"text": query, "function": func}
        return {"text": query, "function": "general"}

    def generate_prompt(self, query_info):
        """Generate a business-specific prompt for Gemini."""
        function = query_info["function"]
        text = query_info["text"]

        templates = {
            "finance": f"Provide a financial analysis of {text} including revenue trends, profit margins, and investment opportunities.",
            "marketing": f"Analyze marketing strategies for {text} and suggest campaigns to increase brand visibility.",
            "operations": f"Evaluate operational efficiencies for {text} and recommend process improvements.",
            "sales": f"Assess sales performance for {text} and propose strategies to boost revenue.",
            "general": f"Analyze the business query '{text}' and provide structured insights and actionable recommendations."
        }
        return templates.get(function, templates["general"])

    def call_gemini_api(self, prompt):
        """Send prompt to Gemini API and get response."""
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]  
        }
        
        try:
            
            response = requests.post(f"{self.base_url}?key={self.api_key}", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return f"Error calling Gemini API: {e}"

    def postprocess_response(self, raw_response):
        """Structure the raw API response into a report."""
        if "Error" in raw_response:
            return raw_response
        
        text_response = raw_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received")
        
        return {
            "Summary": text_response[:200] + "..." if len(text_response) > 200 else text_response,
            "Recommendations": ["Implement strategy A", "Review metric B", "Invest in C"],
            "Generated_At": "2025-03-31"  
        }

    def process_query(self, query):
        """Full workflow: preprocess, generate, call API, and postprocess."""
        query_info = self.preprocess_query(query)
        prompt = self.generate_prompt(query_info)
        raw_response = self.call_gemini_api(prompt)
        return self.postprocess_response(raw_response)

def evaluate_response(self, query, response):
    """Basic evaluation of response quality."""
    relevance = 1.0 if query.lower() in response.get("Summary", "").lower() else 0.5
    consistency = 1.0 if len(response["Recommendations"]) > 0 else 0.8
    return {"Relevance": relevance, "Consistency": consistency}


if __name__ == "__main__":
    
    API_KEY = "your_api_key_from_gemini"  
    
    assistant = BusinessInsightsAssistant(API_KEY)
    query = "How can we improve sales for Q4?"
    result = assistant.process_query(query)
    print(json.dumps(result, indent=2))
