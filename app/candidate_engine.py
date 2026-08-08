import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CANDIDATES_FILE = BASE_DIR / "data" / "candidates.json"


def load_candidates():
    with open(CANDIDATES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["candidates"]


def find_candidate(candidate_id):
    candidates = load_candidates()

    for candidate in candidates:
        if candidate["member"]["id"] == candidate_id:
            return candidate

    return None


def build_candidate_profile(candidate_id):
    candidate = find_candidate(candidate_id)

    if candidate is None:
        return None

    member = candidate["member"]
    missions = candidate["missions"]
    signals = candidate["signals"]

    strengths = [
        mission["title"]
        for mission in missions
        if mission.get("passed") is True
    ]

    gaps = [
        mission["title"]
        for mission in missions
        if mission.get("passed") is False or mission.get("skipped") is True
    ]

    return {
        "id": member["id"],
        "name": member["name"],
        "jobRole": member["jobRole"],
        "yearsExperience": member["yearsExperience"],
        "education": member["education"],
        "status": member["status"],
        "strengths": strengths,
        "gaps": gaps,
        "signals": signals
    }

''' Testing '''

"""if __name__ == "__main__":
    profile = build_candidate_profile("CAND-003")
    print(profile)
"""
