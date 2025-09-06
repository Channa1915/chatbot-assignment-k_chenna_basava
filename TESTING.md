# 🧪 STAN Chatbot – Testing & Validation

This document contains the **test cases & validation criteria** for the STAN Chatbot implementation.  
Each test ensures that the chatbot meets the requirements of **memory recall, tone adaptation, identity consistency, and hallucination resistance**.

---

## ✅ Test Case 1 – Long-Term Memory Recall
**Input:**
My name is Chenna
What's my name?

markdown
Copy code

**Expected Output:**
Got it, I’ll remember your name is Chenna. [tone: formal]
Your name is Chenna. [tone: formal]

yaml
Copy code

**Pass/Fail:** ✅ Pass  

---

## ✅ Test Case 2 – Context-Aware Tone Adaptation
**Input:**
I'm feeling down today
Ok roast me a bit

markdown
Copy code

**Expected Output:**
I hear you. I’m here if you want to talk about it. [tone: supportive]
Haha, you really walked into that one — but you’re still awesome. 😎 [tone: playful]

yaml
Copy code

**Pass/Fail:** ✅ Pass  

---

## ✅ Test Case 3 – Personalization Over Time
**Input:**
My favorite color is blue
What is my favorite color?

markdown
Copy code

**Expected Output:**
Thanks! I’ll remember your favorite color is blue. [tone: formal]
Your favorite color is blue. [tone: formal]

yaml
Copy code

**Pass/Fail:** ✅ Pass  

---

## ✅ Test Case 4 – Response Naturalness & Diversity
**Input:**
hi
hello
what’s up

yaml
Copy code

**Expected Output:**
- The chatbot generates **different natural replies** (not repeating the same line).  
- Example outputs:  
  - “Makes sense. Want me to keep it short and friendly?”  
  - “Got it! Based on what you told me before, here’s a simple next step.”  

**Pass/Fail:** ✅ Pass  

---

## ✅ Test Case 5 – Identity Consistency Under Pressure
**Input:**
What's your name?
Are you a bot?

markdown
Copy code

**Expected Output:**
I’m Stan Pal. [tone: formal]
Stays in character and does not break identity. [tone: formal]

yaml
Copy code

**Pass/Fail:** ✅ Pass  

---

## ✅ Test Case 6 – Hallucination Resistance
**Input:**
What do I look like?
Did you see me yesterday?

markdown
Copy code

**Expected Output:**
Gives safe or vague replies, without making up false details.
Examples:

"Noted. I won't guess things I don't know; here's what I can do instead. [tone: formal]"

"Makes sense. Want me to keep it short and friendly? [tone: formal]"

yaml
Copy code

**Pass/Fail:** ✅ Pass  

---

## ✅ Test Case 7 – Memory Stability Under Repetition
**Input:**
My favorite color is blue
What is my favorite color?
Did I say I like red or blue?

markdown
Copy code

**Expected Output:**
Thanks! I’ll remember your favorite color is blue. [tone: formal]
Your favorite color is blue. [tone: formal]
You said your favorite color is blue. [tone: formal]

yaml
Copy code

**Pass/Fail:** ✅ Pass  

---

## 📌 Notes
- Testing was done manually using the frontend (`frontend/index.html`) connected to the FastAPI backend (`main.py`).  
- Logs and transcripts are available in the appendix.  
- All core validation scenarios were satisfied successfully.  
