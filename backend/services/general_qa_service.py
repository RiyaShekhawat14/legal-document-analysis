"""
General Legal Q&A Service
Provides answers to common legal questions without requiring a document.
"""

from config.settings import settings


# Common legal questions database with structured answers
LEGAL_KNOWLEDGE_BASE = {
    "termination": {
        "keywords": ["terminate", "termination", "end contract", "cancel", "dissolution"],
        "answers": [
            "Termination clauses typically specify notice periods, costs, and conditions.",
            "Most contracts require 30-90 days written notice for termination.",
            "Early termination often involves penalty fees or severance costs.",
            "Termination can be 'for cause' (breach) or 'for convenience' (without breach).",
            "Check your contract's termination section for specific requirements.",
        ]
    },
    "payment": {
        "keywords": ["payment", "invoice", "rent", "due date", "late payment", "fee"],
        "answers": [
            "Payment terms typically specify amount, due date, and late payment penalties.",
            "Most commercial agreements have monthly or quarterly payment schedules.",
            "Late payment often triggers interest charges and potential contract breach.",
            "Payment disputes should reference the exact clause numbers in your contract.",
            "Keep records of all payments and communications about payment issues.",
        ]
    },
    "liability": {
        "keywords": ["liable", "liability", "damage", "responsible", "indemnity"],
        "answers": [
            "Liability clauses define who is responsible for damages or losses.",
            "Caps on liability limit the amount you can claim or be liable for.",
            "Unlimited liability can be risky and should be carefully reviewed.",
            "Indemnification clauses require one party to cover losses of another.",
            "Insurance requirements are often tied to liability provisions.",
        ]
    },
    "confidentiality": {
        "keywords": ["confidential", "nda", "non-disclosure", "secret", "proprietary"],
        "answers": [
            "NDAs protect sensitive business information from being shared.",
            "Confidentiality obligations usually survive contract termination.",
            "Breaches of confidentiality can result in legal action and damages.",
            "Standard exceptions include information that is public or independently developed.",
            "Duration of confidentiality varies (often 2-5 years or indefinitely).",
        ]
    },
    "dispute": {
        "keywords": ["dispute", "arbitration", "mediation", "litigation", "court"],
        "answers": [
            "Dispute resolution clauses specify how disagreements will be handled.",
            "Arbitration is often faster and more private than court litigation.",
            "Mediation attempts to resolve disputes before formal proceedings.",
            "Jurisdiction and venue determine which court would hear the case.",
            "Legal fees and arbitration costs should be addressed in the clause.",
        ]
    },
    "breach": {
        "keywords": ["breach", "default", "violation", "non-compliance", "fail"],
        "answers": [
            "A material breach typically requires notice and opportunity to cure (fix).",
            "Most contracts provide 10-30 days to fix a breach after notice.",
            "Remedies for breach include termination, damages, or specific performance.",
            "Keep documentation of any breaches in writing with dates and details.",
            "Some breaches allow immediate termination without cure period.",
        ]
    },
    "renewal": {
        "keywords": ["renewal", "extend", "extension", "term", "continue"],
        "answers": [
            "Renewal options allow parties to extend contracts for additional terms.",
            "Notice requirements (often 90+ days) must be met to exercise renewal.",
            "Auto-renewal clauses automatically extend unless notice is given.",
            "Terms of renewal should be clearly specified (same or different terms).",
            "Missing renewal deadlines can result in contract termination.",
        ]
    },
    "ip": {
        "keywords": ["intellectual property", "patent", "trademark", "copyright", "license"],
        "answers": [
            "IP clauses define ownership of created work, inventions, or designs.",
            "Licenses grant permission to use intellectual property under conditions.",
            "Work-for-hire arrangements often assign IP to the employer/client.",
            "Royalties may be required when IP is used commercially.",
            "IP protection typically includes registration and enforcement rights.",
        ]
    },
    "warranty": {
        "keywords": ["warranty", "guarantee", "performance", "quality", "standard"],
        "answers": [
            "Warranties are promises about quality, performance, or fitness.",
            "Express warranties are explicitly stated; implied warranties are assumed.",
            "Warranty disclaimers can limit or eliminate warranty protection.",
            "Warranty periods specify how long the warranty covers the product/service.",
            "Warranty breaches typically require notice and opportunity to remedy.",
        ]
    },
    "force_majeure": {
        "keywords": ["force majeure", "act of god", "unforeseeable", "pandemic", "disaster"],
        "answers": [
            "Force majeure clauses excuse performance due to unforeseeable events.",
            "Covered events typically include natural disasters, wars, and pandemics.",
            "Party experiencing force majeure must notify the other party promptly.",
            "Performance obligations are suspended, not eliminated, during force majeure.",
            "Contract may be terminated if force majeure event is prolonged.",
        ]
    },
}


def match_question_to_category(question: str) -> tuple[str, list[str]] | None:
    """
    Match user question to legal category and return relevant answers.
    Returns (category, answers) tuple or None if no match found.
    """
    question_lower = question.lower()
    
    for category, info in LEGAL_KNOWLEDGE_BASE.items():
        for keyword in info["keywords"]:
            if keyword in question_lower:
                return category, info["answers"]
    
    return None


def generate_general_legal_advice(question: str) -> dict:
    """
    Generate structured advice for general legal questions.
    """
    match = match_question_to_category(question)
    
    if match:
        category, answers = match
        answer_text = "\n\n".join([f"• {answer}" for answer in answers])
    else:
        # Fallback for unmatched questions
        answer_text = (
            "I don't have specific guidance on this topic. Here are general recommendations:\n\n"
            "• Consult the full contract text for applicable clauses\n"
            "• Consider your specific situation and circumstances\n"
            "• When in doubt, seek advice from a legal professional\n"
            "• Document all communications and actions in writing\n"
            "• Review relevant state or local laws that may apply"
        )
    
    return {
        "answer": answer_text,
        "mode": "general_legal_qa",
        "used_context_chunks": 0,
    }


def is_general_legal_question(question: str) -> bool:
    """Determine if a question is about general legal knowledge vs. a specific document."""
    general_indicators = [
        "generally", "usually", "typically", "what is", "what are", "how do",
        "can i", "should i", "what should", "common", "standard", "normal",
        "example", "explain", "define", "meaning", "help me understand"
    ]
    
    question_lower = question.lower()
    return any(indicator in question_lower for indicator in general_indicators)
