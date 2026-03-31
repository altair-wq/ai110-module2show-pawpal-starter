from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta, time
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
        self.completed = True

    def is_overdue(self, now: Optional[datetime] = None) -> bool:
        """Return True if the task is overdue compared to `now`.

        A task is overdue when it has a due_time in the past and is not completed.
        """
        now = now or datetime.now()
        if self.completed or self.due_time is None:
            return False
        return now > self.due_time

    def next_occurrence(self, after: Optional[datetime] = None) -> Optional[datetime]:
        """Return the next occurrence of this task after `after`.

        Minimal support for daily recurrence. If no recurrence, returns due_time if after < due_time.
        """
        after = after or datetime.now()
        if self.recurrence is None:
            if self.due_time and self.due_time > after:
                return self.due_time
            return None

        if not isinstance(self.recurrence, dict):
            return None

        freq = self.recurrence.get("freq")
        interval = int(self.recurrence.get("interval", 1))

        if freq == "daily":
            base_time = self.due_time.time() if self.due_time else time(9, 0)
            candidate = datetime.combine(after.date(), base_time)
            if candidate <= after:
                candidate = candidate + timedelta(days=interval)
            return candidate

        return None


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
        """Add a Task to this pet. Skips duplicate ids."""
        if any(t.id == task.id for t in self.tasks):
            return
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Remove a Task by id."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Return tasks occurring within the next `days` days or recurring daily tasks."""
        now = datetime.now()
        end = now + timedelta(days=days)
        out: List[Task] = []
        for t in self.tasks:
            if t.completed:
                continue
            if t.due_time and now <= t.due_time <= end:
                out.append(t)
                continue
            if t.recurrence and isinstance(t.recurrence, dict) and t.recurrence.get("freq") == "daily":
                out.append(t)
        return out


class Owner:
    """Represents the owner of one or more pets.

    available_time example:
      { 'mon': [(9,11),(18,20)], 'tue': [(7,9)], ... }
    Each tuple is (start_hour, end_hour) in 24h integers.
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
        """Attach a Pet to this Owner. Skips duplicates by id."""
        if any(p.id == pet.id for p in self.pets):
            return
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove a Pet by id."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def update_availability(self, availability: Dict[str, Any]) -> None:
        """Replace the owner's availability structure."""
        self.available_time = availability or {}


class Scheduler:
    """Responsible for selecting and ordering tasks into a daily plan."""

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort by priority (desc), then by due_time (asc), then shorter duration."""
        def key(t: Task):
            due = t.due_time or datetime.max
            return (-t.priority, due, t.duration_minutes)

        return sorted(tasks, key=key)

    def apply_constraints(self, tasks: List[Task], owner: Owner, plan_date: date) -> List[Task]:
        """Filter tasks for the plan_date and owner preferences.

        - Exclude completed
        - Include tasks due today
        - Include daily recurring tasks
        - Include flexible tasks
        """
        out: List[Task] = []
        for t in tasks:
            if t.completed:
                continue
            if t.due_time:
                if t.due_time.date() == plan_date:
                    out.append(t)
                else:
                    continue
            elif t.recurrence and isinstance(t.recurrence, dict) and t.recurrence.get("freq") == "daily":
                out.append(t)
            else:
                out.append(t)
        return out

    def _get_day_slots(self, owner: Owner, plan_date: date) -> List[tuple]:
        """Convert owner's available_time for the plan_date into list of (start_dt, end_dt) tuples."""
        weekday_keys = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        key = weekday_keys[plan_date.weekday()]
        raw = owner.available_time.get(key, [])
        slots: List[tuple] = []
        for (sh, eh) in raw:
            try:
                start_dt = datetime.combine(plan_date, time(int(sh), 0))
                end_dt = datetime.combine(plan_date, time(int(eh), 0))
            except Exception:
                continue
            if end_dt > start_dt:
                slots.append((start_dt, end_dt))
        return slots

    def generate_daily_plan(self, owner: Owner, plan_date: date) -> Dict[str, Any]:
        """Generate a schedule for the given owner and date.

        Returns a dictionary:
          { 'date': plan_date, 'scheduled': [...], 'unscheduled': [...] }
        """
        # collect tasks from owner's pets
        all_tasks: List[Task] = []
        for pet in owner.pets:
            all_tasks.extend(pet.tasks)

        candidates = self.apply_constraints(all_tasks, owner, plan_date)
        sorted_tasks = self.sort_tasks(candidates)

        slots = self._get_day_slots(owner, plan_date)
        scheduled: List[Dict[str, Any]] = []
        unscheduled: List[int] = []

        slot_index = 0
        current_pointer: Optional[datetime] = slots[0][0] if slots else None

        for task in sorted_tasks:
            placed = False
            for i in range(slot_index, len(slots)):
                slot_start, slot_end = slots[i]
                if current_pointer is None or current_pointer < slot_start:
                    current_pointer = slot_start
                remaining = int((slot_end - current_pointer).total_seconds() // 60)
                if remaining >= task.duration_minutes:
                    start_dt = current_pointer
                    end_dt = start_dt + timedelta(minutes=task.duration_minutes)
                    pet = next((p for p in owner.pets if any(t.id == task.id for t in p.tasks)), None)
                    scheduled.append({
                        "pet_id": pet.id if pet else None,
                        "pet_name": pet.name if pet else None,
                        "task_id": task.id,
                        "task_title": task.title,
                        "start": start_dt,
                        "end": end_dt,
                        "reason": self.explain_selection(task, {"plan_date": plan_date}),
                    })
                    current_pointer = end_dt
                    if current_pointer >= slot_end:
                        slot_index = i + 1
                        if slot_index < len(slots):
                            current_pointer = slots[slot_index][0]
                    placed = True
                    break
                else:
                    slot_index = i + 1
                    if slot_index < len(slots):
                        current_pointer = slots[slot_index][0]
            if not placed:
                unscheduled.append(task.id)

        return {"date": plan_date, "scheduled": scheduled, "unscheduled": unscheduled}

    def explain_selection(self, task: Task, context: Optional[Dict[str, Any]] = None) -> str:
        """Produce a human-readable rationale for why a task was selected/ordered."""
        parts: List[str] = [f"priority={task.priority}"]
        if task.due_time:
            parts.append(f"due={task.due_time.isoformat()}")
        elif task.recurrence:
            parts.append(f"recurrence={task.recurrence}")
        else:
            parts.append("flexible")
        if context and context.get("plan_date"):
            parts.append(f"for {context.get('plan_date')}")
        return "Selected (" + "; ".join(parts) + ")"