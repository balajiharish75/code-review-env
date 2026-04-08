---
title: Code Review Env
sdk: docker
app_port: 8000
---

# Code Review Environment

A multi-language code review environment for AI agents.

## Overview

This environment provides a comprehensive code review system that supports multiple programming languages and review difficulty levels.

## Tasks

| Task | Difficulty | Description |
|------|------------|-------------|
| review_syntax | Easy | Check code for syntax errors and style issues |
| review_security | Medium | Identify security vulnerabilities and risks |
| review_comprehensive | Hard | Full code analysis including performance and best practices |

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run locally:
   ```bash
   uvicorn src.server:app --reload
   ```

3. Run with Docker:
   ```bash
   docker build -t code-review-env .
   docker run -p 8000:8000 code-review-env
   ```

## Usage

```python
from src.environment import CodeReviewEnv

env = CodeReviewEnv(task_name='review_syntax')
obs = env.reset()
obs2, reward, done, info = env.step(Action(review='Your review text'))
```

## API Endpoints

- `POST /reset` - Reset environment with task_name
- `POST /step` - Submit review text
- `GET /state` - Get current state

## Environment Variables

- `API_BASE_URL` - API endpoint for LLM (default: https://router.huggingface.co/v1)
- `MODEL_NAME` - Model identifier (default: Qwen/Qwen2.5-72B-Instruct)
- `HF_TOKEN` - HuggingFace API token
