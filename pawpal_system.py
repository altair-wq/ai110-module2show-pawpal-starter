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
        """Return True if the task is overdue compared to `now`."""
        now = now or datetime.now()
        if self.completed or self.due_time is None:
            return False
        return now > self.due_time

    def next_occurrence(self, after: Optional[datetime] = None) -> Optional[datetime]:
        """Return the next occurrence of this task after `after`."""
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

        if freq == "weekly":
            base_time = self.due_time.time() if self.due_time else time(9, 0)
            candidate = datetime.combine(after.date(), base_time)
            if candidate <= after:
                candidate = candidate + timedelta(weeks=interval)
            return candidate

        return None

    def create_next_recurring_task(self) -> Optional["Task"]:
        """Create the next task instance if this task is recurring."""
        if not self.recurrence or not self.due_time:
            return None

        freq = self.recurrence.get("freq")
        interval = int(self.recurrence.get("interval", 1))

        if freq == "daily":
            next_due = self.due_time + timedelta(days=interval)
        elif freq == "weekly":
            next_due = self.due_time + timedelta(weeks=interval)
        else:
            return None

        return Task(
            id=self.id + 1000,
            title=self.title,
            category=self.category,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            due_time=next_due,
            completed=False,
            recurrence=self.recurrence,
        )


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
        """Add a task to this pet."""
        if any(t.id == task.id for t in self.tasks):
            return
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Remove a task by id."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """Mark a task complete and auto-create the next recurring task."""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_completed()
                next_task = task.create_next_recurring_task()
                if next_task:
                    self.add_task(next_task)
                return next_task
        return None

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
    """Represents the owner of one or more pets."""

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
        """Attach a pet to this owner."""
        if any(p.id == pet.id for p in self.pets):
            return
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet by id."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def update_availability(self, availability: Dict[str, Any]) -> None:
        """Replace the owner's availability structure."""
        self.available_time = availability or {}


class Scheduler:
    """Responsible for selecting and ordering tasks into a daily plan."""

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by due time, then priority, then duration."""
        return sorted(
            tasks,
            key=lambda t: (
                t.due_time or datetime.max,
                -t.priority,
                t.duration_minutes,
            ),
        )

    def filter_tasks(
        self,
        tasks: List[Task],
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
        owner: Optional[Owner] = None,
    ) -> List[Task]:
        """Filter tasks by completion status or pet name."""
        filtered = tasks

        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]

        if pet_name is not None and owner is not None:
            pet_task_ids = set()
            for pet in owner.pets:
                if pet.name == pet_name:
                    pet_task_ids.update(task.id for task in pet.tasks)
            filtered = [task for task in filtered if task.id in pet_task_ids]

        return filtered

    def apply_constraints(self, tasks: List[Task], owner: Owner, plan_date: date) -> List[Task]:
        """Filter tasks for the plan date and owner preferences."""
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
        """Convert owner's available_time for the plan date into (start, end) datetime slots."""
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
        """Generate a schedule for the given owner and date."""
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
                    scheduled.append(
                        {
                            "pet_id": pet.id if pet else None,
                            "pet_name": pet.name if pet else None,
                            "task_id": task.id,
                            "task_title": task.title,
                            "start": start_dt,
                            "end": end_dt,
                            "reason": self.explain_selection(task, {"plan_date": plan_date}),
                        }
                    )
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

    def detect_due_time_conflicts(self, tasks: List[Task], owner: Owner) -> List[str]:
        """Return warnings when two or more tasks share the same due time.

        Simpler and faster than pairwise comparison:
        - builds a task_id -> pet_name map once
        - groups tasks by exact due_time
        - emits one warning per group with 2+ tasks
        """
        warnings: List[str] = []

        # quick map from task id -> pet name (avoids scanning pets repeatedly)
        task_to_pet: Dict[int, str] = {}
        for pet in owner.pets:
            for t in pet.tasks:
                task_to_pet[t.id] = pet.name

        # group tasks by due_time (skip tasks without due_time)
        groups: Dict[datetime, List[Task]] = {}
        for t in tasks:
            if not t.due_time:
                continue
            groups.setdefault(t.due_time, []).append(t)

        # produce one warning per due_time group that has multiple tasks
        for due_time, group in groups.items():
            if len(group) <= 1:
                continue
            parts = [
                f"'{t.title}' ({task_to_pet.get(t.id, 'Unknown')})" for t in group
            ]
            warnings.append(
                f"Warning: tasks {', '.join(parts)} share the same due time "
                f"at {due_time.strftime('%Y-%m-%d %H:%M')}."
            )

        return warnings

    def explain_selection(self, task: Task, context: Optional[Dict[str, Any]] = None) -> str:
        """Produce a human-readable rationale for why a task was selected."""
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
        