# Manual Execution Baton
## The Human-in-the-Loop Bridge

**Role:** Internal Execution Agent (VS Code Copilot / Cursor)
**Context:** You are acting as the "Hands" for an external agent (The "Brain", e.g., Grok/Claude) who cannot run code directly.

### Protocol for Executing External Files

When the user asks you to "Run the manual baton" on a specific script (e.g., `feedback/Grok_XX/tests/test_script.py`), you must follow this strict sequence:

#### 1. Pre-Flight Review
*   **Read the Code**: Analyze the provided script.
*   **Path Correction**: The external agent likely guessed file interactions. Ensure imports (e.g., `from ukft_sim import ...`) and file paths (e.g., `experiments/`) are correct relative to the repository root.
    *   **Pro-Tip**: If a document is missing (e.g., `Paper.md`), check `papers/` or `references/`.
*   **Import Strategy**: External agents often assume experimental logic is already in the core library.
    *   **Search**: If `from ukft_sim import EntropicAction` fails, grep `experiments/` for that class/function.
    *   **Patch**: If the code is missing but the intent is clear (e.g., checking a constant), define it locally in the test script to allow the logic to run.
*   **Safety Check**: Ensure no destructive operations (rm -rf) are present.

#### 2. Hallucination Detection Heuristic (The "Stop" Button)
If the script is completely off-base, **do not fix it**. Use these metrics to decide when to reject the task and provide high-level feedback instead:
*   **The "3-Strike" Rule**: If you have to patch more than 3 non-trivial imports or missing classes to get it to run, the agent is hallucinating the library structure.
*   **Path Fantasy**: If the script references multiple files (e.g., `data/2025_run.csv`, `configs/hyperparameters.json`) that simply do not exist in the repo.
*   **API Drift**: If the script calls methods that look linguistically plausible but don't exist in the actual class definitions (e.g., calling `simulation.evolve()` when the method is `simulation.step()`).
*   **Containment Breach**: The agent is **FORBIDDEN** from modifying any files outside the current session folder. If the script requires patching the core library (`ukft_sim/`) to run, it is hallucinating the library's readiness. **Report it immediately.**

**Action**: If triggered, create `FEEDBACK_TO_AGENT.md`:
1.  **State the Confusion**: "The script assumes a library structure that refers to X, Y, Z which do not exist."
2.  **Point to Truth**: "Please review `ukft_sim/physics.py` for the actual `EntropicAction` implementation or check `experiments/` for the prototype code."

#### 3. Execution
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
