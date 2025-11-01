from typing import Optional
from pathlib import Path
import yaml

def load_prompts() -> Optional[tuple[str, str, str, str]]:
    system_prompt_path = Path(__file__).parent / "system_prompts.yaml"

    with open(system_prompt_path, "r") as yamlFile:
        yaml_dict: dict = yaml.safe_load(yamlFile)
        return (
            yaml_dict['prompts']["interviewer_role"],
            yaml_dict['prompts']["job_description_context"],
            yaml_dict['prompts']["resume_context"],
            yaml_dict['prompts']["feedback_request"])