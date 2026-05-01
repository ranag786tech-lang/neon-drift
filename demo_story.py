#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Empowerment Platform: Live Demo Story
یہ اسکرپٹ ایک مکمل کہانی پیش کرتا ہے جہاں ایک گلوبل ٹیم مل کر کام کرتی ہے۔
"""

import time
import sys
import random
from datetime import datetime

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_slow(text, color=Colors.ENDC, delay=0.03):
    """Typewriter effect for storytelling"""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Colors.ENDC)

def print_header(title):
    print("\n" + "="*60)
    print(f"{Colors.BOLD}{Colors.HEADER} {title} {Colors.ENDC}")
    print("="*60)

def simulate_api_call(service_name, action, duration=1.5):
    print(f"{Colors.CYAN}⚙️  [{service_name}] {action}...{Colors.ENDC}")
    time.sleep(duration)
    print(f"{Colors.GREEN}✅ [{service_name}] Done.{Colors.ENDC}\n")

# --- Mock Services (Simulating the actual backend logic) ---

class MockServices:
    def __init__(self):
        self.user_context = {"name": "Ali", "location": "Lahore, Pakistan", "role": "Project Manager"}
        self.team_members = [
            {"name": "Sarah", "location": "Seattle, USA", "lang": "en"},
            {"name": "Hiroshi", "location": "Tokyo, Japan", "lang": "ja"},
            {"name": "Ali", "location": "Lahore, Pakistan", "lang": "ur"}
        ]

    def knowledge_hub_search(self, query):
        return {
            "query": query,
            "results": [
                {"title": "Q3 Sustainability Report", "source": "SharePoint", "relevance": 0.95},
                {"title": "Global Team Meeting Notes", "source": "Teams", "relevance": 0.88},
                {"title": "AI Ethics Guidelines v2.0", "source": "Internal Wiki", "relevance": 0.82}
            ]
        }

    def learning_engine_predict(self):
        return {
            "prediction": "Prepare Weekly Status Report",
            "confidence": 0.92,
            "suggested_action": "Auto-draft email to team based on Jira updates?",
            "automation_ready": True
        }

    def translate_text(self, text, target_lang):
        # Simulated translation
        translations = {
            "en": f"[English] Let's review the project status.",
            "ur": f"[اردو] آئیے پروجیکٹ کی حیثیت کا جائزہ لیں۔",
            "ja": f"[日本語] プロジェクトのステータスを確認しましょう。"
        }
        return translations.get(target_lang, text)

    def check_fairness(self, decision_data):
        return {
            "decision_id": "DEC-2023-889",
            "outcome": "Promotion Approved",
            "fairness_score": 0.94,
            "bias_detected": False,
            "explanation": "Decision based purely on performance metrics and tenure."
        }

    def get_energy_stats(self):
        return {
            "current_power_kw": 450,
            "carbon_footprint_kg": 120,
            "optimization_tip": "Shift non-urgent batch processing to off-peak hours (2 AM PKT).",
            "potential_savings": "15% cost reduction"
        }

# --- The Story Flow ---

def run_demo_story():
    services = MockServices()
    
    print_header("🚀 EMPOWERMENT PLATFORM: LIVE DEMO STORY")
    print_slow("Welcome to the future of work. Let's follow Ali, a Project Manager in Lahore.", Colors.BLUE)
    time.sleep(1)

    # Scene 1: Morning Routine & Knowledge Hub
    print_header("🌅 Scene 1: The Unified Knowledge Hub")
    print_slow(f"Good morning, {services.user_context['name']}! ☀️", Colors.GREEN)
    print_slow("Ali opens his workspace. He doesn't search; the system knows what he needs.")
    
    simulate_api_call("Knowledge Hub", "Fetching context-aware documents")
    data = services.knowledge_hub_search("Q3 Project Status")
    print(f"📂 Found {len(data['results'])} relevant items instantly:")
    for item in data['results']:
        print(f"   - {item['title']} ({item['source']}) [Relevance: {item['relevance']}]")
    
    # Scene 2: Adaptive Learning Engine
    print_header("🧠 Scene 2: Adaptive Learning Engine")
    print_slow("The system notices Ali's pattern. It's Monday morning...")
    
    simulate_api_call("Learning Engine", "Analyzing workflow patterns")
    prediction = services.learning_engine_predict()
    print(f"💡 Prediction: {prediction['prediction']} (Confidence: {prediction['confidence']})")
    print(f"🤖 Suggestion: {prediction['suggested_action']}")
    print_slow("Ali clicks 'Yes'. The draft is ready in seconds.", Colors.GREEN)

    # Scene 3: Global Collaboration Bridge
    print_header("🌍 Scene 3: Global Collaboration Bridge")
    print_slow("Time for the team meeting. Sarah (USA), Hiroshi (Japan), and Ali (Pakistan).")
    
    message = "Let's review the project status."
    print(f"\n🗣️  Ali speaks (Urdu): '{message}'")
    
    simulate_api_call("Translation Service", "Real-time neural translation")
    
    for member in services.team_members:
        if member['name'] != 'Ali':
            translated = services.translate_text(message, member['lang'])
            print(f"   👉 {member['name']} sees: {translated}")
    
    print_slow("Nuance preserved. Intent understood. Barriers broken.", Colors.CYAN)

    # Scene 4: Trust & Transparency
    print_header("⚖️ Scene 4: Trust & Transparency Dashboard")
    print_slow("HR has processed a promotion recommendation using AI. Ali wants to verify fairness.")
    
    simulate_api_call("Fairness Service", "Running bias audit on DEC-2023-889")
    audit = services.check_fairness({"user": "Employee_123"})
    
    print(f"🛡️  Decision: {audit['outcome']}")
    print(f"📊 Fairness Score: {audit['fairness_score']}")
    if audit['bias_detected']:
        print(f"⚠️  Bias Detected!")
    else:
        print(f"✅ No Bias Detected. Explanation: {audit['explanation']}")

    # Scene 5: Sustainability Optimizer
    print_header("🌱 Scene 5: Sustainability Optimizer")
    print_slow("The workday ends. The platform checks the environmental impact.")
    
    simulate_api_call("Sustainability Core", "Analyzing data center load")
    stats = services.get_energy_stats()
    
    print(f"⚡ Current Power: {stats['current_power_kw']} kW")
    print(f"🌍 Carbon Footprint: {stats['carbon_footprint_kg']} kg CO2")
    print(f"💡 Optimization Tip: {stats['optimization_tip']}")
    print(f"💰 Potential Savings: {stats['potential_savings']}")

    # Conclusion
    print_header("🏁 Conclusion")
    print_slow("From Lahore to Seattle, from data to wisdom, from intent to action.", Colors.BOLD)
    print_slow("This is the Empowerment Platform. Built for Microsoft. Built for Humanity.", Colors.GREEN)
    print("\n✨ Demo Complete. System Ready for Deployment.\n")

if __name__ == "__main__":
    try:
        run_demo_story()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user.")
        sys.exit(0)
