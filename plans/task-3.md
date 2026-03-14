## New Tool: query_api
I will implement `query_api(method, path, body)`. 
- It will use the `requests` library to make HTTP calls to the backend.
- **URL:** Constructed using `AGENT_API_BASE_URL` (defaulting to `http://localhost:42002`).
- **Auth:** It will attach the `LMS_API_KEY` (read from environment variables) to the headers (e.g., as a Bearer token or X-API-Key) to authenticate with the backend.
- **Return:** A JSON string containing `status_code` and `body`.

## System Prompt Update
I will update the system prompt to instruct the LLM on tool selection:
- Use `list_files` and `read_file` for static facts, source code, and wiki documentation.
- Use `query_api` for live system data, database item counts, and status code checks.

## Iteration Strategy
1. Implement the tool and update `agent.py`.
2. Run `uv run run_eval.py` to get the baseline score.
3. Identify failing questions (e.g., LLM choosing the wrong tool or missing keywords).
4. Tweak the system prompt and tool descriptions until all 10 local tests pass.
