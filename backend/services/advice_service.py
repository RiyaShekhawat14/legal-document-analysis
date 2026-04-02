def generate_advice(risk_level):
    if risk_level == "High Risk":
        return "This document contains high risk clauses. Review carefully before signing."
    elif risk_level == "Medium Risk":
        return "This document has moderate risk. Consider reviewing important clauses."
    else:
        return "This document appears low risk."