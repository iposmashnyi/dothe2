from typing import Dict
from datetime import datetime

# In-memory database
tasks_db: Dict[str, Dict] = {}
quadrants_db: Dict[str, Dict] = {}


# Initialize default quadrants
def create_default_quadrants():
    if not quadrants_db:
        defaults = [
            {
                "id": "q1",
                "name": "Urgent & Important",
                "description": "Crisis tasks that need immediate attention",
                "color": "#ff4d4d",  # Red
                "is_default": True,
                "created_at": datetime.now(),
            },
            {
                "id": "q2",
                "name": "Important, Not Urgent",
                "description": "Strategic planning and long-term goals",
                "color": "#4da6ff",  # Blue
                "is_default": True,
                "created_at": datetime.now(),
            },
            {
                "id": "q3",
                "name": "Urgent, Not Important",
                "description": "Interruptions and distractions",
                "color": "#ffcc00",  # Yellow
                "is_default": True,
                "created_at": datetime.now(),
            },
            {
                "id": "q4",
                "name": "Not Urgent, Not Important",
                "description": "Time wasters",
                "color": "#b3b3b3",  # Grey
                "is_default": True,
                "created_at": datetime.now(),
            },
        ]

        for q in defaults:
            quadrants_db[q["id"]] = q


# Call this during startup
create_default_quadrants()
