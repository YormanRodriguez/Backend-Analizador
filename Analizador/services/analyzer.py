from radon.complexity import cc_visit
from radon.metrics import mi_visit

def analyze_code(code: str):
    try:
        complexity_results = cc_visit(code)
        complexity_score = sum([item.complexity for item in complexity_results]) / len(complexity_results) if complexity_results else 0
        maintainability_score = mi_visit(code, True)
        return {
            "complexity": round(complexity_score, 2),
            "maintainability": round(maintainability_score, 2)
        }
    except Exception:
        return {
            "complexity": 0.0,
            "maintainability": 0.0
        }
