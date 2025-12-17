import os
import requests

API_URL = "http://localhost:8000/analyze"

def analyze_folder(folder="tests"):
    for filename in os.listdir(folder):
        if filename.endswith(".py"):
            filepath = os.path.join(folder, filename)
            print(f"Analyzing {filepath}...")
            with open(filepath, "rb") as f:
                response = requests.post(API_URL, files={"file": f})
                print(response.json())

if __name__ == "__main__":
    analyze_folder("tests")
