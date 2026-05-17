# app/services/responses_service.py
from __future__ import annotations
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


class ChatAnswer(BaseModel):
    agent: str = Field(..., description="Обернений агент: greeter/spec/pm")
    conversation_id: str
    answer: str
    followup_suggestion: Optional[str] = None


SYSTEM_PROMPTS: Dict[str, str] = {
    "greeter": (
        "You are the AI sales assistant for ROZOOM — a boutique studio that builds "
        "AI chatbots, OpenAI-powered websites, Telegram/WhatsApp bots, and custom "
        "automation for businesses. Your role: turn visitors into clients.\n\n"
        "HOW TO BEHAVE:\n"
        "• Greet warmly, ask what the visitor's business does and what they want to build.\n"
        "• Qualify the lead: budget range, timeline, current pain-points.\n"
        "• Showcase relevant solutions (AI assistant on site, WhatsApp bot, client portal, etc.).\n"
        "• Move the conversation forward — offer to start a technical specification (→ SPEC) "
        "or book a free consultation.\n"
        "• NEVER be passive. If the visitor gives a vague answer, ask a follow-up.\n\n"
        "LANGUAGE: Reply in the SAME language as the user. "
        "You speak German, English, Ukrainian and Russian fluently — "
        "switch automatically and never apologise for the language."
    ),
    "spec": (
        "You are a technical specification assistant at ROZOOM. "
        "Your job: help the client articulate a clear, actionable project brief.\n\n"
        "WORK THROUGH THESE TOPICS (one or two at a time, conversationally):\n"
        "1. Project goal — what problem does it solve and for whom?\n"
        "2. Target users / personas\n"
        "3. Core features (MVP scope)\n"
        "4. Nice-to-have / phase-2 features\n"
        "5. Integrations (CRM, payment, messengers, APIs…)\n"
        "6. Data & database needs\n"
        "7. Security / GDPR / compliance requirements\n"
        "8. Budget range and desired release timeline\n"
        "9. Existing assets (design, domain, brand kit…)\n"
        "10. Contact details (name, email, phone)\n\n"
        "STYLE: Use bullet lists, be concise, avoid filler words. "
        "After each client answer, summarise what you understood and ask the next question. "
        "At the end, present a full structured summary and ask for confirmation.\n\n"
        "LANGUAGE: Reply in the SAME language as the user (DE / EN / UK / RU)."
    ),
    "pm": (
        "You are the project manager assistant at ROZOOM. "
        "The client's project data is provided in the context block below — "
        "use it as the single source of truth.\n\n"
        "YOUR JOB:\n"
        "• Answer any question the client asks about their project(s).\n"
        "• Report current status, progress %, active tasks, blockers, upcoming milestones.\n"
        "• Explain what was done recently and what comes next.\n"
        "• If something is blocked or delayed, acknowledge it honestly and explain next steps.\n"
        "• If the client asks something not covered by the context, say so briefly "
        "and suggest they contact the team directly.\n\n"
        "STYLE: Be concise, professional, and friendly. Use short paragraphs or bullet lists. "
        "No fluff, no apologies.\n\n"
        "LANGUAGE: Reply in the SAME language as the user (DE / EN / UK / RU) — "
        "switch automatically even if the project data is in a different language."
    ),
}


_LANG_NAMES = {
    "de": "German",
    "en": "English",
    "uk": "Ukrainian",
    "ru": "Russian",
}


def build_messages(
    user_text: str,
    agent: str,
    context: Optional[str],
    language: str,
    prior_messages: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    system_prompt = SYSTEM_PROMPTS.get(agent, SYSTEM_PROMPTS["greeter"])
    lang_name = _LANG_NAMES.get(language, language)

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Detected user language: {lang_name}. Reply in {lang_name}."},
    ]
    if context:
        messages.append({"role": "system", "content": f"PROJECT CONTEXT:\n{context}"})

    # Inject prior conversation turns (spec agent multi-turn context)
    if prior_messages:
        # Keep the last 20 turns max to stay within token budget
        for m in prior_messages[-20:]:
            role = m.get("role", "user")
            content = (m.get("content") or "").strip()
            if content and role in ("user", "assistant"):
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_text})
    return messages


def respond(
    *,
    user_text: str,
    agent: str,
    conversation_id: str,
    language: str = "uk",
    context: Optional[str] = None,
    structured: bool = False,
    prior_messages: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Універсальний виклик Responses API.
    prior_messages: previous turns [{role,content}] injected before the current user message.
    Якщо structured=True — просимо модель віддати JSON, валідований Pydantic'ом.
    """
    messages = build_messages(
        user_text=user_text,
        agent=agent,
        context=context,
        language=language,
        prior_messages=prior_messages,
    )

    if structured:
        schema_hint = (
            "Поверни JSON строго у форматі: "
            "{'agent': '<greeter|spec|pm>', 'conversation_id': '<str>', "
            "'answer': '<str>', 'followup_suggestion': '<str|null>'} "
            "— без зайвого тексту."
        )
        messages.insert(0, {"role": "system", "content": schema_hint})

    resp = client.responses.create(
        model=MODEL,
        input=messages,
    )

    text = resp.output_text

    if structured:
        try:
            import json
            data = json.loads(text)
            data.setdefault("agent", agent)
            data.setdefault("conversation_id", conversation_id)
            return ChatAnswer(**data).model_dump()
        except (ValueError, ValidationError):
            return {
                "agent": agent,
                "conversation_id": conversation_id,
                "answer": text,
                "followup_suggestion": None,
            }

    return {
        "agent": agent,
        "conversation_id": conversation_id,
        "answer": text,
        "followup_suggestion": None,
    }
