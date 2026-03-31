## PawPal+ UML

```mermaid
classDiagram
    class Owner {
        - id: int
        - name: str
        - contact: str
        - available_time: dict     -- e.g. {"mon": [(9,11),(18,20)], ...}
        - preferences: dict        -- scheduling prefs, priorities, exclusions
        - pets: list[Pet]
        + add_pet(pet: Pet) -> None
        + remove_pet(pet_id: int) -> None
        + update_availability(availability: dict) -> None
    }

    class Pet {
        - id: int
        - name: str
        - species: str
        - age: int
        - notes: str
        - tasks: list[Task]
        + add_task(task: Task) -> None
        + remove_task(task_id: int) -> None
        + upcoming_tasks(days: int=7) -> list[Task]
    }

    class Task {
        - id: int
        - title: str
        - category: str           -- e.g. "feeding", "walk", "medication"
        - duration_minutes: int
        - priority: int           -- higher = more urgent/important
        - due_time: datetime|None
        - completed: bool
        - recurrence: dict|None   -- e.g. {"freq":"daily","interval":1}
        + mark_completed() -> None
        + is_overdue(now: datetime) -> bool
        + next_occurrence(after: datetime) -> datetime|None
    }

    class Scheduler {
        + sort_tasks(tasks: list[Task]) -> list[Task]
        + generate_daily_plan(owner: Owner, date: date) -> dict   -- returns schedule slots
        + explain_selection(task: Task, context: dict) -> str     -- human-readable rationale
        + apply_constraints(tasks: list[Task], owner: Owner, date: date) -> list[Task]
    }

    Owner "1" o-- "*" Pet : owns
    Pet "1" o-- "*" Task : has
    Scheduler ..> Owner : reads
    Scheduler ..> Pet : reads
    Scheduler ..> Task : schedules