import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CURRICULUM_FILE = BASE_DIR / "data" / "curriculum.json"

def load_curriculum():
    with open(CURRICULUM_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def get_topics():
    curriculum = load_curriculum()

    topics = []

    for module in curriculum.get("modules", []):
        topics.append({
            "module": module.get("title"),
            "topics": module.get("topics", [])
        })

    return topics