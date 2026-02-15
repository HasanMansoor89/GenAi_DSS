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

### 6. 🎯 Goal-Oriented Behavior
Agents are not just reactive; they are driven by specific objectives.
- **Context Injection:** Each agent has a set of `goals` injected into their system prompt (e.g., "Avoid paying the bribe", "Get to the hospital").
- **Impact:** The "Chain-of-Thought" engine uses these goals to evaluate trade-offs during decision making.

### 7. 🛡️ Robustness & Reliability
The system includes fail-safes to ensure continuous operation.
- **JSON Validation:** All agent outputs are validated against a strict schema.
- **Auto-Correction:** If an LLM produces malformed JSON, a fallback mechanism captures the raw text as dialogue to prevent a crash.

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
3.  Auto-generate story files in the `Story_Output/` directory (e.g., `Story_Output/The_Rickshaw_Accident_Scenario#1.json`) and `prompts_log.json` (Debug Log).

---

## 📂 Understanding the Output

The console output is color-coded and structured for clarity. Additionally, structured JSON logs are saved to disk.

### 📄 Output Files

- **`Story_Output/` Folder**: Contains the full narrative logs in JSON format.
  - Files are named: `[Scenario_Name]#[Run_ID].json` (e.g., `The_Rickshaw_Accident_Scenario#1.json`).
  - Each file contains an array of turn objects with structured fields (speaker, dialogue, action, mood, memory).
- **`prompts_log.json`**: A raw debug log of all prompts sent to the LLM and its responses.

### Console Output Structure:

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
