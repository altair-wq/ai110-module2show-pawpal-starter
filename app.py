import streamlit as st
from datetime import datetime, date, time as dtime
from typing import Optional

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Step 2: keep app memory in session_state
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        id=1,
        name="Owner",
        available_time={
            "mon": [(9, 11)],
            "tue": [(9, 11)],
            "wed": [(9, 11)],
            "thu": [(9, 11)],
            "fri": [(9, 11)],
            "sat": [(10, 12)],
            "sun": [(10, 12)],
        },
    )

if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = Scheduler()

if "next_pet_id" not in st.session_state:
    st.session_state["next_pet_id"] = 1

if "next_task_id" not in st.session_state:
    st.session_state["next_task_id"] = 1

owner: Owner = st.session_state["owner"]
scheduler: Scheduler = st.session_state["scheduler"]

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

st.divider()

# Step 3: Add Pet wired to Owner.add_pet()
st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Age", min_value=0, step=1, value=1)
    pet_notes = st.text_area("Notes", value="")
    pet_submitted = st.form_submit_button("Add Pet")

    if pet_submitted:
        new_pet = Pet(
            id=st.session_state["next_pet_id"],
            name=pet_name,
            species=species,
            age=int(pet_age),
            notes=pet_notes,
        )
        owner.add_pet(new_pet)
        st.session_state["next_pet_id"] += 1
        st.success(f"Added pet: {new_pet.name}")

st.subheader("Current Pets")
if owner.pets:
    for pet in owner.pets:
        st.write(f"- **{pet.name}** ({pet.species}), age {pet.age}")
else:
    st.info("No pets added yet.")

st.divider()

# Step 3: Add Task wired to Pet.add_task()
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before assigning tasks.")
else:
    pet_options = {f"{pet.name} (id={pet.id})": pet for pet in owner.pets}
    selected_pet_label = st.selectbox("Choose pet", list(pet_options.keys()))
    selected_pet = pet_options[selected_pet_label]

    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        task_category = st.text_input("Category", value="walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        set_due = st.checkbox("Set due date/time", value=False)
        due_dt: Optional[datetime] = None
        if set_due:
            due_date = st.date_input("Due date", value=date.today())
            due_time = st.time_input("Due time", value=dtime(9, 0))
            due_dt = datetime.combine(due_date, due_time)

        recurrence_label = st.selectbox("Recurrence", ["none", "daily"], index=0)
        task_submitted = st.form_submit_button("Add Task")

        if task_submitted:
            priority_map = {"low": 1, "medium": 2, "high": 3}
            recurrence = None
            if recurrence_label == "daily":
                recurrence = {"freq": "daily", "interval": 1}

            new_task = Task(
                id=st.session_state["next_task_id"],
                title=task_title,
                category=task_category,
                duration_minutes=int(duration),
                priority=priority_map[priority_label],
                due_time=due_dt,
                recurrence=recurrence,
            )
            selected_pet.add_task(new_task)
            st.session_state["next_task_id"] += 1
            st.success(f"Added task '{new_task.title}' to {selected_pet.name}")

st.subheader("Current Tasks")
has_tasks = any(pet.tasks for pet in owner.pets)

if has_tasks:
    for pet in owner.pets:
        st.write(f"**Tasks for {pet.name}**")
        if pet.tasks:
            rows = []
            for task in pet.tasks:
                rows.append(
                    {
                        "id": task.id,
                        "title": task.title,
                        "category": task.category,
                        "duration": task.duration_minutes,
                        "priority": task.priority,
                        "due": task.due_time.isoformat() if task.due_time else "",
                        "recurrence": task.recurrence if task.recurrence else "",
                        "completed": task.completed,
                    }
                )
            st.table(rows)
        else:
            st.write("- no tasks")
else:
    st.info("No tasks added yet.")

st.divider()

# Step 3: Generate schedule wired to Scheduler.generate_daily_plan()
st.subheader("Build Schedule")
plan_date = st.date_input("Plan date", value=date.today())

if st.button("Generate schedule"):
    plan = scheduler.generate_daily_plan(owner, plan_date)

    st.subheader("Schedule")

    scheduled = plan.get("scheduled", [])
    unscheduled = plan.get("unscheduled", [])

    if scheduled:
        display_rows = []
        for item in scheduled:
            display_rows.append(
                {
                    "pet": item.get("pet_name"),
                    "task": item.get("task_title"),
                    "start": item.get("start").strftime("%H:%M") if item.get("start") else "",
                    "end": item.get("end").strftime("%H:%M") if item.get("end") else "",
                    "reason": item.get("reason"),
                }
            )
        st.table(display_rows)
    else:
        st.info("No tasks were scheduled for this date.")

    if unscheduled:
        st.warning(f"Unscheduled task ids: {unscheduled}")
    else:
        st.write("All candidate tasks were scheduled or there were no candidate tasks.")