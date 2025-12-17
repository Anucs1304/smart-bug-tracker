import subprocess
import yaml

# Insecure subprocess call
subprocess.run("ls -l", shell=True)

# Insecure YAML load
data = yaml.load("foo: bar")
