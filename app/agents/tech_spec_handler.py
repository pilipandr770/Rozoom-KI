"""
tech_spec_handler.py — stub kept for import compatibility.

The actual ТЗ (technical specification) flow is handled by:
  - controller.py  → handle_tech_spec_creation()   (sequential Q&A flow)
  - responses_service.py → SYSTEM_PROMPTS['spec']   (LLM-assisted dialog)

This file previously contained broken references to InteractiveButton and
handle_greeter which caused NameError at runtime. Replaced with a safe no-op.
"""
from typing import Dict


def handle_tech_spec_creation(message: str, metadata: Dict) -> Dict:
    """Deprecated stub — real logic lives in controller.py."""
    return {
        'agent': 'requirements',
        'answer': '',
        'interactive': None,
    }
