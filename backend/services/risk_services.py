from ml.inference import predict_risk


def analyze_document_risk(clauses: list) -> dict:
    results = []
    high_risk_count = 0

    for clause in clauses:
        text = clause.get("text", "")
        clause_type = clause.get("type", "Unknown")

        prediction = predict_risk(text)

        if prediction["risk"] == "High Risk":
            high_risk_count += 1

        results.append({
            "clause_type": clause_type,
            "risk": prediction["risk"],
            "confidence": prediction["confidence"]
        })

    if high_risk_count >= 2:
        overall_risk = "High Risk"
    elif high_risk_count == 1:
        overall_risk = "Medium Risk"
    else:
        overall_risk = "Low Risk"

    return {
        "overall_risk": overall_risk,
        "clauses": results
    }