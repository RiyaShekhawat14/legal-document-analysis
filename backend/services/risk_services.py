from ml.inference import predict_risk


def analyze_document_risk(clauses: list) -> dict:
    """
    Analyze risk level for each clause and overall document.
    Returns comprehensive risk analysis with red flags.
    """
    results = []
    high_risk_count = 0
    medium_risk_count = 0
    total_red_flags = []

    for clause in clauses:
        text = clause.get("text", "")
        clause_type = clause.get("type", "Unknown")
        red_flags = clause.get("red_flags", [])

        prediction = predict_risk(text)

        if prediction["risk"] == "High Risk":
            high_risk_count += 1
        elif prediction["risk"] == "Medium Risk":
            medium_risk_count += 1

        total_red_flags.extend(red_flags)

        results.append({
            "clause_type": clause_type,
            "risk": prediction["risk"],
            "confidence": prediction["confidence"],
            "red_flags": red_flags,
            "summary": clause.get("summary", ""),
        })

    # Calculate overall risk
    if high_risk_count >= 3 or (high_risk_count >= 2 and len(total_red_flags) > 3):
        overall_risk = "High Risk"
    elif high_risk_count >= 1 or medium_risk_count >= 2:
        overall_risk = "Medium Risk"
    else:
        overall_risk = "Low Risk"

    return {
        "overall_risk": overall_risk,
        "clauses": results,
        "statistics": {
            "total_clauses": len(clauses),
            "high_risk_clauses": high_risk_count,
            "medium_risk_clauses": medium_risk_count,
            "total_red_flags": len(set(total_red_flags)),
            "critical_issues": list(set([flag for flags in [r.get("red_flags", []) for r in results] for flag in flags]))
        }
    }