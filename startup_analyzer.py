# fixed_analyzer.py
import PyPDF2
import re
import json
import requests
import os
from typing import Dict, List

class StartupAnalyzerOllama:
    def __init__(self, ollama_base_url: str = "http://localhost:11434"):
        self.base_url = ollama_base_url
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def call_ollama(self, prompt: str, model: str = "tinyllama:latest") -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 1000}
        }
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except requests.exceptions.Timeout:
            print("⏱️  Timeout")
            return ""
        except Exception as e:
            print(f"🤖 Error: {e}")
            return ""
    
    def analyze_startup_text(self, startup_text: str) -> Dict:
        prompt = f"""Analyze this startup and return JSON:
        {{
            "problem": "description",
            "solution": "description",
            "target_market": "description",
            "score": 0
        }}
        Startup: {startup_text}
        JSON:"""
        
        response = self.call_ollama(prompt)
        
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response
            return json.loads(json_str)
        except:
            return self.fallback_analysis(startup_text)
    
    def fallback_analysis(self, text: str) -> Dict:
        return {
            "problem": "Not detected",
            "solution": "Automation platform" if "automate" in text.lower() else "Not detected",
            "target_market": "Healthcare clinics" if any(x in text.lower() for x in ["clinic", "patient"]) else "Not detected",
            "score": 5
        }
    
    def analyze_pitch_deck(self, pdf_path: str) -> Dict:
        print(f"📄 Analyzing: {pdf_path}")
        text = self.extract_text_from_pdf(pdf_path)
        print(f"✅ Extracted {len(text)} chars")
        
        print("🤖 AI analyzing...")
        analysis = self.analyze_startup_text(text[:2000])
        
        metrics = {
            "revenue": self.find_pattern(text, r'revenue.*?(\$?[0-9,.]+[MK]?)'),
            "burn_rate": self.find_pattern(text, r'burn.*?rate.*?(\$?[0-9,.]+[MK]?/month)'),
            "team_size": self.find_pattern(text, r'team.*?of.*?(\d+)'),
            "funding": self.find_pattern(text, r'raising.*?(\$?[0-9,.]+[MK]?)')
        }
        
        return {
            "analysis": analysis,
            "metrics": metrics,
            "preview": text[:300]
        }
    
    def find_pattern(self, text: str, pattern: str) -> str:
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else "Not found"

if __name__ == "__main__":
    analyzer = StartupAnalyzerOllama()
    
    test_text = "AI scheduling for clinics. $150K revenue. 5 people team."
    print("🧪 Test analysis:", analyzer.analyze_startup_text(test_text))
    
    if os.path.exists("sample_pitch.pdf"):
        result = analyzer.analyze_pitch_deck("sample_pitch.pdf")
        print(json.dumps(result, indent=2))