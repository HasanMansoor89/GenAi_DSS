# GenAI_DSS: Reasoning Multi-Agent Narrative System

> **Hackfest x Datathon 2026 Submission**  
> **Module:** Generative AI

This repository contains an advanced upgrade to the baseline Multi-Agent Narrative System. Unlike traditional chatbots, our agents possess **Cognitive Reasoning** (Thinking), **Physical Agency** (Acting), and **Long-Term Memory** (Learning).

---

## 🚀 Key Features Implemented

### 1. 🧠 Cognitive Reasoning Layer (The "Brain")
Every character executes a **Chain-of-Thought** process before generating dialogue. 
- **Internal Monologue:** Agents analyze the situation and their goals privately.
- **Decision Making:** They decide *whether* to speak or act based on this reasoning.
- **Output:** Visible in logs as `[INTERNAL THOUGHT]`.

### 2. ⚡ Autonomous Action System (The "Body")
Characters are no longer limited to speech. They can perform non-verbal actions that modify the story state.
- **Action Triggers:** Agents autonomously choose actions (e.g., `Picks up phone`, `Pays bribe`).
- **Enforcement:** If agents act too passive, a "Director Override" injects instructions to force action, ensuring the **5-Action Constraint** is always met.
- **Visibility:** Actions are logged as distinct narrative events (`type: narration`) and fed back into the context window of other agents.

### 3. 📝 Dynamic Evolving Memory (The "Mind")
Characters learn from their interactions.
- **Memory Update Loop:** After each turn, agents can choose to extract a "Memory Nugget" (e.g., "The constable is corrupt").
### 4. 🎭 Emotional Intelligence Engine
Agents possess dynamic emotional states (Moods) that evolve based on the conversation.
- **Mood Tracking:** Characters transition (e.g., `Neutral` -> `Angry` -> `Desperate`).
- **Context Injection:** The current mood is injected into the prompt, influencing the tone of the *next* response.
- **Visibility:** Mood changes are explicitly logged: `[MOOD CHANGE]: Neutral -> Angry`.

### 5. 🎒 Functional Inventory System
The "Action" system is backed by a real inventory.
- **Item Exchange:** Agents can gain (`+`) or lose (`-`) items.
- **Example:** A driver might lose `"-500 rupees"` and gain `"+Ticket"`.
- **Log:** Updates are shown as `[INVENTORY]: ['-500 rupees']`.

---

## 🛠️ Setup & Execution

### Prerequisites
- Python 3.10+
- `uv` package manager (or standard `pip`).

### Installation

1.  **Clone & Install Dependencies:**
    ```bash
    uv sync
    # OR
    pip install .
    ```

2.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```ini
    GOOGLE_API_KEY=your_gemini_api_key
    ```

### Running the Simulation

Execute the main script:
```bash
uv run src/main.py
```

The system will:
1.  Initialize the **Rickshaw Accident** scenario.
2.  Run for **10-25 turns**.
3.  Auto-generate `story_output.json` (Formatted Narrative) and `prompts_log.json` (Debug Log).

---

## 📂 Understanding the Output

The console output is color-coded and structured for clarity:

- **[INTERNAL THOUGHT]**: The agent's private reasoning.
- **[ACTION]**: Physical actions taken (e.g., *Checks watch*).
- **[DIALOGUE]**: Spoken words.
- **[MEMORY UPDATED]**: A new fact learned by the agent.

### Example Log Entry:
```
=== AHMED MALIK'S TURN ===

[INTERNAL THOUGHT]:
   This is wasting my time. I need to leave.

[ACTION]:
   Checks watch impatiently.

[DIALOGUE]:
   "Constable, I don't have all day!"

[MEMORY UPDATED]: Constable Raza is stalling.
```

---

## 📜 Technical Design
For a detailed breakdown of the architecture, prompt engineering, and logic flow, please see [DESIGN_REPORT.md](./DESIGN_REPORT.md).
