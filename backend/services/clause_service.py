import re


def split_into_clauses(text: str) -> list:
    """
    Split document text into clauses
    """
    if not text:
        return []

    raw_clauses = re.split(r'\n\d+\.|\n[A-Z][A-Z\s]+\n', text)

    clauses = []

    for clause in raw_clauses:
        clause = clause.strip()

        if len(clause) < 40:
            continue

        clauses.append({
            "type": "General Clause",
            "text": clause
        })

    return clauses