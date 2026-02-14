# GenAI_DSS: Technical Design Report

**Module:** Generative AI  
**Author:** (Your Name)  
**Task:** Multi-Agent Narrative System

---

## 1. System Architecture

This solution enhances the default "Dialogue Only" agents with a **Cognitive Loop (Plan-Act-Learn)**. The core innovation is the decoupling of **Thought**, **Action**, and **Dialogue**.

### High-Level Flow
1. **Director Engine (`NarrativeGraph`):** Selects the next speaker based on turn history.
2. **Cognitive Agent (`CharacterAgent`):** Receives context -> Thinks -> Decides Action/Dialogue -> Updates Memory.
3. **State Manager (`StoryState`):** Logs the action as a global event and appends it to the shared context.

---

## 2. Feature Implementation (Beyond Base Design)

### 2.1 The Reasoning Engine (Chain-of-Thought)
Unlike standard LLM calls, our agents execute a multi-step reasoning process within a single prompt generation.
- **Input:** Full context + Persona Goals + Inventory + **Long-Term Memory**.
- **Process:** The LLM is instructed to first output a `thought` field. This acts as a "scratchpad" where the agent rationalizes its decision before committing to speech.
- **Output Schema (Strict JSON):**
  ```json
  {
      "thought": "Internal reasoning...",
      "action": "Physical action description...",
      "dialogue": "Spoken words...",
      "memory_update": "Fact to remember..."
  }
  ```

### 2.2 Autonomous Action System
Agents can modify the narrative state through physical actions.
- **Trigger:** Agents autonomously populate the `action` field.
- **Visibility:** Actions are logged as `[ACTION]: Content` events (`type: narration`) in the story graph. This ensures downstream agents "see" the physical act in their context window.
- **Enforcement Logic (Gap #3 Solved):**
  To guarantee the **5-Action Constraint**, the `CharacterAgent` counts existing actions in `state.events`.
  - If `Action Count` is low and turns are running out, the system injects a **SYSTEM OVERRIDE** into the prompt: *"You MUST include a physical action in this turn."*

### 2.3 Dynamic Evolving Memory (Gap #1 Solved)
Agents possess a mutable long-term memory.
- **Mechanism:** After generating a response, the specific `memory_update` field is extracted.
- **Storage:** This string is appended to the `CharacterProfile.memory` list.
- **Reinjection:** In future turns, the `get_character_prompt` function retrieves this list and injects it under `"Things You Remember (Long-term Facts)"`. This allows agents to recall events even if they slide out of the token window.

---

## 3. Design Decisions & Trade-offs

### JSON vs. Free-TxT
*Decision*: We enforced structured JSON output.
*Justification*: Reliability. Parsing "Action: [text]" from free-text is prone to regex errors. JSON guarantees separation of concerns (Thought vs Speech). Robust error handling catches malformed JSON.

### Action Type Mapping
*Decision*: Actions are logged as `type: "narration"` in the final output.
*Justification*: To strictly adhere to the provided problem statement schema which lists only `"dialogue"` and `"narration"`. We prefix content with `[ACTION]` to maintain semantic clarity.

---

## 4. Constraint Adherence
- **Memory Management:** Prompts are dynamically truncated if `max_context_length` is exceeded (handled by underlying history pruning).
- **Turn Limits:** The simulation strictly ends between 10-25 turns.
- **Token Limits:** The recursive prompt structure ensures efficient use of context.
