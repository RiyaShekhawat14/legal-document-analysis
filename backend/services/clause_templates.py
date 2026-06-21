"""
Clause Templates Service
Provides standard, professionally-drafted clause templates for common scenarios.
"""


CLAUSE_TEMPLATES = {
    "Payment Terms": {
        "standard": """PAYMENT TERMS

The Vendor shall invoice the Client for services rendered. Payment shall be due within thirty (30) days of invoice date. 
Payment shall be made in USD to the account specified in the invoice.

The Client shall pay a late fee of 1.5% per month on any unpaid balance after the due date, or the maximum rate permitted 
by applicable law, whichever is lower.""",
        
        "pro_vendor": """PAYMENT TERMS

The Vendor shall invoice the Client immediately upon delivery of services. Payment shall be due within fifteen (15) days 
of invoice date. 

A late payment fee of 2% per month shall apply to any balance unpaid after the due date, plus all reasonable collection 
costs. The Client shall also pay interest at the maximum rate permitted by law.""",
        
        "pro_client": """PAYMENT TERMS

The Client shall make payment within forty-five (45) days of invoice receipt. Payment terms are net 45. 
No interest shall accrue on undisputed invoices during normal payment terms.

If payment cannot be made due to a legitimate dispute, the Client shall notify the Vendor in writing within five (5) 
business days of invoice receipt."""
    },

    "Termination": {
        "standard": """TERMINATION

Either party may terminate this Agreement with sixty (60) days written notice. 

If terminated for convenience, the terminating party shall pay:
• All undisputed fees for services rendered through termination date
• Reasonable costs to wind down services

Either party may terminate immediately if the other party materially breaches and fails to cure within thirty (30) days 
of written notice.""",
        
        "pro_vendor": """TERMINATION FOR CONVENIENCE

The Client may not terminate this Agreement for convenience. Early termination by Client constitutes a material breach 
and requires payment of:
• All remaining contract value
• Any associated penalties as outlined in the agreement

Vendor may terminate for Client breach after ten (10) days written notice if not cured.""",
        
        "pro_client": """TERMINATION FOR CONVENIENCE

Either party may terminate this Agreement at will with thirty (30) days written notice. 

Terminating party shall pay only for services rendered through the termination date on a pro-rata basis. 
No penalties apply for termination without cause."""
    },

    "Confidentiality": {
        "standard": """CONFIDENTIALITY

Confidential Information includes all non-public information disclosed by one party to the other. Each party shall 
maintain confidentiality and not disclose to third parties without prior written consent.

Exceptions include information that: (a) is publicly available; (b) was independently developed; (c) was properly 
received from third parties; or (d) is required to be disclosed by law.

Confidentiality obligations survive termination of this Agreement for three (3) years.""",
        
        "pro_recipient": """CONFIDENTIALITY - LIMITED

Recipient may use Confidential Information solely to evaluate a potential business relationship. Recipient shall not 
disclose to any third party without prior written consent, except to employees and advisors with legitimate need.

All Confidential Information shall be returned or destroyed within thirty (30) days of request. Standard business 
information and general knowledge are excluded.""",
        
        "pro_discloser": """CONFIDENTIAL INFORMATION - PROTECTED

All Confidential Information is proprietary. Recipient shall: (a) maintain in strict confidence; (b) restrict access 
to need-to-know employees under confidentiality agreements; (c) implement reasonable safeguards; (d) not use except 
as expressly permitted.

Breach entitles Discloser to injunctive relief and damages. Confidentiality survives in perpetuity."""
    },

    "Liability": {
        "standard": """LIMITATION OF LIABILITY

Neither party shall be liable to the other for indirect, incidental, special, or consequential damages.

Each party's total liability shall not exceed the fees paid in the twelve (12) months preceding the claim or $10,000, 
whichever is greater.

These limitations apply except for gross negligence, willful misconduct, or breach of confidentiality.""",
        
        "pro_vendor": """LIMITATION OF LIABILITY

Vendor shall not be liable for:
• Loss of profits, revenue, data, or business opportunity
• Any indirect, incidental, special, consequential, or punitive damages
• Delays or failures in performance

Vendor's total liability is limited to fees paid in the preceding three (3) months. This applies regardless of the 
nature of the claim.""",
        
        "pro_client": """LIMITATION OF LIABILITY

Each party's liability is limited to direct damages actually caused, up to the total contract value. This cap does not 
apply to: (a) personal injury; (b) breach of confidentiality; (c) gross negligence; or (d) IP infringement.

Either party may seek injunctive relief for breaches."""
    },

    "Dispute Resolution": {
        "standard": """DISPUTE RESOLUTION

Before litigation, the parties agree to attempt resolution through good faith negotiation for thirty (30) days.

If unresolved, disputes shall be resolved through binding arbitration administered by [Arbitration Organization] 
under its rules. Arbitration shall be held in [Location]. Each party shall bear its own costs plus equal share of 
arbitrator fees.

This agreement is governed by the laws of [Jurisdiction], without regard to conflicts of law principles.""",
        
        "pro_vendor": """DISPUTE RESOLUTION

Any disputes shall be resolved exclusively through binding arbitration. Arbitration shall be handled by a single 
arbitrator selected by Vendor.

The arbitrator's decision is final. Client waives the right to jury trial and class action. Client shall pay all 
arbitration fees if Client is not the prevailing party.

This agreement is governed by [Vendor's preferred jurisdiction].""",
        
        "pro_client": """DISPUTE RESOLUTION

Either party may pursue litigation in courts of [Client's location]. Binding arbitration is available only if both 
parties agree in writing.

The prevailing party in any legal proceeding shall recover reasonable attorneys' fees and costs."""
    },

    "Intellectual Property": {
        "standard": """INTELLECTUAL PROPERTY RIGHTS

Each party retains ownership of Intellectual Property created by it prior to this Agreement or outside the scope of 
this Agreement.

IP created specifically for Client under this Agreement shall be owned by Client upon full payment. Vendor retains 
rights to general methodologies and concepts.

Licenses granted herein are non-exclusive unless expressly stated as exclusive.""",
        
        "pro_vendor": """INTELLECTUAL PROPERTY RIGHTS

All work product, designs, and deliverables are Vendor's proprietary property. Client receives a non-exclusive, 
non-transferable license to use deliverables solely for Client's internal purposes.

Client may not modify, reverse-engineer, or create derivative works. All improvements and enhancements belong to Vendor.

Vendor may use Client's name in case studies and marketing materials.""",
        
        "pro_client": """INTELLECTUAL PROPERTY RIGHTS

All work created under this Agreement, including but not limited to deliverables, tools, and materials, shall be 
owned exclusively by Client. Client may use and modify freely without restrictions.

Vendor hereby assigns all IP rights to Client and shall execute any documents necessary to perfect Client's ownership."""
    },

    "Warranty": {
        "standard": """WARRANTIES

Vendor warrants that services shall be performed in a professional manner consistent with industry standards.

EXCEPT AS EXPRESSLY STATED, VENDOR MAKES NO OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF 
MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

If Vendor breaches a warranty, Client's sole remedy is re-performance of the services at no additional charge.""",
        
        "pro_vendor": """LIMITED WARRANTY

Vendor's sole warranty is that services shall be performed using industry-standard practices.

VENDOR DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS, AND NON-INFRINGEMENT. 
CLIENT ASSUMES ALL RISK.

In no event shall Vendor be liable for any warranty claim. Client's sole remedy is contract termination.""",
        
        "pro_client": """COMPREHENSIVE WARRANTY

Vendor warrants: (a) professional, timely performance; (b) compliance with applicable laws; (c) no infringement of 
third-party rights; (d) fitness for Client's stated purpose.

Vendor shall remedy any breach at no additional cost within thirty (30) days of notice. If not remedied, Client may 
terminate and receive a full refund."""
    },
}


def get_clause_template(clause_type: str, version: str = "standard") -> dict | None:
    """
    Get a clause template by type and version (standard, pro_vendor, pro_client).
    
    Args:
        clause_type: Type of clause (e.g., "Payment Terms")
        version: Template version - "standard", "pro_vendor", or "pro_client"
    
    Returns:
        Dict with template content or None if not found
    """
    if clause_type not in CLAUSE_TEMPLATES:
        return None
    
    templates = CLAUSE_TEMPLATES[clause_type]
    if version not in templates:
        version = "standard"
    
    return {
        "clause_type": clause_type,
        "version": version,
        "template": templates[version],
        "available_versions": list(templates.keys())
    }


def list_available_clause_types() -> list[str]:
    """Return list of available clause template types."""
    return list(CLAUSE_TEMPLATES.keys())


def get_all_clause_templates() -> dict:
    """Return all clause templates organized by type and version."""
    return CLAUSE_TEMPLATES


def compare_clause_versions(clause_type: str) -> dict:
    """Get all versions of a clause type for comparison."""
    if clause_type not in CLAUSE_TEMPLATES:
        return None
    
    templates = CLAUSE_TEMPLATES[clause_type]
    comparison = {}
    
    for version, template in templates.items():
        if version == "standard":
            favors = "Neutral"
        elif version in ("pro_vendor", "pro_discloser"):
            favors = "Vendor/Discloser"
        elif version in ("pro_client", "pro_recipient"):
            favors = "Client/Recipient"
        else:
            favors = version
        comparison[version] = {
            "template": template,
            "length": len(template),
            "favors": favors
        }
    
    return {
        "clause_type": clause_type,
        "comparison": comparison
    }
