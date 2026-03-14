import sys
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# --- Security & Tools ---
PROJECT_ROOT = os.path.abspath(".")

def is_safe_path(target_path):
    abs_target = os.path.abspath(os.path.join(PROJECT_ROOT, target_path))
    return os.path.commonpath([PROJECT_ROOT, abs_target]) == PROJECT_ROOT

def list_files(path):
    if not is_safe_path(path):
        return "Error: Access denied."
    target = os.path.join(PROJECT_ROOT, path)
    try:
        if not os.path.isdir(target):
            return f"Error: {path} is not a directory."
        return "\n".join(os.listdir(target))
    except Exception as e:
        return f"Error: {str(e)}"

def read_file(path):
    if not is_safe_path(path):
        return "Error: Access denied."
    target = os.path.join(PROJECT_ROOT, path)
    try:
        if not os.path.isfile(target):
            return f"Error: {path} is not a file."
        with open(target, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

# --- Tool Schemas ---
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file content.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        }
    }
]

def main():
    load_dotenv(".env.agent.secret")
    
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: uv run agent.py 'question'\n")
        sys.exit(1)
        
    question = sys.argv[1]
    client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_API_BASE"))
    
    system_prompt = """You are a documentation agent. 
CRITICAL: You MUST use tools (list_files, read_file) to find answers in the wiki/ directory.
Always return final answer as JSON: {"answer": "...", "source": "..."}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    executed_tool_calls = []
    max_loops = 10
    
    for _ in range(max_loops):
        try:
            response = client.chat.completions.create(
                model=os.getenv("LLM_MODEL"),
                messages=messages,
                tools=TOOLS,
                max_tokens=1000 # Ограничиваем, чтобы не вылетала ошибка 402
            )
            
            # ПРОВЕРКА: Если OpenRouter прислал пустой список choices
            if not response.choices:
                sys.stderr.write(f"API Error: Received empty choices. Full response: {response}\n")
                sys.exit(1)
                
            msg = response.choices[0].message
            messages.append(msg)

            if msg.tool_calls:
                for tc in msg.tool_calls:
                    name = tc.function.name
                    args = json.loads(tc.function.arguments)
                    
                    res = list_files(args["path"]) if name == "list_files" else read_file(args["path"])
                    
                    executed_tool_calls.append({"tool": name, "args": args, "result": res[:200]})
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": res})
            else:
                # Финальный ответ
                try:
                    content = msg.content.strip().replace('```json', '').replace('```', '').strip()
                    data = json.loads(content)
                    print(json.dumps({
                        "answer": data.get("answer", msg.content),
                        "source": data.get("source", "Unknown"),
                        "tool_calls": executed_tool_calls
                    }))
                except:
                    print(json.dumps({
                        "answer": msg.content,
                        "source": "Unknown",
                        "tool_calls": executed_tool_calls
                    }))
                return

        except Exception as e:
            sys.stderr.write(f"Loop Error: {str(e)}\n")
            sys.exit(1)

if __name__ == "__main__":
    main()
