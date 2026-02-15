import asyncio
import json
import sys
import os
from pathlib import Path

current_dir = Path(__file__).parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config import StoryConfig
from src.agents.character_agent import CharacterAgent
from src.agents.director_agent import DirectorAgent
from src.graph.narrative_graph import NarrativeGraph
from src.story_state import StoryStateManager

async def main():
    # Load seed story from examples
    # Assuming examples is in project root
    examples_dir = project_root / "examples" / "rickshaw_accident"
    
    seed_story = json.loads((examples_dir / "seed_story.json").read_text())
    
    # Load character configs
    char_configs = json.loads((examples_dir / "character_configs.json").read_text())
    
    # Initialize config
    config = StoryConfig()
    
    # Create character agents
    characters = [
        CharacterAgent(
            name=char["name"],
            config=config
        )
        for char in char_configs["characters"]
    ]
    
    # Create director
    director = DirectorAgent(config)
    
    # Initialize StoryStateManager to prepare initial state properly
    story_manager = StoryStateManager(seed_story, char_configs["characters"], config)
    
    # Build and run narrative graph
    story_graph = NarrativeGraph(config, characters, director)
    
    print("Starting Narrative Game...")
    print(f"Title: {seed_story['title']}")
    print(f"Scenario: {seed_story['description']}\n")
    
    # Run the game with the prepared character states
    final_state = await story_graph.run(
        seed_story=seed_story, 
        character_profiles=story_manager.state.character_profiles
    )
    
    # Print results
    print("\n=== STORY TRANSCRIPT ===\n")
    for turn in final_state["dialogue_history"]:
        if isinstance(turn, dict):
             # Handle dict case if Pydantic model dump
             speaker = turn.get('speaker')
             dialogue = turn.get('dialogue')
             metadata = turn.get('metadata', {})
             action = metadata.get('action')
             
             print(f"[Turn {turn.get('turn_number')}] {speaker}:")
             if action:
                 print(f"  [ACTION]: {action}")
             print(f"  {dialogue}\n")
        else:
             # Handle Pydantic object
             action = turn.metadata.get('action')
             print(f"[Turn {turn.turn_number}] {turn.speaker}:")
             if action:
                 print(f"  [ACTION]: {action}")
             print(f"  {turn.dialogue}\n")
    
    print(f"\n=== CONCLUSION ===")
    print(f"Ended after {final_state['current_turn']} turns")
    print(f"Reason: {final_state.get('conclusion_reason')}")

    # Ensure directory exists
    output_dir = project_root / "Story_Output"
    output_dir.mkdir(exist_ok=True)

    # Create valid filename: Title_Scenario#[NextNumber].json
    raw_title = seed_story.get("title", "Story")
    # Sanitize: Alphanumeric + spaces/dashes/underscores only, then spaces -> underscores
    safe_title = "".join(x for x in raw_title if x.isalnum() or x in " -_").strip().replace(" ", "_")
    
    # Find the next scenario number by scanning existing files
    existing_files = list(output_dir.glob(f"{safe_title}_Scenario#*.json"))
    max_num = 0
    for f in existing_files:
        try:
            # Expected format: Title_Scenario#1.json
            # extract the number after the last '#'
            parts = f.stem.split("#")
            if len(parts) > 1 and parts[-1].isdigit():
                num = int(parts[-1])
                if num > max_num:
                    max_num = num
        except Exception:
            pass
            
    next_num = max_num + 1
    filename = f"{safe_title}_Scenario#{next_num}.json"
    
    output_path = output_dir / filename
    
    output_data = {
        "title": seed_story.get("title"),
        "seed_story": seed_story,
        "events": final_state.get("events", []),
        "metadata": {
            "total_turns": final_state["current_turn"],
            "conclusion_reason": final_state.get("conclusion_reason")
        }
    }
    
    output_path.write_text(json.dumps(output_data, indent=2, default=str))
    print(f"\nStory saved to {output_path}")

    # Save prompts
    all_logs = []
    
    # Director logs
    for log in director.logs:
        log["role"] = "Director"
        all_logs.append(log)
        
    # Character logs
    for char in characters:
        for log in char.logs:
            log["role"] = f"Character ({char.name})"
            all_logs.append(log)
            
    # Sort by timestamp
    all_logs.sort(key=lambda x: x["timestamp"])
    
    prompts_path = project_root / "prompts_log.json"
    prompts_path.write_text(json.dumps(all_logs, indent=2, default=str))
    print(f"Prompts saved to {prompts_path}")

if __name__ == "__main__":
    asyncio.run(main())
