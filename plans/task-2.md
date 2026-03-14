## Tool Schemas
I will define two tools:
1. `list_files(path)`: Lists directory contents.
2. `read_file(path)`: Reads text from a file.
Both will be registered as JSON schemas in the OpenAI client `tools` array.

## Agentic Loop
I will implement a `while` loop (max 10 iterations):
1. Send message history + tools to the LLM (Gemini 3 Flash).
2. If the LLM returns `tool_calls`, execute them, append the results to the message history as `tool` role messages, and record the call details for the final JSON.
3. If the LLM returns text (no tool calls), parse it for the final answer and source, combine it with the recorded tool calls, and print the JSON.

## Path Security
To prevent directory traversal (e.g., `../../etc/passwd`), I will use `os.path.abspath` and `os.path.commonpath` to ensure any requested path strictly resides within the project root directory.
