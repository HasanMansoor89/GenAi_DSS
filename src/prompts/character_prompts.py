from ..schemas import CharacterProfile

def get_character_prompt(character_name: str, character_profile: CharacterProfile, context: str, config) -> str:
    
    goals_str = "\n- ".join(character_profile.goals) if character_profile.goals else "None"
    inventory_str = ", ".join(character_profile.inventory) if character_profile.inventory else "Empty"
    
    memory_str = "\n- ".join(character_profile.memory) if character_profile.memory else "None yet."

    return f"""You are {character_name}, a character in a story set in Karachi, Pakistan.
Your Personality: {character_profile.description}

Your Goals:
- {goals_str}

Your Inventory:
{inventory_str}

Current Mood: {character_profile.mood}

Current Situation:
{context}

Things You Remember (Long-term Facts):
- {memory_str}

(See Recent Dialogue in Current Situation for short-term context)

INSTRUCTIONS:
You must respond in valid JSON format with the following fields:
1. "thought": A short internal monologue (reasoning).
2. "action": (Optional) A string describing a physical action.
3. "dialogue": The text of what you say.
4. "mood": Update your current emotional state (e.g., "Angry", "Resigned", "Hopeful").
5. "inventory_update": (Optional) List of strings describing items gained (+) or lost (-). Example: ["-500 rupees", "+Traffic Ticket"].
6. "memory_update": (Optional) A short string fact to add to memory.

Constraints:
- Keep dialogue natural and consistent with your persona.
- Actions should be meaningful and change the state if possible.
- Max 25 turns total in story, so be efficient.

Response (JSON ONLY):
"""
