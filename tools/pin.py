#!/usr/bin/env python3
"""Pin the shortcut's install step to one commit of this fork.

Usage: python3 tools/pin.py <commit>

Rewrites the install text in src/SW-DLT.plist so the phone downloads
src/SW_DLT.py from that exact commit, checks its SHA-256, and installs the
pip versions in PINS. The commit must be pushed before you sign the shortcut.
"""
import hashlib
import plistlib
import subprocess
import sys

REPO = "vzhny/SW-DLT"
PLIST = "src/SW-DLT.plist"
PINS = [
    "chardet==7.7.0",
    "requests==2.34.2",
    "certifi==2026.11.20",
    "mutagen==1.48.1",
    "yt-dlp==2026.11.23",
    "yt-dlp-ejs==0.8.0",
    "yt-dlp-apple-webkit-jsi==0.1.1",
    "gallery-dl==1.32.21",
]


def install_text(commit, digest):
    script = "$HOME/Documents/SW-DLT/SW_DLT.py"
    return "\n".join([
        "clear",
        "hideKeyboard",
        'echo "Please wait..."',
        "python -m venv $HOME/Documents/SW-DLT/SW-DLT-ENV/",
        "source $HOME/Documents/SW-DLT/SW-DLT-ENV/bin/activate",
        f"pip install {' '.join(PINS)} -q --disable-pip-version-check --force-reinstall",
        f"curl -sL https://raw.githubusercontent.com/{REPO}/{commit}/src/SW_DLT.py -o {script}",
        # Fail closed: a missing script makes the shortcut run this install step again
        "python -c \"import hashlib,os,sys; p,h=sys.argv[1:]; "
        "hashlib.sha256(open(p,'rb').read()).hexdigest()==h or os.remove(p)\" "
        f"{script} {digest}",
        "deactivate",
        "open shortcuts://",
        "clear && cd",
        "exit",
    ])


def main():
    commit = subprocess.run(["git", "rev-parse", "--verify", sys.argv[1] + "^{commit}"],
                            capture_output=True, text=True, check=True).stdout.strip()
    source = subprocess.run(["git", "show", f"{commit}:src/SW_DLT.py"],
                            capture_output=True, check=True).stdout
    digest = hashlib.sha256(source).hexdigest()

    with open(PLIST, "rb") as f:
        doc = plistlib.load(f)
    [step] = [a["WFWorkflowActionParameters"] for a in doc["WFWorkflowActions"]
              if a["WFWorkflowActionParameters"].get("CustomOutputName") == "installDep"]
    step["WFTextActionText"] = install_text(commit, digest)
    with open(PLIST, "wb") as f:
        plistlib.dump(doc, f)
    print(f"pinned {commit} sha256={digest}")


if __name__ == "__main__":
    main()
