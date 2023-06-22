import subprocess
import sys
import pip
try:
    subprocess.check_call(["pip","install","cryptography"])
except subprocess.CalledProcessError:
    print("Failure to download")