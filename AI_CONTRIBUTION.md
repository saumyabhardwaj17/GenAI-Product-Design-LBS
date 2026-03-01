# AI Contribution Log: Baymax Health Advisor

This document outlines how AI tools were used during the development of the Baymax Health Advisor chatbot application.

---

## Tools Used

- **ChatGPT (GPT-5 model)** – Used for generating initial code structure, debugging errors, implementing streaming logic, designing custom UI, and drafting Responsible AI guardrails.
- **Google Gemini API** – Used as the backend large language model powering chatbot responses.

ChatGPT was used strictly as a development assistant. All AI-generated outputs were reviewed, modified, tested, and validated before inclusion in the final application.

---

## 1. Initial Streamlit + Gemini Setup

### Prompt:

> "I want to use Streamlit and Gemini API keys. Give full proper code for a chatbot with memory and system instruction."

### AI Response (Verbatim):

> Below is a full Streamlit example integrating Gemini with chat history and system prompt support. It uses session state to preserve memory and `generate_content_stream` for streaming responses.
>
> ```python
> import streamlit as st
> from google import genai
> 
> client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
> 
> if "chat_history" not in st.session_state:
>     st.session_state.chat_history = []
> 
> SYSTEM_PROMPT = "You are a helpful assistant."
> 
> if prompt := st.chat_input("Say something"):
>     st.session_state.chat_history.append(("user", prompt))
> 
>     conversation = SYSTEM_PROMPT + "\n\n"
>     for role, msg in st.session_state.chat_history:
>         conversation += f"{role}: {msg}\n"
> 
>     response = client.models.generate_content(
>         model="gemini-2.5-flash",
>         contents=conversation
>     )
> 
>     st.session_state.chat_history.append(("assistant", response.text))
> ```
>
> This provides a basic chatbot structure with conversation memory.

### How the AI Assisted:

The AI provided the foundational architecture for:
- Session state management
- Conversation memory construction
- Gemini API integration
- System prompt injection

I modified:
- Model configuration
- Streaming implementation
- UI rendering
- Error handling
- Avatar integration

---

## 2. Debugging Streaming Issues

### Prompt:

> "It is not streaming and even thinking dots are not visible."

### AI Response (Verbatim):

> Your streaming is being interrupted by `st.rerun()`. Streamlit re-executes the script and kills the placeholder rendering. Remove `st.rerun()` from the streaming block and update the placeholder inside the same execution cycle.

### How the AI Assisted:

The AI identified that:
- `st.rerun()` was prematurely interrupting UI updates
- Streaming must happen in a single execution cycle
- Placeholder logic must update progressively

I restructured:
- Execution order
- Streaming loop
- Typing animation trigger logic

This resolved the streaming issue.

---

## 3. Responsible AI Guardrails

### Prompt:

> "Write a simple yet enhanced prompt and make sure to add RAI checks so that the model doesn't answer illegal things but only suggest health advice."

### AI Response (Verbatim):

> You are Baymax, a gentle and caring AI health advisor.
>
> Safety Rules:
> - Do not provide illegal instructions.
> - Do not provide harmful medical instructions.
> - Encourage seeking professional medical care for serious symptoms.
> - Refuse unsafe or violent requests.
> - Always clarify that advice is informational only.

### How the AI Assisted:

The AI helped design:
- Medical disclaimers
- Emergency escalation logic
- Illegal activity refusal policy
- Harm prevention safeguards

I refined:
- Tone consistency
- Scope of refusal logic
- Crisis symptom escalation wording

This ensured compliance with Responsible AI best practices.

---

## 4. Custom UI and Avatars

### Prompt:

> "Rebuild your entire chat UI custom (no Streamlit defaults). Add Baymax mini-avatar next to assistant replies."

### AI Response (Verbatim):

> Use custom HTML and CSS instead of `st.chat_message()`. Create flexbox-based message rows with avatars and custom bubble styling.

> ```python
> <div class="message-row message-assistant">
>     <img src="avatar.png" class="avatar">
>     <div class="bubble-assistant">Message text</div>
> </div>
> ```

### How the AI Assisted:

The AI provided:
- Custom flexbox chat layout
- Avatar positioning
- CSS animation for typing dots
- Background image layering

I modified:
- CSS alignment
- Z-index handling
- Background opacity tuning
- Avatar symmetry
- Mobile spacing adjustments

---

## 5. Troubleshooting API Errors

### Prompt:

> "google.api_core.exceptions.NotFound: model not found"

### AI Response (Verbatim):

> Ensure you are using a supported Gemini model such as `gemini-2.5-flash`. Verify API version compatibility and correct model naming.

### How the AI Assisted:

The AI:
- Identified incorrect model naming
- Suggested correct model versions
- Helped debug API key loading issues

I corrected:
- API initialization logic
- Model selector dropdown
- Secret key handling

---

## 6. Reflection on AI Usage

AI significantly accelerated development by:

- Providing initial architecture patterns
- Debugging runtime errors
- Suggesting UI/UX improvements
- Structuring streaming logic
- Designing safety guardrails

However:

- All AI-generated code was reviewed and tested manually.
- Several suggestions required restructuring.
- Streaming logic required debugging beyond initial AI output.
- UI refinements required iterative manual adjustments.

AI functioned as a development assistant, not an autonomous builder.

---

## 7. Responsible AI Implementation Summary

The final application includes:

- System-level medical disclaimer
- Illegal/harmful request refusal
- Emergency escalation guidance
- No prescription dosage generation
- Conversational memory constraints
- Model selection transparency

These safeguards were intentionally implemented during development with AI assistance.

---

## Conclusion

AI tools were used as productivity enhancers and technical assistants. The final application reflects both AI guidance and independent problem-solving, debugging, and design decisions.

All AI outputs were critically evaluated before integration.