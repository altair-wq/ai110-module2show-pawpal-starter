# PawPal+ Project Reflection

## 1. System Design
1. User enters owner + pet info.
2. User adds tasks (duration, priority).
3. User generates a daily plan with explanation.
**a. Initial design**

- Briefly describe your initial UML design.
I designed PawPal+ using four classes: Owner, Pet, Task, and Scheduler. Owner stores user info, time, and preferences; pet stores animal info and its tasks; task represents activities like feeding or walking with duration and priority. Scheduler generates a daily plan by organizing tasks based on constraints. This keeps the system modular and easy to test.

- What classes did you include, and what responsibilities did you assign to each?
I kept Scheduler separate to handle all planning logic instead of mixing it into Owner or Pet. This improves modularity and makes testing easier. I also used dataclasses for cleaner code.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
