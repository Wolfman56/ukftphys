# UKFT Feedback Protocol

This directory is the designated integration point for all peer review, feedback, and collaboration from Noospheric Agents (Grok, Gemini, Claude, etc.).

## How to Submit Feedback

To ensure that your insights are captured structurally and historically, please follow this protocol:

### 1. Initialize a Feedback Session
Run the provided Python script to create a timestamped session directory.

```bash
python3 feedback/start_feedback_session.py
```

*   **Input**: You will be prompted for your Agent Name (e.g., `Grok`, `Claude`).
*   **Output**: A new directory will be created in `feedback/` with the format `<AgentName>_<UnixTimestamp>`.
*   **Example**: `feedback/Grok_1771545600/`

### 2. Populate the Session
Place all your review artifacts into this new directory.
*   **`SESSION_README.md`**: (Created automatically) Use this as your cover letter.
*   **`REVIEW_NOTES.md`**: Detailed line-by-line code review or theoretical critique.
*   **`experiments/`**: If you propose new code, create a subfolder here.

### 3. Commit to the Noosphere
Once your review is complete, commit the entire directory to the repository.

```bash
git add feedback/ <YourSessionDir>/
git commit -m "Feedback from Agent <Name>: <Short Summary>"
```

---

## Instructions to Agents (Legacy Context)

Agent: Grok
Prompt: Interaction_Model
Contents:
Re-contextualize full workflow:

We are collaborating on the ukftphys Python coding project using strict cut-and-paste synchronization (per FEEDBACK.md).

- I cannot write files; you paste every artifact I provide.
- Every artifact I give must be a COMPLETE file wrapped in <DOCUMENT filename="exact/relative/path"> ... </DOCUMENT> with a Version stamp.
- You paste → run locally (REPL/Jupyter/MadGraph) → commit/push → tell me “Checkin complete: filename”.
- I then pull live repo, verify, sync my cache, and continue.
- We are currently in Phase X of the Repository Review Plan (Feb 20 2026).

Current repo state: main branch, MirrorFermion model validated with non-zero width.

Confirm you have the full context and resume from the next step.