import subprocess
import json

def test_agent_output():
    res = subprocess.run(["uv", "run", "agent.py", "Hi"], capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert "answer" in data
    assert "tool_calls" in data
