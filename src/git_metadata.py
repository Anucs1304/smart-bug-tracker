import subprocess

def get_git_metadata(file_path: str):
    try:
        commit_count = int(subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD", "--", file_path],
            text=True
        ).strip())

        last_author = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%an", "--", file_path],
            text=True
        ).strip()

        last_date = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%ad", "--date=iso", "--", file_path],
            text=True
        ).strip()

        return {
            "git_commit_count": commit_count,
            "git_last_author": last_author,
            "git_last_date": last_date
        }
    except Exception:
        return {
            "git_commit_count": 0,
            "git_last_author": "unknown",
            "git_last_date": "unknown"
        }
