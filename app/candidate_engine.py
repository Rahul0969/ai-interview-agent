import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CANDIDATES_FILE = BASE_DIR / "data" / "candidates.json"

def load_candidates():
    with open(CANDIDATES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("candidates", [])

def find_candidate(candidate_id):
    candidates = load_candidates()

    for candidate in candidates:
        member = candidate.get("member", {})

        if member.get("id") == candidate_id:
            return candidate

    return None

def build_candidate_profile(candidate_id):
    candidate = find_candidate(candidate_id)

    if candidate is None:
        return None

    member = candidate.get("member", {})
    missions = candidate.get("missions", [])
    signals = candidate.get("signals", [])

    strengths = [
        mission.get("title")
        for mission in missions
        if mission.get("passed") is True
    ]

    gaps = [
        mission.get("title")
        for mission in missions
        if mission.get("passed") is False
        or mission.get("skipped") is True
    ]

    return {
        "id": member.get("id"),
        "name": member.get("name"),
        "jobRole": member.get("jobRole"),
        "yearsExperience": member.get("yearsExperience"),
        "education": member.get("education"),
        "status": member.get("status"),
        "strengths": strengths,
        "gaps": gaps,
        "signals": signals
    }

''' Testing '''

"""if __name__ == "__main__":
    profile = build_candidate_profile("CAND-003")
    print(profile)
"""
