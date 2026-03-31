# PawPal+ Project Reflection

## 1. System Design
**Core user actions**
1. User enters owner + pet info.
2. User adds tasks (duration, priority).
3. User generates a daily plan with explanation.
**a. Initial design**

- Briefly describe your initial UML design.
My initial design had four classes: Owner, Pet, Task, and Scheduler. Owner stores the pet owner’s information, availability, preferences, and list of pets. Pet stores the animal’s basic information and its care tasks. Task represents individual care activities like feeding, walking, medication, or grooming, and includes attributes such as duration, priority, due time, and recurrence. Scheduler is responsible for sorting tasks, applying constraints, generating a daily plan, and explaining why tasks were selected.

- What classes did you include, and what responsibilities did you assign to each?
I included four main classes: Owner, Pet, Task, and Scheduler. Owner is responsible for storing the user’s information, availability, preferences, and list of pets. Pet is responsible for storing details about each animal and managing its tasks. Task represents individual care activities and stores attributes like duration, priority, due time, and recurrence. Scheduler is responsible for the planning logic, including sorting tasks, applying constraints, generating a daily plan, and explaining why certain tasks were selected.

**b. Design changes**

- Did your design change during implementation?
Yes, but only slightly. I kept the same four main classes because the overall structure already matched the problem well.

- If yes, describe at least one change and why you made it.
One important refinement was keeping Scheduler responsible for the planning logic instead of moving scheduling behavior into Owner or Pet. This made the system more modular and easier to test. I also decided not to adopt more advanced suggestions like caching or extra relationship classes, because they would add unnecessary complexity for this version of the project.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My scheduler considers several constraints: task due time, task priority, task duration, and the owner's available time windows. It also filters out completed tasks and includes recurring tasks when relevant. I prioritized due time and priority as the most important factors because they directly affect urgency. Availability was also important to ensure tasks fit realistically into the owner's schedule.

- How did you decide which constraints mattered most?
My scheduler considers several constraints: task due time, task priority, task duration, and the owner's available time windows. It also filters out completed tasks and includes recurring tasks when relevant. I prioritized due time and priority as the most important factors because they directly affect urgency. Availability was also important to ensure tasks fit realistically into the owner's schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My scheduler only checks conflicts when tasks have the exact same due time, instead of detecting every possible overlap in durations. This is a simplification of the full scheduling problem.

- Why is that tradeoff reasonable for this scenario?
This tradeoff is reasonable because it keeps the algorithm simple, fast, and easy to understand while still catching obvious scheduling conflicts. For this version of the project, detecting exact-time conflicts gives useful feedback without making the code too complex.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI for brainstorming the UML design, generating class skeletons, refining scheduling methods, and improving algorithms like sorting, filtering, recurrence, and conflict detection. I also used it to review my code and suggest cleaner implementations.

- What kinds of prompts or questions were most helpful?
The most helpful prompts were specific implementation questions, such as asking how to sort tasks with Python’s sorted() function, how to use timedelta for recurring tasks, and how to design a lightweight conflict detection method. Targeted prompts worked better than broad ones because they produced more practical answers.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment was when AI suggested adding more advanced features like caching and extra relationship layers between objects. I chose not to use those suggestions directly.

- How did you evaluate or verify what the AI suggested?
I evaluated the suggestions by comparing them to the scope of the assignment. If a suggestion made the code harder to understand without improving the required functionality, I rejected it. I kept solutions that improved readability, performance, or correctness without adding unnecessary complexity.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested task completion, task addition to a pet, sorting tasks by due time, filtering by pet and completion status, recurring task generation, and conflict detection for tasks with the same due time.

- Why were these tests important?
These tests were important because they checked the core behaviors of the system. They showed that tasks can be created and managed correctly, that scheduling logic behaves as expected, and that the smarter features added later actually work.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am confident that the scheduler works correctly for the main use cases in this project. The CLI demo and test cases both showed that the major features behave as expected.

- What edge cases would you test next if you had more time?
If I had more time, I would test overlapping durations, tasks without due times, multiple recurring tasks on the same day, duplicate task IDs, and cases where many tasks compete for a very small time window.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with turning the system from a UML design into a working scheduler with sorting, filtering, recurrence, and conflict detection. I am also happy that the app and backend logic were successfully connected.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve conflict detection so it handles overlapping time ranges, not only exact matching due times. I would also refine the scheduling algorithm to make better placement decisions when many tasks compete for limited time.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that strong system design makes coding much easier. I also learned that AI is most useful when I treat it as a tool for suggestions and feedback, not as something to follow blindly.
