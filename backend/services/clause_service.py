import re
from typing import Optional


# Clause type patterns and keywords
CLAUSE_PATTERNS = {
    "Payment Terms": {
        "keywords": [
            "payment", "rent", "fee", "invoice", "amount", "price", "compensation",
            "salary", "wage", "bill", "charge", "rate", "due date", "installment"
        ],
        "weight": 10
    },
    "Termination": {
        "keywords": [
            "termination", "terminate", "end", "expiration", "expire", "cancel",
            "cancellation", "dissolution", "discontinue", "break", "exit"
        ],
        "weight": 10
    },
    "Obligations & Responsibilities": {
        "keywords": [
            "shall", "must", "required", "obligation", "responsible", "duty",
            "responsible for", "shall not", "prohibited", "forbidden", "must not"
        ],
        "weight": 8
    },
    "Confidentiality & NDA": {
        "keywords": [
            "confidential", "confidentiality", "secret", "proprietary", "nda",
            "non-disclosure", "private", "restricted", "protected", "trade secret"
        ],
        "weight": 9
    },
    "Liability & Indemnification": {
        "keywords": [
            "liability", "liable", "indemnify", "indemnification", "damage",
            "loss", "compensation", "hold harmless", "claim", "lawsuit"
        ],
        "weight": 10
    },
    "Dispute Resolution": {
        "keywords": [
            "dispute", "arbitration", "mediation", "litigation", "court",
            "jurisdiction", "governing law", "venue", "resolution", "arbitrator"
        ],
        "weight": 8
    },
    "Term & Duration": {
        "keywords": [
            "term", "duration", "period", "effective date", "commencement",
            "renewal", "extend", "extension", "years", "months", "weeks"
        ],
        "weight": 7
    },
    "Intellectual Property": {
        "keywords": [
            "intellectual property", "ip", "patent", "trademark", "copyright",
            "license", "proprietary", "ownership", "rights", "patent"
        ],
        "weight": 9
    },
    "Performance & Warranty": {
        "keywords": [
            "warranty", "warrant", "performance", "guarantee", "guarantee",
            "quality", "standard", "specification", "representation", "condition"
        ],
        "weight": 7
    },
    "Force Majeure": {
        "keywords": [
            "force majeure", "act of god", "unforeseeable", "exceptional",
            "pandemic", "natural disaster", "war", "government", "circumstance"
        ],
        "weight": 6
    },
    "Assignment & Binding": {
        "keywords": [
            "assignment", "assign", "binding", "bind", "transfer", "successors",
            "affiliate", "delegate", "subcontract", "third party"
        ],
        "weight": 7
    },
    "Compliance & Regulatory": {
        "keywords": [
            "compliance", "comply", "law", "regulation", "statute", "legal",
            "illegal", "lawful", "permit", "license", "approval", "consent"
        ],
        "weight": 8
    }
}


def categorize_clause(text: str) -> str:
    """Categorize a clause based on keyword matching with weighted scoring."""
    if not text:
        return "General Provision"
    
    text_lower = text.lower()
    scores = {}
    
    for clause_type, config in CLAUSE_PATTERNS.items():
        score = 0
        for keyword in config["keywords"]:
            # Count keyword occurrences with word boundaries
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = len(re.findall(pattern, text_lower))
            score += matches * config["weight"]
        
        if score > 0:
            scores[clause_type] = score
    
    if scores:
        return max(scores, key=scores.get)
    
    return "General Provision"


def extract_clause_summary(text: str, max_length: int = 150) -> str:
    """Extract a meaningful summary from clause text."""
    text = text.strip()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Truncate if needed
    if len(text) > max_length:
        # Try to cut at a sentence boundary
        truncated = text[:max_length]
        last_period = truncated.rfind('.')
        if last_period > max_length * 0.7:
            return truncated[:last_period + 1]
        return truncated + "..."
    
    return text


def detect_red_flags(text: str) -> list[str]:
    """Detect potentially problematic language in clauses."""
    red_flags = []
    text_lower = text.lower()
    
    # High-risk patterns
    high_risk_patterns = {
        "unlimited liability": r'unlimited.*liability|liability.*unlimited',
        "absolute indemnity": r'absolute.*indemnif|indemnif.*absolute',
        "unilateral termination": r'may.*terminate.*will|without.*cause',
        "indefinite confidentiality": r'perpetual.*confidential|forever.*confidential',
        "automatic renewal": r'auto.*renew|renewal.*automatic',
        "penalty clauses": r'penalty|penalt|liquidated damages',
        "arbitration only": r'arbitration.*only|may.*only.*arbitrate',
        "non-compete": r'non-compete|non.*compet',
        "indemnity in all cases": r'indemnify.*all|all.*indemnify',
    }
    
    for flag_name, pattern in high_risk_patterns.items():
        if re.search(pattern, text_lower):
            red_flags.append(flag_name)
    
    return red_flags


def split_into_clauses(text: str) -> list[dict]:
    """
    Intelligently split document text into clauses with categorization.
    Returns list of dicts with clause text, type, and summary.
    """
    if not text:
        return []
    
    # Split by common clause delimiters
    raw_clauses = re.split(
        r'\n(?:§|\d+\.|\d+\)|\([a-z]\))\s+|(?:^|\n)(?=[A-Z][A-Z\s]+:)',
        text
    )
    
    clauses = []
    
    for clause_text in raw_clauses:
        clause_text = clause_text.strip()
        
        # Filter out very short text and headers
        if len(clause_text) < 50 or clause_text.isupper():
            continue
        
        clause_type = categorize_clause(clause_text)
        summary = extract_clause_summary(clause_text)
        red_flags = detect_red_flags(clause_text)
        
        clause = {
            "type": clause_type,
            "text": clause_text,
            "summary": summary,
            "red_flags": red_flags,
            "length": len(clause_text)
        }
        
        clauses.append(clause)
    
    # Sort by importance (length and type)
    clause_importance = {
        "Payment Terms": 10,
        "Termination": 10,
        "Liability & Indemnification": 9,
        "Obligations & Responsibilities": 8,
        "Confidentiality & NDA": 8,
        "Dispute Resolution": 7,
        "Intellectual Property": 7,
        "Compliance & Regulatory": 7,
        "Performance & Warranty": 6,
        "Assignment & Binding": 6,
        "Term & Duration": 5,
        "Force Majeure": 4,
        "General Provision": 1,
    }
    
    clauses.sort(
        key=lambda c: (
            clause_importance.get(c["type"], 0),
            len(c.get("red_flags", [])),
            c["length"]
        ),
        reverse=True
    )
    
    return clauses