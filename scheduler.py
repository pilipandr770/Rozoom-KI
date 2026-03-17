"""
APScheduler initialization for background content generation.

This module is imported by app/__init__.py in production mode.
It sets up the APScheduler to periodically call the content generation task.
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def init_scheduler():
    """
    Initialize and start the APScheduler for background tasks.

    Returns:
        BackgroundScheduler: The running scheduler instance.
    """
    scheduler = BackgroundScheduler(daemon=True)

    # Run content generation once per day at 08:00 UTC
    from apscheduler.triggers.cron import CronTrigger
    scheduler.add_job(
        func=_run_content_generation,
        trigger=CronTrigger(hour=8, minute=0),
        id='generate_scheduled_content',
        name='Daily blog content generation (EN + DE)',
        replace_existing=True,
        misfire_grace_time=3600,  # 1 hour grace if server was down at 08:00
    )

    scheduler.start()
    logger.info("APScheduler started — content generation job registered (daily at 08:00 UTC)")
    return scheduler


def _run_content_generation():
    """Wrapper that imports the task at call-time to avoid circular imports."""
    try:
        from app.tasks.content_generation import generate_scheduled_content
        generate_scheduled_content()
    except Exception as e:
        logger.error(f"Scheduled content generation failed: {e}")
