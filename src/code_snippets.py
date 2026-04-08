CODE_SNIPPETS = {
    "python": {
        "syntax_error_1": {
            "code": "def greet(name:\n    return f\"Hello, {name}\"",
            "issues": [
                {
                    "type": "syntax_error",
                    "line": 1,
                    "description": "Missing closing parenthesis in function definition"
                }
            ]
        },
        "security_1": {
            "code": "def get_user(user_id):\n    query = f\"SELECT * FROM users WHERE id = {user_id}\"\n    cursor.execute(query)\n    return cursor.fetchone()",
            "issues": [
                {
                    "type": "security",
                    "line": 2,
                    "description": "SQL injection vulnerability - user input directly interpolated into query"
                }
            ]
        },
        "comprehensive_1": {
            "code": "def process_items(items):\n    result = []\n    for item in items:\n        if item.get('active'):\n            result.append(item)\n    return result\n\ndef main():\n    data = get_all_items()\n    processed = process_items(data)\n    print(processed)",
            "issues": [
                {
                    "type": "bug",
                    "line": 3,
                    "description": "Using .get() on None if item could be None"
                },
                {
                    "type": "performance",
                    "line": 3,
                    "description": "Using append in loop instead of list comprehension"
                },
                {
                    "type": "style",
                    "line": 9,
                    "description": "Undefined function 'get_all_items' - likely missing import or definition"
                }
            ]
        }
    },
    "javascript": {
        "syntax_error_1": {
            "code": "function calculateSum(a, b {\n    return a + b;\n}",
            "issues": [
                {
                    "type": "syntax_error",
                    "line": 1,
                    "description": "Missing closing parenthesis in function parameters"
                }
            ]
        },
        "security_1": {
            "code": "function displayMessage(userInput) {\n    document.getElementById('message').innerHTML = userInput;\n}",
            "issues": [
                {
                    "type": "security",
                    "line": 2,
                    "description": "XSS vulnerability - user input directly assigned to innerHTML without sanitization"
                }
            ]
        },
        "comprehensive_1": {
            "code": "function fetchUsers() {\n    const users = [];\n    for (let i = 0; i < users.length; i++) {\n        console.log(users[i].name);\n    }\n    fetch('/api/users').then(response => response.json());\n}",
            "issues": [
                {
                    "type": "style",
                    "line": 3,
                    "description": "Use for-of loop or forEach instead of traditional for loop"
                },
                {
                    "type": "performance",
                    "line": 5,
                    "description": "Unused promise - result of fetch is not handled or stored"
                }
            ]
        }
    }
}

TASKS = {
    "review_syntax": {
        "languages": ["python", "javascript"],
        "difficulty": "easy"
    },
    "review_security": {
        "languages": ["python", "javascript"],
        "difficulty": "medium"
    },
    "review_comprehensive": {
        "languages": ["python", "javascript"],
        "difficulty": "hard"
    }
}