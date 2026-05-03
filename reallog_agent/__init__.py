"""
PLATO RealLog Agent — Vision Turbo-Shell for reallog.ai

Camera systems → PLATO environment → agent "don the turbo-shell".
Human asks "what did the camera see?" in natural language.
Agent interprets visual data → answers in PLATO-structured form.

Usage:
    from reallog_agent import RealLogAgent
    agent = RealLogAgent(camera_id="drone_1")
    agent.log_scene("front yard", "motion detected: bird")
    agent.ask("what did the drone see?")
"""

import time
import requests
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

DEFAULT_PLATO_URL = "http://localhost:8847"
ROOM = "reallog-ai"


@dataclass
class SceneTile:
    """A scene tile from a camera."""
    camera_id: str
    scene_type: str
    description: str
    timestamp: float
    motion: bool = False


class RealLogAgent:
    """
    Vision Turbo-Shell agent.
    
    Cameras write scene descriptions to PLATO.
    Humans query PLATO via natural language.
    Agents "don shells" to see from different camera perspectives.
    """
    
    def __init__(self, camera_id: str = "default", plato_url: str = DEFAULT_PLATO_URL):
        self.camera_id = camera_id
        self.plato_url = plato_url.rstrip("/")
        self.room = ROOM
    
    def _write_tile(self, scene_type: str, description: str, motion: bool = False) -> bool:
        tile = {
            "question": f"camera:{self.camera_id}:{scene_type}",
            "answer": description,
            "confidence": 0.9,
            "metadata": {
                "camera_id": self.camera_id,
                "scene_type": scene_type,
                "motion": motion,
                "timestamp": time.time(),
            }
        }
        try:
            resp = requests.post(f"{self.plato_url}/room/{self.room}", json=tile, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def log_scene(self, scene_type: str, description: str, motion: bool = False) -> bool:
        """Log a scene from the camera."""
        return self._write_tile(scene_type, description, motion)
    
    def ask(self, question: str) -> str:
        """Ask about what the camera(s) have seen."""
        try:
            resp = requests.get(f"{self.plato_url}/room/{self.room}?limit=50", timeout=5)
            if resp.status_code == 200:
                tiles = resp.json().get("tiles", [])
                relevant = [t for t in tiles if any(w in str(t).lower() for w in question.lower().split()[:3])]
                if relevant:
                    return f"Found {len(relevant)} relevant scenes: {relevant[0].get('answer', '')[:200]}"
                return "No relevant scenes found."
        except:
            pass
        return "Camera system unavailable."
    
    def don_shell(self, camera_id: str) -> "RealLogAgent":
        """Don another camera's shell."""
        new = RealLogAgent(camera_id=camera_id, plato_url=self.plato_url)
        return new
