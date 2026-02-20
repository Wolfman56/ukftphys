#!/usr/bin/env python3
import os
import time
import sys
from datetime import datetime, timezone

def start_feedback_session():
    print("----------------------------------------------------------------")
    print("   UKFT Agent Feedback Session Initiator")
    print("----------------------------------------------------------------")
    
    # 1. Get Agent Name
    agent_name = input("Enter Agent Name (e.g. Grok, Claude, Gemini): ").strip()
    if not agent_name:
        print("Error: Agent name cannot be empty.")
        sys.exit(1)
    
    # Sanitize agent name (remove spaces, special chars)
    agent_name_clean = "".join(c for c in agent_name if c.isalnum() or c in ('-', '_'))

    # 1b. Get Workflow Mode
    print("\nSelect Workflow Mode:")
    print("  [1] Manual Sync (Grok / Web Interface) - Artifacts must be copy-pasted")
    print("  [2] Direct Integration (Copilot / Cursor) - Agent has file access")
    mode_input = input("Enter Choice (1 or 2) [Default: 1]: ").strip()
    
    if mode_input == "2":
        workflow_type = "Direct Integration"
        workflow_text = """We are collaborating on the ukftphys Python coding project using direct integration.

- I have direct read/write access to the repository.
- I will inspect the code, run tools (e.g. `ls`, `grep`), and create/edit files using my toolset.
- I will commit changes directly or guide you to commit them."""
    else:
        workflow_type = "Manual Sync"
        workflow_text = """We are collaborating on the ukftphys Python coding project using strict cut-and-paste synchronization.

- I cannot write files; you paste every artifact I provide.
- Every artifact I give must be a COMPLETE file wrapped in `<DOCUMENT filename="exact/relative/path"> ... </DOCUMENT>` with a Version stamp.
- You paste → run locally (REPL/Jupyter/MadGraph) → commit/push → tell me “Checkin complete: filename”.
- I then pull live repo, verify, sync my cache, and continue."""

    # 2. Get UNIX GMT 0 Timestamp
    # We use time.time() which returns seconds since epoch (UTC/GMT)
    timestamp = int(time.time())
    
    # Format directory name
    dir_name = f"{agent_name_clean}_{timestamp}"
    
    # Determine absolute path to feedback directory
    # Assumes this script is running from the root or inside feedback/
    # We want it to be relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    feedback_dir = os.path.join(script_dir, dir_name)
    
    # 3. Create Directory
    try:
        os.makedirs(feedback_dir, exist_ok=True)
        print(f"\n[SUCCESS] Created feedback session directory:")
        print(f"   -> {feedback_dir}")
    except OSError as e:
        print(f"Error creating directory: {e}")
        sys.exit(1)

    # 4. Create a README template inside the session
    readme_path = os.path.join(feedback_dir, "SESSION_README.md")
    
    human_readable_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    try:
        with open(readme_path, "w") as f:
            f.write(f"# Feedback Session: {agent_name}\n")
            f.write(f"**Date:** {human_readable_time}\n")
            f.write(f"**Timestamp:** {timestamp}\n")
            f.write(f"**Workflow Mode:** {workflow_type}\n\n")
            f.write("## Objectives\n")
            f.write("- [ ] Review Mathematical Consistency\n")
            f.write("- [ ] Review Code Performance\n")
            f.write("- [ ] Propose Future Experiments\n\n")
            f.write("## Workflow\n")
            f.write(f"{workflow_text}\n\n")
            f.write("## Notes\n")
            f.write("(Agent to add notes here)\n")
        print(f"   -> Created template: {readme_path}")
    except OSError as e:
        print(f"Error creating template file: {e}")

    print("\n----------------------------------------------------------------")
    print("INSTRUCTIONS:")
    print("1. All feedback artifacts (markdown, code, logs) should be saved")
    print(f"   into the directory created above.")
    print("2. Commit the new directory to git when the session is complete.")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    start_feedback_session()
