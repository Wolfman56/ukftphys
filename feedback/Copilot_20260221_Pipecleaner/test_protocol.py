# Copilot Feedback Baton - Protocol Test
# Objective: Demonstrate direct execution and read access to core library
import os
import sys

# Ensure repo root is available
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(REPO_ROOT)

print(f"Executing from: {REPO_ROOT}")

try:
  from ukft_sim.physics import EntropicAction
  print("✅ Successfully imported ukft_sim.physics.EntropicAction (Read Access Verify)")
except ImportError as e:
  print(f"❌ Failed to import ukft_sim.physics: {e}")
  exit(1)

print("Protocol Validation: PASSED (Green Zone Write / Core Read Verified)")
