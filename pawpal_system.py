from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any


@dataclass
class Task:
    """Represents a task related to pet care."""
    id: int
    title: str
    category: str  # e.g. "feeding", "walk", "medication"
    duration_minutes: int
    priority: int  # higher = more urgent/important
    due_time: Optional[datetime] = None
    completed: bool = False
    recurrence: Optional[Dict[str, Any]] = None  # e.g. {"freq": "daily", "interval": 1}

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        pass

    def is_overdue(self, now: datetime) -> bool:
        """Return True if the task is overdue compared to `now`."""
        pass

    def next_occurrence(self, after: datetime) -> Optional[datetime]:
        """Return the next occurrence of this task after the given datetime, if recurring."""
        pass


@dataclass
class Pet:
    """Represents a pet owned by an Owner."""
    id: int
    name: str
    species: str
    age: int
    notes: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this pet."""
        pass

    def remove_task(self, task_id: int) -> None:
        """Remove a Task by id."""
        pass

    def upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Return tasks occurring within the next `days` days."""
        pass


class Owner:
    """Represents the owner of one or more pets.

    Designed for a CLI-first backend; store simple availability and preferences.
    """

    def __init__(
        self,
        id: int,
        name: str,
        contact: Optional[str] = None,
        available_time: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None,
        pets: Optional[List[Pet]] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.contact = contact
        self.available_time: Dict[str, Any] = available_time or {}
        self.preferences: Dict[str, Any] = preferences or {}
        self.pets: List[Pet] = pets or []

    def add_pet(self, pet: Pet) -> None:
        """Attach a Pet to this Owner."""
        pass

    def remove_pet(self, pet_id: int) -> None:
        """Remove a Pet by id."""
        pass

    def update_availability(self, availability: Dict[str, Any]) -> None:
        """Update owner's available_time structure."""
        pass


class Scheduler:
    """Responsible for selecting and ordering tasks into a daily plan."""

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority, due time, or other heuristics."""
        pass

    def apply_constraints(self, tasks: List[Task], owner: Owner, plan_date: date) -> List[Task]:
        """Apply availability, preferences and other constraints to filter/adjust tasks."""
        pass

    def generate_daily_plan(self, owner: Owner, plan_date: date) -> Dict[str, Any]:
        """Generate a schedule for the given owner and date.

        Returns a simple dictionary representing scheduled slots. Implementation intentionally omitted.
        """
        pass

    def explain_selection(self, task: Task, context: Optional[Dict[str, Any]] = None) -> str:
        """Produce a human-readable rationale for why a task was selected/ordered."""
        pass
