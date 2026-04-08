from typing import List, Dict


def grade_syntax_review(agent_review: str, ground_truth: List[Dict]) -> Dict:
    """Grade syntax error detection - easy task."""
    found = []
    missed = []
    
    agent_lower = agent_review.lower()
    
    for issue in ground_truth:
        issue_found = False
        issue_desc = issue.get('description', '').lower()
        
        if 'syntax' in issue_desc:
            keywords = ['syntax', 'parenthesis', 'bracket', 'brace', 'missing', 'error']
        else:
            keywords = [w for w in issue_desc.split() if len(w) > 3]
        
        if any(kw in agent_lower for kw in keywords):
            if 'line' in issue:
                line_str = str(issue['line'])
                if line_str in agent_review:
                    issue_found = True
        
        if issue_found:
            found.append(issue)
        else:
            missed.append(issue)
    
    score = len(found) / len(ground_truth) if ground_truth else 0.0
    
    if score == 0.0 and len(ground_truth) > 0 and len(agent_review.strip()) > 10:
        score = 0.1
    
    return {
        "score": score,
        "issues_found": found,
        "issues_missed": missed,
        "feedback": f"Found {len(found)}/{len(ground_truth)} syntax issues"
    }


def grade_security_review(agent_review: str, ground_truth: List[Dict]) -> Dict:
    """Grade security vulnerability detection - medium task."""
    found = []
    missed = []
    
    agent_lower = agent_review.lower()
    
    for issue in ground_truth:
        issue_found = False
        issue_desc = issue.get('description', '').lower()
        
        security_keywords = ['sql injection', 'xss', 'injection', 'vulnerability', 'unsafe', 
                           'eval', 'sanitize', 'escape', 'command', 'injection']
        
        if any(kw in agent_lower for kw in security_keywords):
            if any(word in issue_desc for word in issue_desc.split()):
                issue_found = True
        
        if issue_found:
            found.append(issue)
        else:
            missed.append(issue)
    
    score = len(found) / len(ground_truth) if ground_truth else 0.0
    
    if score == 0.0 and len(ground_truth) > 0:
        if len(agent_review.strip()) > 20:
            score = 0.1
    
    return {
        "score": score,
        "issues_found": found,
        "issues_missed": missed,
        "feedback": f"Found {len(found)}/{len(ground_truth)} security issues"
    }


def grade_comprehensive_review(agent_review: str, ground_truth: List[Dict]) -> Dict:
    """Grade full code review - hard task."""
    found = []
    missed = []
    
    agent_lower = agent_review.lower()
    
    type_weights = {"security": 0.4, "bug": 0.3, "performance": 0.2, "style": 0.1}
    weighted_score = 0.0
    
    for issue in ground_truth:
        issue_found = False
        issue_type = issue.get('type', 'style')
        issue_desc = issue.get('description', '').lower()
        
        type_keywords = {
            "security": ['sql', 'injection', 'xss', 'vulnerability', 'unsafe', 'sanitize'],
            "bug": ['bug', 'error', 'wrong', 'incorrect', 'issue', 'fix'],
            "performance": ['performance', 'slow', 'inefficient', 'optimize', 'comprehension'],
            "style": ['style', 'convention', 'naming', 'guard', 'const', 'let']
        }
        
        keywords = type_keywords.get(issue_type, type_keywords['style'])
        
        if any(kw in agent_lower for kw in keywords):
            if any(word in agent_lower for word in issue_desc.split() if len(word) > 3):
                issue_found = True
        
        if issue_found:
            found.append(issue)
            weighted_score += type_weights.get(issue_type, 0.1)
        else:
            missed.append(issue)
    
    max_score = sum(type_weights.values())
    score = min(weighted_score / max_score, 1.0) if max_score > 0 else 0.0
    
    if score == 0.0 and len(ground_truth) > 0 and len(agent_review.strip()) > 30:
        score = 0.1
    
    return {
        "score": score,
        "issues_found": found,
        "issues_missed": missed,
        "feedback": f"Found {len(found)}/{len(ground_truth)} issues (weighted score: {score:.2f})"
    }


def grade_task(task_name: str, agent_review: str, ground_truth: List[Dict]) -> Dict:
    """Route to appropriate grader."""
    graders = {
        "review_syntax": grade_syntax_review,
        "review_security": grade_security_review,
        "review_comprehensive": grade_comprehensive_review
    }
    
    grader = graders.get(task_name)
    if not grader:
        return {"score": 0.0, "issues_found": [], "issues_missed": [], "feedback": "Unknown task"}
    
    return grader(agent_review, ground_truth)
