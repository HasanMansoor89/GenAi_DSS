from typing import List, Dict
from .base_agent import BaseAgent
from ..config import StoryConfig
from ..schemas import StoryState, CharacterProfile
from ..prompts.character_prompts import get_character_prompt

class CharacterAgent(BaseAgent):
    def __init__(self, name: str, config: StoryConfig):
        super().__init__(name, config)

    async def respond(self, story_state: StoryState, context: str) -> Dict:
        """Generate a response based on the current story state and context."""
        
        # Get character profile
        character_profile = story_state.character_profiles.get(self.name)
        
        # Build prompt
        prompt = get_character_prompt(
            character_name=self.name,
            character_profile=character_profile,
            context=context,
            config=self.config
        )
        
        # --- ACTION ENFORCEMENT LOGIC ---
        # Count existing actions in history (check 'content' for [ACTION])
        action_count = sum(1 for e in story_state.events if "[ACTION]" in str(e.get('content', '')))
        
        # Calculate urgency
        needed = max(0, 5 - action_count)
        remaining_turns = max(0, self.config.max_turns - story_state.current_turn)
        
        # Force action if needed and running out of time
        # E.g., need 2 actions, 4 turns left -> Force.
        if needed > 0 and remaining_turns <= (needed * 2):
             prompt += "\n\nSYSTEM OVERRIDE: You MUST include a physical action in your response's 'action' field to drive the plot forward."
        elif needed > 0 and story_state.current_turn > 5:
             # Soft nudge
             prompt += "\n\nHint: Consider performing a physical action instead of just talking."
        # --------------------------------
        
        try:
            content = await self.generate_response(prompt)
            content = self._clean_json_response(content)
            
            import json
            try:
                response_data = json.loads(content)
            except json.JSONDecodeError:
                # Fallback if model fails to output valid JSON
                print(f"WARNING: Model {self.name} failed to output JSON. Raw: {content[:50]}...")
                response_data = {
                    "thought": "I am confused.",
                    "action": None,
                    "dialogue": content,
                    "memory_update": None,
                    "mood": character_profile.mood,
                    "inventory_update": None
                }
            
            # --- PROCESS UPDATES ---
            
            # 1. Update Mood
            new_mood = response_data.get("mood")
            if new_mood and new_mood != character_profile.mood:
                old_mood = character_profile.mood
                character_profile.mood = new_mood
                print(f"\n🎭 [MOOD CHANGE]: {old_mood} -> {new_mood}")

            # 2. Update Inventory
            inv_changes = response_data.get("inventory_update")
            if inv_changes and isinstance(inv_changes, list):
                for change in inv_changes:
                    if change.startswith("-"):
                        item = change[1:].strip()
                        if item in character_profile.inventory:
                            character_profile.inventory.remove(item)
                    elif change.startswith("+"):
                        character_profile.inventory.append(change[1:].strip())
                print(f"\n🎒 [INVENTORY]: {inv_changes}")

            # 3. Update Memory
            memory_update = response_data.get("memory_update")
            if memory_update:
                if not hasattr(character_profile, 'memory'):
                    character_profile.memory = []
                character_profile.memory.append(memory_update)
                print(f"\n[MEMORY UPDATED]: {memory_update}")

            return response_data
            
        except Exception as e:
            print(f"Error in character response: {e}")
            return {
                "thought": "Error processing response",
                "action": None,
                "dialogue": "...",
                "memory_update": None,
                "mood": character_profile.mood,
                "inventory_update": None
            }
