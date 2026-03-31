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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
