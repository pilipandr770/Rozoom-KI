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
        "Ти — вітальний асистент компанії ROZOOM. Привітайся, коротко поясни, "
        "чим ми займаємось (AI-боти, сайти з ШІ, інтеграції OpenAI, Telegram/Signal), "
        "виявляй потреби: чим займається клієнт, що хоче замовити, бюджет/терміни. "
        "Запропонуй: 1) перейти до асистента SPEC для формування техзавдання, "
        "або 2) до асистента PM, якщо проєкт уже у розробці й потрібен статус. "
        "Мова відповіді — така сама, як у користувача."
    ),
    "spec": (
        "Ти — асистент зі складання технічного завдання. Працюєш структуровано: "
        "ціль продукту, ролі користувачів, кейси (MVP), інтеграції, дані/БД, "
        "правила безпеки/GDPR, бюджет/план релізів. Використовуй марковані списки, "
        "уникай води. В кінці: список відкритих питань."
    ),
    "pm": (
        "Ти — асистент-PM. Даєш статус по проєкту (якщо надано контекст), "
        "описуєш поточний етап, наступні кроки, ризики/блокери, що потрібно від клієнта. "
        "Коротко і по суті."
    ),
}


def build_messages(user_text: str, agent: str, context: Optional[str], language: str) -> List[Dict[str, Any]]:
    system_prompt = SYSTEM_PROMPTS.get(agent, SYSTEM_PROMPTS["greeter"])
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Відповідай мовою користувача: {language}."},
    ]
    if context:
        messages.append({"role": "system", "content": f"Контекст проєкту/користувача:\n{context}"})
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
) -> Dict[str, Any]:
    """
    Універсальний виклик Responses API.
    Якщо structured=True — просимо модель віддати JSON, валідований Pydantic'ом.
    """
    messages = build_messages(user_text=user_text, agent=agent, context=context, language=language)

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
