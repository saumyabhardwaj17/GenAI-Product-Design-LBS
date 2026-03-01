# README.md


# 🤍 Baymax Health Advisor

A Streamlit-based AI chatbot that provides safe, supportive health guidance using the Google Gemini API.

This project was built for Assignment 1: Chatbot App.

---

## Overview

Baymax Health Advisor is an interactive web chatbot that:

- Maintains conversational memory
- Uses a customized system prompt (Baymax persona)
- Streams responses in real time
- Includes Responsible AI safeguards
- Provides general health guidance with safety disclaimers
- Escalates serious symptoms appropriately

The chatbot is designed to resemble a clean, modern health-tech product.

---

## Key Features

### Conversational Memory
The chatbot maintains chat history using Streamlit session state and sends full conversation context to Gemini for continued dialogue.

### Custom System Prompt
The assistant follows a carefully designed system instruction that:

- Enforces a calm, empathetic tone
- Provides general health information
- Refuses illegal or harmful requests
- Encourages professional medical consultation when necessary

### Streaming Responses
Responses are streamed word-by-word using:
```python
client.models.generate_content_stream(...)
````

### Custom UI

* Fully custom chat layout (no default Streamlit chat UI)
* Assistant avatar (`baymax-bot.png`)
* User avatar (`user.png`)
* Background branding (`baymax.png`)
* Animated typing indicator
* Sidebar controls

### Responsible AI Guardrails

The chatbot:

* Refuses illegal or violent instructions
* Avoids prescription dosage guidance
* Escalates emergency symptoms
* Includes a medical disclaimer

---

## Tech Stack

* Python 3.9+
* Streamlit
* Google Gemini API (`google-genai` SDK)
* Custom HTML/CSS styling

---

## Responsible AI Considerations

This application includes:

* Medical disclaimer logic
* Emergency escalation advice
* Refusal of illegal/harmful instructions
* No prescription dosage generation
* Safety-first conversational guardrails

The chatbot is informational only and does not replace professional medical advice.

---

## Project Structure

```
project/
│
├── app1.py
├── baymax.png
├── baymax-bot.png
├── user.png
├── requirements.txt
├── README.md
└──  AI_CONTRIBUTION.md

```

---

## Disclaimer

Baymax Health Advisor provides general health information only. It is not a substitute for professional medical diagnosis or treatment. Always consult a qualified healthcare provider for medical concerns.

---

## 🤍 Author

Developed by: *Group 5 - LBS: Saumya, Evelina, Chloe (Zilu), Andra, Christain, Dante, Kai*
Course: *Group Assignment 1 – Chatbot App*

