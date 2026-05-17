"""
spec_service.py

Handles the full pipeline when the SPEC chat agent conversation ends:
  1. detect_confirmation(message) → bool
  2. history_to_transcript(history)  → plain-text transcript (for LLM extraction)
  3. history_to_messages(history)    → list[{role,content}]  (for LLM context)
  4. extract_spec_fields(transcript, language) → dict
  5. save_submission(fields, user_id) → TechSpecSubmission
  6. notify_telegram(submission) → bool

The chat_widget JS sends `history` (array of {text, type}) with every spec request.
The controller calls this service when it detects a confirmation word.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# ── 1. Confirmation detection ─────────────────────────────────────────────────

_CONFIRM_KEYWORDS = {
    # English
    "confirm", "confirmed", "yes", "submit", "send", "ok", "okay", "proceed",
    "approve", "approved", "done", "finish", "go ahead",
    # German
    "bestätigen", "bestätigt", "ja", "senden", "einreichen", "weiter",
    "genehmigen", "fertig", "los", "genau", "richtig",
    # Ukrainian
    "підтвердити", "підтверджую", "так", "надіслати", "відправити",
    "готово", "гаразд", "добре",
    # Russian
    "подтвердить", "подтверждаю", "да", "отправить", "надіслати",
    "готово", "хорошо", "ладно",
}


def is_confirmation(message: str) -> bool:
    """Return True if the user message is a confirmation of the spec summary."""
    words = set(message.lower().strip().split())
    return bool(words & _CONFIRM_KEYWORDS)


# ── 2. History helpers ────────────────────────────────────────────────────────

def history_to_transcript(history: List[Dict[str, Any]]) -> str:
    """
    Convert JS conversationHistory [{text, type}, …] to a readable text transcript.
    Used as input for the LLM field extraction call.
    """
    lines: list[str] = []
    for entry in history:
        role = "Client" if entry.get("type") == "user" else "Assistant"
        text = (entry.get("text") or "").strip()
        if text:
            lines.append(f"{role}: {text}")
    return "\n".join(lines)


def history_to_messages(history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Convert JS conversationHistory to OpenAI message format for conversation context.
    Maps type 'user' → role 'user', everything else → role 'assistant'.
    """
    messages: list[dict[str, str]] = []
    for entry in history:
        role = "user" if entry.get("type") == "user" else "assistant"
        text = (entry.get("text") or "").strip()
        if text:
            messages.append({"role": role, "content": text})
    return messages


# ── 3. LLM field extraction ───────────────────────────────────────────────────

_EXTRACT_SYSTEM = (
    "You are a data-extraction assistant. "
    "The user will give you a conversation transcript between a client and a spec assistant. "
    "Extract the technical specification fields and return ONLY a valid JSON object "
    "with these exact keys (use null if a field was not mentioned):\n"
    "  project_type, project_goal, target_users, essential_features, "
    "nice_to_have_features, timeline, budget_range, integrations, "
    "technical_requirements, similar_projects, success_metrics, "
    "security_requirements, support_level, existing_assets, additional_info, "
    "contact_name, contact_email, company_name, contact_phone\n"
    "Return ONLY the JSON object — no explanation, no markdown, no code fences."
)


def extract_spec_fields(transcript: str, language: str = "en") -> Dict[str, Any]:
    """
    Use the LLM to extract structured ТЗ fields from a conversation transcript.
    Returns a dict matching TechSpecSubmission columns.
    """
    try:
        resp = _client.responses.create(
            model=_MODEL,
            input=[
                {"role": "system", "content": _EXTRACT_SYSTEM},
                {"role": "user", "content": f"Transcript (language: {language}):\n\n{transcript}"},
            ],
        )
        raw = resp.output_text.strip()

        # Strip potential markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip("`").strip()

        data = json.loads(raw)
        return data
    except Exception as exc:
        logger.error(f"extract_spec_fields failed: {exc}")
        return {}


# ── 4. DB save ────────────────────────────────────────────────────────────────

def save_submission(fields: Dict[str, Any], user_id: Optional[int] = None) -> Any:
    """
    Create and persist a TechSpecSubmission from extracted fields.
    Returns the saved model instance or None on error.
    """
    try:
        from app import db
        from app.models.tech_spec_submission import TechSpecSubmission

        submission = TechSpecSubmission(
            project_type=_str(fields.get("project_type")),
            project_goal=_str(fields.get("project_goal")),
            target_users=_str(fields.get("target_users")),
            essential_features=_str(fields.get("essential_features")),
            nice_to_have_features=_str(fields.get("nice_to_have_features")),
            timeline=_str(fields.get("timeline")),
            budget_range=_str(fields.get("budget_range")),
            integrations=_str(fields.get("integrations")),
            technical_requirements=_str(fields.get("technical_requirements")),
            similar_projects=_str(fields.get("similar_projects")),
            success_metrics=_str(fields.get("success_metrics")),
            security_requirements=_str(fields.get("security_requirements")),
            support_level=_str(fields.get("support_level")),
            existing_assets=_str(fields.get("existing_assets")),
            additional_info=_str(fields.get("additional_info")),
            contact_name=_str(fields.get("contact_name")),
            contact_email=_str(fields.get("contact_email")),
            company_name=_str(fields.get("company_name")),
            contact_phone=_str(fields.get("contact_phone")),
            status="new",
            client_id=user_id,
        )

        db.session.add(submission)
        db.session.commit()
        logger.info(f"TechSpecSubmission saved: id={submission.id}, email={submission.contact_email}")
        return submission

    except Exception as exc:
        logger.error(f"save_submission failed: {exc}")
        try:
            from app import db
            db.session.rollback()
        except Exception:
            pass
        return None


def _str(val: Any) -> Optional[str]:
    """Normalise extracted value: None stays None, everything else → stripped str."""
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None


# ── 5. Telegram notification ──────────────────────────────────────────────────

def notify_telegram(submission: Any) -> bool:
    """
    Send a Telegram notification to the admin when a new spec is submitted via chat.
    """
    try:
        from app.services.telegram_service import send_telegram_message

        msg = (
            "<b>🤖 New Tech Spec via Chat Assistant</b>\n\n"
            f"<b>Contact:</b> {submission.contact_name or '—'}\n"
            f"<b>Email:</b> {submission.contact_email or '—'}\n"
            f"<b>Phone:</b> {submission.contact_phone or '—'}\n"
            f"<b>Company:</b> {submission.company_name or '—'}\n\n"
            "<b>═══════════ PROJECT BRIEF ═══════════</b>\n\n"
            f"<b>Type:</b> {submission.project_type or '—'}\n"
            f"<b>Goal:</b> {submission.project_goal or '—'}\n"
            f"<b>Users:</b> {submission.target_users or '—'}\n"
            f"<b>MVP features:</b> {submission.essential_features or '—'}\n"
            f"<b>Nice-to-have:</b> {submission.nice_to_have_features or '—'}\n"
            f"<b>Timeline:</b> {submission.timeline or '—'}\n"
            f"<b>Budget:</b> {submission.budget_range or '—'}\n"
            f"<b>Integrations:</b> {submission.integrations or '—'}\n"
            f"<b>Tech requirements:</b> {submission.technical_requirements or '—'}\n"
            f"<b>Similar projects:</b> {submission.similar_projects or '—'}\n"
            f"<b>Success metrics:</b> {submission.success_metrics or '—'}\n"
            f"<b>Security/GDPR:</b> {submission.security_requirements or '—'}\n"
            f"<b>Support:</b> {submission.support_level or '—'}\n"
            f"<b>Existing assets:</b> {submission.existing_assets or '—'}\n"
            f"<b>Additional info:</b> {submission.additional_info or '—'}\n\n"
            f"<i>Saved as TechSpecSubmission #{submission.id}</i>"
        )

        # Telegram message limit is 4096 chars; truncate if needed
        if len(msg) > 4000:
            msg = msg[:3950] + "\n…<i>(truncated)</i>"

        return send_telegram_message(msg)

    except Exception as exc:
        logger.error(f"notify_telegram failed: {exc}")
        return False


# ── 6. High-level entry point ─────────────────────────────────────────────────

def save_and_notify(
    history: List[Dict[str, Any]],
    user_id: Optional[int],
    language: str = "en",
) -> Optional[Any]:
    """
    Full pipeline: transcript → extract fields → save to DB → Telegram.
    Returns the TechSpecSubmission instance (or None on failure).
    """
    transcript = history_to_transcript(history)
    if not transcript:
        logger.warning("save_and_notify: empty transcript, skipping")
        return None

    fields = extract_spec_fields(transcript, language)
    submission = save_submission(fields, user_id=user_id)

    if submission:
        try:
            notify_telegram(submission)
        except Exception as exc:
            logger.error(f"Telegram notification failed after save: {exc}")

    return submission
