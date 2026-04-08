import os
import asyncio
import textwrap
from typing import List, Optional

from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

TASKS = ["review_syntax", "review_security", "review_comprehensive"]
MAX_STEPS = 5
BENCHMARK = "code_review_env"


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


SYSTEM_PROMPTS = {
    "review_syntax": textwrap.dedent("""
        You are a code reviewer. Your task is to identify SYNTAX ERRORS in the given code snippet.
        Look for missing parentheses, brackets, quotes, indentation issues, etc.
        Provide your review as natural language text.
        If you identify an issue, mention the specific line number.
        Reply with ONLY your review text, no prefixes.
    """).strip(),
    
    "review_security": textwrap.dedent("""
        You are a code reviewer. Your task is to identify SECURITY VULNERABILITIES in the given code snippet.
        Look for SQL injection, XSS, command injection, hardcoded secrets, unsafe eval, etc.
        Provide your review as natural language text.
        If you identify an issue, mention the specific line number.
        Reply with ONLY your review text, no prefixes.
    """).strip(),
    
    "review_comprehensive": textwrap.dedent("""
        You are a code reviewer. Perform a COMPREHENSIVE code review.
        Identify ALL issues: bugs, security vulnerabilities, performance problems, code style issues.
        Provide your review as natural language text covering all categories.
        If you identify issues, mention specific line numbers.
        Reply with ONLY your review text, no prefixes.
    """).strip()
}


def get_model_review(code: str, language: str, task: str, step: int) -> str:
    prompt = f"Language: {language}\n\nCode:\n{code}\n\nProvide your code review:"
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[task]},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            stream=False
        )
        text = (completion.choices[0].message.content or "").strip()
        return text if text else "No issues found"
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return f"Error: {exc}"


async def run_task(task: str) -> None:
    from src.environment import CodeReviewEnv
    from src.models import Action
    
    env = CodeReviewEnv(task_name=task, max_steps=MAX_STEPS)
    
    log_start(task=task, env=BENCHMARK, model=MODEL_NAME)
    
    rewards = []
    steps_taken = 0
    score = 0.0
    success = False
    error_msg = None
    
    try:
        obs = env.reset()
        
        for step in range(1, MAX_STEPS + 1):
            review = get_model_review(obs.code_snippet, obs.language, task, step)
            
            obs2, reward, done, info = env.step(Action(review=review))
            
            rewards.append(reward)
            steps_taken = step
            error_msg = info.get("last_action_error")
            
            action_str = review[:80] + "..." if len(review) > 80 else review
            log_step(step=step, action=action_str, reward=reward, done=done, error=error_msg)
            
            if done:
                break
        
        score = sum(rewards) / MAX_STEPS if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= 0.3
    
    finally:
        try:
            env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
    
    log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


async def main() -> None:
    for task in TASKS:
        await run_task(task)


if __name__ == "__main__":
    asyncio.run(main())
