RULE_DESCRIPTIONS = {
    # Bandit rules
    "B101": "Avoid using assert statements for data validation in production code.",
    "B102": "Do not use exec(); consider safer alternatives.",
    "B103": "Avoid using eval(); it can execute arbitrary code.",
    "B104": "Do not hardcode passwords or secrets in code.",
    "B301": "Avoid pickle for serialization; use json or safer libraries.",
    "B303": "Use yaml.safe_load() instead of yaml.load() to prevent arbitrary code execution.",
    "B403": "Avoid importing subprocess directly; use safer wrappers.",
    "B404": "Avoid importing os.system; use subprocess.run() instead.",
    "B602": "Avoid shell=True in subprocess calls; use explicit argument lists.",
    "B607": "Ensure input validation when using regular expressions.",
    "B608": "Validate SQL queries properly to prevent SQL injection.",
    "B110": "Do not hardcode passwords or secrets in code.",
    "B320": "Avoid insecure random functions; use secrets or SystemRandom.",
    "B501": "Do not use requests with verify=False; enable SSL certificate verification.",
    "B506": "Avoid unsafe yaml.load() usage; prefer safe_load().",
    
    # Pylint rules
    "E0001": "Syntax error detected; fix the code structure.",
    "E1120": "Function call missing required positional arguments.",
    "E1136": "Value used is unsubscriptable; check variable type.",
    "W0612": "Remove unused variables to clean up code.",
    "W0613": "Remove unused function arguments.",
    "W0702": "Avoid bare except clauses; catch specific exceptions.",
    "W0703": "Avoid catching too general exceptions.",
    "C0103": "Follow naming conventions for variables and functions.",
    "C0114": "Add module docstring for clarity.",
    "C0116": "Add function or method docstring.",
    "R0912": "Refactor functions with too many branches for readability.",
    "R0915": "Refactor functions with too many statements.",
    "R0913": "Reduce number of function arguments for simplicity.",
    "R0902": "Class has too many instance attributes; consider refactoring.",
    "R0904": "Class has too many public methods; simplify design.",
    "C0301": "Line too long; break into shorter lines.",
    "C0303": "Remove trailing whitespace.",
    "C0411": "Imports are not in alphabetical order; fix import order.",
    "E2511": "Method defined outside of a class; ensure methods are properly scoped.",
    "C0304": "Remove unnecessary blank lines at the end of the file.",
    "C0305": "Remove trailing newlines; keep file endings clean."
}


def get_description(rule_id: str) -> str:
    """
    Return a fix suggestion for a given rule ID.
    If no suggestion is available, return a default message.
    """
    return RULE_DESCRIPTIONS.get(rule_id, "No automated fix available for this rule.")

