"""
project_manager_handler.py

Collects the authenticated client's project data from the DB,
builds a structured context string, and delegates the answer to
the LLM via responses_service.respond().  The LLM handles any
language (DE / EN / UK / RU) and any question the client may ask.
"""
from __future__ import annotations

from datetime import date
from typing import Dict, Any, Optional

from app import db
from app.models.project import Project, ProjectTask, ProjectUpdate
from app.models.base import User
from app.services.responses_service import respond as _llm_respond


# ── helpers ──────────────────────────────────────────────────────────────────

def _fmt_date(d) -> str:
    if d is None:
        return "—"
    if isinstance(d, date):
        return d.strftime("%d.%m.%Y")
    return str(d)


def _build_project_context(user: User) -> str:
    """
    Return a compact text block with all project data for this client.
    Injected as a system-level context message for the PM agent.
    """
    projects = Project.query.filter_by(client_id=user.id).all()

    if not projects:
        return (
            f"CLIENT: {user.name}\n"
            "STATUS: No active projects yet. The client may have submitted a "
            "technical specification that is being reviewed by the team."
        )

    lines: list[str] = [f"CLIENT: {user.name}  |  email: {user.email or '—'}\n"]

    for idx, proj in enumerate(projects, 1):
        tasks = ProjectTask.query.filter_by(project_id=proj.id).all()
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == "completed")
        in_progress_tasks = [t for t in tasks if t.status == "in_progress"]
        blocked_tasks = [t for t in tasks if t.status == "blocked"]

        updates = (
            ProjectUpdate.query
            .filter_by(project_id=proj.id)
            .order_by(ProjectUpdate.created_at.desc())
            .limit(5)
            .all()
        )

        lines.append(f"── PROJECT {idx}: {proj.title} ──")
        lines.append(f"Status   : {(proj.status or 'unknown').upper()}")
        lines.append(f"Progress : {proj.progress}%")
        lines.append(f"Start    : {_fmt_date(proj.start_date)}")
        lines.append(f"Deadline : {_fmt_date(proj.estimated_end_date)}")
        lines.append(f"Tasks    : {completed_tasks}/{total_tasks} completed")

        if proj.description:
            lines.append(f"Goal     : {proj.description[:200]}")

        # Current work
        if in_progress_tasks:
            lines.append("In progress:")
            for t in in_progress_tasks[:5]:
                lines.append(f"  • {t.title}" + (f": {t.description[:80]}" if t.description else ""))

        # Blockers
        if blocked_tasks:
            lines.append("⚠ Blocked:")
            for t in blocked_tasks[:3]:
                lines.append(f"  • {t.title}")

        # Recent updates
        if updates:
            lines.append("Recent updates:")
            for u in updates:
                milestone = " 🏆 MILESTONE" if u.is_milestone else ""
                lines.append(
                    f"  [{_fmt_date(u.created_at)}] {u.title}{milestone}"
                    + (f" — {u.content[:120]}" if u.content else "")
                )
        else:
            lines.append("Recent updates: none yet")

        lines.append("")  # blank line between projects

    return "\n".join(lines)


def _not_logged_in_msg(language: str) -> str:
    msgs = {
        "en": (
            "It looks like you're not logged in. Please log in to your client "
            "dashboard to check your project status."
        ),
        "de": (
            "Es scheint, dass Sie nicht angemeldet sind. Bitte melden Sie sich "
            "in Ihrem Kundenbereich an, um den Projektstatus zu sehen."
        ),
        "uk": (
            "Здається, ви не увійшли в систему. Будь ласка, увійдіть у свій "
            "кабінет, щоб перевірити статус проєкту."
        ),
        "ru": (
            "Похоже, вы не вошли в систему. Войдите в личный кабинет, "
            "чтобы проверить статус проекта."
        ),
    }
    return msgs.get(language, msgs["en"])


# ── public entry point ────────────────────────────────────────────────────────

def handle_pm_request(message: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Called by controller.route_and_respond() when agent == 'pm'.

    Returns:
        { 'agent': 'pm', 'answer': <str>, 'conversation_id': <str> }
    """
    language = metadata.get("language", "en")
    conversation_id = metadata.get("conversation_id", "anon")

    # ── auth guard ────────────────────────────────────────────────────────────
    user_id = metadata.get("user_id")
    user: Optional[User] = db.session.get(User, user_id) if user_id else None

    if not user:
        return {
            "agent": "pm",
            "answer": _not_logged_in_msg(language),
            "conversation_id": conversation_id,
        }

    # ── build context from DB ─────────────────────────────────────────────────
    context = _build_project_context(user)

    # ── ask the LLM ───────────────────────────────────────────────────────────
    result = _llm_respond(
        user_text=message or "",
        agent="pm",
        conversation_id=conversation_id,
        language=language,
        context=context,
        structured=False,
    )

    return {
        "agent": "pm",
        "answer": result.get("answer", ""),
        "conversation_id": result.get("conversation_id", conversation_id),
    }
