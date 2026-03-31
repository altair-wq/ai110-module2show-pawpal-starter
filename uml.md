## PawPal+ UML

```mermaid
classDiagram
    class Owner {
        - id: int
        - name: str
        - contact: str
        - available_time: dict
        - preferences: dict
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
        + mark_task_complete(task_id: int) -> Task|None
        + upcoming_tasks(days: int=7) -> list[Task]
    }

    class Task {
        - id: int
        - title: str
        - category: str
        - duration_minutes: int
        - priority: int
        - due_time: datetime|None
        - completed: bool
        - recurrence: dict|None
        + mark_completed() -> None
        + is_overdue(now: datetime) -> bool
        + next_occurrence(after: datetime) -> datetime|None
        + create_next_recurring_task() -> Task|None
    }

    class Scheduler {
        + sort_tasks(tasks: list[Task]) -> list[Task]
        + filter_tasks(tasks: list[Task], completed: bool|None, pet_name: str|None, owner: Owner|None) -> list[Task]
        + apply_constraints(tasks: list[Task], owner: Owner, date: date) -> list[Task]
        + generate_daily_plan(owner: Owner, date: date) -> dict
        + detect_due_time_conflicts(tasks: list[Task], owner: Owner) -> list[str]
        + explain_selection(task: Task, context: dict) -> str
    }

    Owner "1" o-- "*" Pet : owns
    Pet "1" o-- "*" Task : has
    Scheduler ..> Owner : reads
    Scheduler ..> Pet : reads
    Scheduler ..> Task : schedules
uml page screenshot can be accessed: ai110-module2show-pawpal-starter/uml_final.png
