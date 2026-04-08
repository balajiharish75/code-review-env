import random
from typing import Optional, Dict, Any, List, Tuple
from src.models import Observation, Action, Reward
from src.code_snippets import CODE_SNIPPETS, TASKS
from src.graders import grade_task


class CodeReviewEnv:
    """OpenEnv-compatible code review environment."""
    
    def __init__(self, task_name: str = "review_syntax", max_steps: int = 5):
        self.task_name = task_name
        self.max_steps = max_steps
        self.current_step = 0
        self.current_snippet: Optional[str] = None
        self.current_language: Optional[str] = None
        self.current_snippet_id: Optional[str] = None
        self.current_ground_truth: List[Dict] = []
        self.done = False
        self.last_action_error: Optional[str] = None
        self.rewards: List[float] = []
    
    def reset(self) -> Observation:
        """Reset environment to initial state."""
        task_config = TASKS.get(self.task_name)
        if not task_config:
            raise ValueError(f"Unknown task: {self.task_name}")
        
        languages = task_config["languages"]
        self.current_language = random.choice(languages)
        
        snippets = CODE_SNIPPETS.get(self.current_language, {})
        
        if self.task_name == "review_syntax":
            snippet_keys = [k for k in snippets.keys() if "syntax" in k]
        elif self.task_name == "review_security":
            snippet_keys = [k for k in snippets.keys() if "security" in k]
        else:
            snippet_keys = [k for k in snippets.keys() if "comprehensive" in k]
        
        if not snippet_keys:
            snippet_keys = list(snippets.keys())
        
        self.current_snippet_id = random.choice(snippet_keys)
        self.current_snippet = snippets[self.current_snippet_id]["code"]
        self.current_ground_truth = snippets[self.current_snippet_id]["issues"]
        
        self.current_step = 0
        self.done = False
        self.rewards = []
        self.last_action_error = None
        
        return Observation(
            code_snippet=self.current_snippet,
            language=self.current_language,
            task_name=self.task_name,
            max_steps=self.max_steps,
            current_step=self.current_step,
            snippet_id=self.current_snippet_id
        )
    
    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """Execute one step."""
        self.current_step += 1
        
        if self.current_step >= self.max_steps:
            self.done = True
        
        result = grade_task(self.task_name, action.review, self.current_ground_truth)
        
        reward = result["score"]
        
        partial_bonus = 0.0
        if self.current_ground_truth:
            for issue in self.current_ground_truth:
                if "line" in issue:
                    line_str = str(issue["line"])
                    if line_str in action.review:
                        partial_bonus = 0.1
                        break
        
        reward = min(reward + partial_bonus, 1.0)
        
        if self.done and reward > 0:
            final_bonus = 0.05
            reward = min(reward + final_bonus, 1.0)
        
        self.rewards.append(reward)
        
        obs = Observation(
            code_snippet=self.current_snippet,
            language=self.current_language,
            task_name=self.task_name,
            max_steps=self.max_steps,
            current_step=self.current_step,
            snippet_id=self.current_snippet_id
        )
        
        info = {
            "issues_found": result["issues_found"],
            "issues_missed": result["issues_missed"],
            "feedback": result["feedback"],
            "last_action_error": self.last_action_error
        }
        
        return obs, reward, self.done, info
    
    def state(self) -> Dict[str, Any]:
        """Return current state."""
        return {
            "task_name": self.task_name,
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "done": self.done,
            "language": self.current_language,
            "snippet_id": self.current_snippet_id
        }
    
    def close(self):
        """Clean up resources."""
        pass
