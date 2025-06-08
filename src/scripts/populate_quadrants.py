#!/usr/bin/env python3
"""
Populate default quadrants script.

Usage:
    python populate_quadrants.py

This script will create the default Eisenhower Matrix quadrants if they don't exist.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.db.database import AsyncSession, local_session
from app.models.quadrant import Quadrant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def populate_default_quadrants(session: AsyncSession) -> None:
    """Create the default Eisenhower Matrix quadrants if they don't exist."""

    default_quadrants = [
        {
            "name": "Urgent & Important",
            "description": "Crisis tasks that need immediate attention",
            "color": "#ff4d4d",  # Red
            "is_default": True,
        },
        {
            "name": "Important, Not Urgent",
            "description": "Strategic planning and long-term goals",
            "color": "#4da6ff",  # Blue
            "is_default": True,
        },
        {
            "name": "Urgent, Not Important",
            "description": "Interruptions and distractions",
            "color": "#ffcc00",  # Yellow
            "is_default": True,
        },
        {
            "name": "Not Urgent, Not Important",
            "description": "Time wasters",
            "color": "#b3b3b3",  # Grey
            "is_default": True,
        },
    ]

    # Check if default quadrants already exist
    stmt = select(Quadrant).where(Quadrant.is_default)
    result = await session.execute(stmt)
    existing_defaults = result.scalars().all()

    if existing_defaults:
        logger.info(f"Default quadrants already exist ({len(existing_defaults)} found)")
        return

    # Create default quadrants
    logger.info("Creating default quadrants...")
    created_count = 0
    for quadrant_data in default_quadrants:
        quadrant = Quadrant(**quadrant_data)
        session.add(quadrant)
        created_count += 1
        logger.debug(f"Added quadrant: {quadrant_data['name']}")

    await session.commit()
    logger.info(f"Successfully created {created_count} default quadrants")


async def main():
    """Run quadrant population."""
    logger.info("Starting quadrant population process")
    logger.info("Eisenhower Matrix quadrants to be created:")
    logger.info("   Q1: Urgent & Important (Red)")
    logger.info("   Q2: Important, Not Urgent (Blue)")
    logger.info("   Q3: Urgent, Not Important (Yellow)")
    logger.info("   Q4: Not Urgent, Not Important (Grey)")

    try:
        async with local_session() as session:
            await populate_default_quadrants(session)
        logger.info("Quadrant population completed successfully!")
    except Exception as e:
        logger.error(f"Error during population: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
