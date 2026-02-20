# Manual Execution Baton
## The Human-in-the-Loop Bridge

**Role:** Internal Execution Agent (VS Code Copilot / Cursor)
**Context:** You are acting as the "Hands" for an external agent (The "Brain", e.g., Grok/Claude) who cannot run code directly.

### Protocol for Executing External Files

When the user asks you to "Run the manual baton" on a specific script (e.g., `feedback/Grok_XX/tests/test_script.py`), you must follow this strict sequence:

#### 1. Pre-Flight Review
*   **Read the Code**: Analyze the provided script.
*   **Path Correction**: The external agent likely guessed file interactions. Ensure imports (e.g., `from ukft_sim import ...`) and file paths (e.g., `experiments/`) are correct relative to the repository root.
*   **Safety Check**: Ensure no destructive operations (rm -rf) are present.

#### 2. Execution
*   **Run the Script**: Execute the script in the terminal from the **Repository Root**.
    ```bash
    python3 feedback/Path/To/Script.py
    ```
*   **Capture Output**: Save the stdout/stderr.

#### 3. Organization
*   **Artifacts**: If the script generates plots or data, ensure they are saved within the same `feedback/Agent_Session/` directory (or a `results/` folder therein), NOT cluttering the root.

#### 4. The Explainer (Crucial Step)
*   **Create a Report**: Generate a `README_TEST_RESULTS.md` in the script's directory.
*   **Structure**:
    *   **Objective**: What was the external agent trying to test?
    *   **Modifications**: Did you have to fix imports/paths?
    *   **Results**: Paste the terminal output or summary.
    *   **Interpretation**: Did it pass? What does this prove about the hypothesis?
    *   **Next Steps**: Suggest what the external agent should do next.
