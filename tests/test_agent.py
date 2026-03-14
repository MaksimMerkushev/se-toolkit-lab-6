import subprocess
import json

def test_agent_output():
    # Вместо "Hi" спрашиваем что-то по делу
    res = subprocess.run(["uv", "run", "agent.py", "What is in the wiki?"], capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert "answer" in data
    assert "tool_calls" in data
    # Проверяем, что в ответе есть хоть какой-то текст
    assert len(data["answer"]) > 0

def test_agent_tool_list_files():
    res = subprocess.run(["uv", "run", "agent.py", "What files are in the wiki?"], capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)

    # Проверяем, что агент использовал list_files
    tool_names = [tc["tool"] for tc in data["tool_calls"]]
    assert "list_files" in tool_names

def test_agent_tool_read_file():
    res = subprocess.run(["uv", "run", "agent.py", "How do you resolve a merge conflict?"], capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)

    # Проверяем, что агент читал файлы и нашел источник
    tool_names = [tc["tool"] for tc in data["tool_calls"]]
    assert "read_file" in tool_names
    assert "wiki" in data["source"]
