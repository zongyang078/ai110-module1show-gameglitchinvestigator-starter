# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

(1) When I first ran the game, it appeared to be a number guessing game built with Streamlit, but it was clearly broken.

(2) The most obvious issue was that the hints were reversed — when I guessed 1 and the secret was 97, the game told me "Go LOWER!" instead of "Go HIGHER!"

I also noticed that the score kept going negative even when I eventually won. The root cause was a double penalty: every wrong guess deducted 5 points, and the win bonus also shrank with more attempts. On a typical game this left the final score in the negatives.

A third bug was discovered through the Developer Debug Info panel: on even-numbered attempts, the code converts the secret number to a string before comparing it with the integer guess, causing unreliable comparisons and making it nearly impossible to win.

Further investigation revealed three more bugs: switching difficulty mid-game kept the old secret number instead of resetting, Hard mode gave only 5 attempts for a 1–500 range (mathematically requiring at least 9), and the guess input accepted numbers outside the valid range without any error.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

(1) I used Claude as my primary AI tool for this project. 

(2) One example of a correct suggestion was when Claude identified that the hint messages in check_guess were swapped — guess > secret was returning "Go HIGHER!" instead of "Go LOWER!". I verified this by checking the Debug Info panel: with secret=97 and guess=1, the game said "Go LOWER!" which was clearly wrong. After applying the fix, the hints matched the expected behavior. 

(3) An example of an incorrect suggestion was that Claude initially set attempts to start at 0 and only increment on valid guesses, but the Debug Info showed attempts=1 after two guesses were made. I realized the display was actually a Streamlit rerun timing issue rather than a real counting bug, so I kept the logic as-is after verifying the final results were correct.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by running the game manually through Streamlit and checking three things: that the hints pointed in the right direction, that the score stayed reasonable (not deeply negative), and that I could actually win the game. I also ran pytest tests/test_game_logic.py -v which ran 9 test cases covering check_guess, parse_guess, and update_score. For example, test_hint_message_direction verified that guessing 60 when the secret is 50 returns a message containing "LOWER", confirming the hint swap was fixed. Claude helped me design these tests by suggesting what to assert for each function based on the bugs we had just fixed.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit works by re-running the entire Python script from top to bottom every time the user interacts with the page (clicks a button, changes an input). This means any regular variable gets reset every time. To keep data between reruns, you use st.session_state, which is like a persistent dictionary that survives reruns. I would explain it to a friend as: "Imagine every time you click a button, the entire page reloads from scratch — session_state is the sticky note that remembers what happened before the reload."

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is writing pytest cases immediately after fixing a bug, before moving on. It gave me confidence that my fix actually worked and didn't break other things. Next time I work with AI on a coding task, I would review the AI's suggested code more carefully line by line before applying it, since some suggestions looked correct at first glance but had subtle issues like the string conversion bug. This project taught me that AI-generated code can look professional and complete while hiding serious logic errors — you always need to test and verify, not just trust the output.
