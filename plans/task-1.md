## LLM Provider & Model
I will use the Qwen Code API deployed on the VM. Specifically, the `qwen3-coder-plus` model, as it is recommended for this task and provides an OpenAI-compatible API.

## Agent Structure
1. **Environment**: Read configurations (`LLM_API_KEY`, `LLM_API_BASE`, `LLM_MODEL`) from `.env.agent.secret` using the `dotenv` package.
2. **Input parsing**: Use `sys.argv` to capture the question passed via CLI.
3. **LLM Interaction**: Use the official `openai` Python package to make a chat completion call to the local Qwen endpoint.
4. **Output formatting**: Print standard progress/errors to `sys.stderr`. Format the final response into a dictionary containing `answer` and `tool_calls` (empty for now) and output strictly as JSON to `sys.stdout`.
