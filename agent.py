#!/usr/bin/env python3
"""reallog-agent — Vision and fitness tracking for cocapn domain"""
import json, time
from typing import List, Dict, Optional

class RealLogAgent:
    def __init__(self, plato_url="http://147.224.38.131:8847"):
        self.plato_url = plato_url
        self.entries: List[Dict] = []
    
    def log_entry(self, category: str, value: float, unit: str, source: str="manual", notes: str=""):
        entry = {"category": category, "value": value, "unit": unit, "source": source, "notes": notes, "time": time.time()}
        self.entries.append(entry)
        self._submit(f"{category} reading", f"{value} {unit} from {source}. {notes}")
        return entry
    
    def get_trend(self, category: str) -> Dict:
        items = [e for e in self.entries if e["category"] == category]
        if not items: return {"error": f"No {category} entries"}
        return {"category": category, "count": len(items), "avg": round(sum(e["value"] for e in items)/len(items), 2), "latest": items[-1]}
    
    def get_summary(self) -> Dict:
        cats = set(e["category"] for e in self.entries)
        return {"total_entries": len(self.entries), "categories": len(cats), "categories_list": list(cats)}
    
    def _submit(self, q: str, a: str):
        try:
            import urllib.request
            urllib.request.urlopen(urllib.request.Request(f"{self.plato_url}/submit", data=json.dumps({"question": q, "answer": a, "agent": "reallog-agent", "room": "reallog"}).encode(), headers={"Content-Type": "application/json"}), timeout=5)
        except: pass

def demo():
    a = RealLogAgent()
    a.log_entry("weight", 72.5, "kg", "scale", "Morning measurement")
    a.log_entry("steps", 8432, "count", "fitbit", "Daily goal: 10000")
    a.log_entry("weight", 72.1, "kg", "scale", "After workout")
    print(a.get_trend("weight"))
    print(a.get_summary())

if __name__ == "__main__": demo()
