# Final Architecture and Lessons Learned

The final architecture of the system agent is designed to interact with the local filesystem and the backend API seamlessly. The agent uses a large language model to reason about user prompts and determine which tools to invoke.

We implemented three primary tools:
1. `list_files`: Allows the agent to recursively list files in a specified directory, ignoring irrelevant files like pycache or node_modules.
2. `read_file`: Enables the agent to read the exact contents of project files, which is crucial for answering questions about the codebase or wiki.
3. `query_api`: Allows the agent to make HTTP requests to the backend API. It uses the `AGENT_API_BASE_URL` environment variable to determine the target host and passes the `LMS_API_KEY` for authentication.

Lessons learned:
Throughout this lab, I learned how to integrate LLMs with external tools using function calling. I encountered challenges with rate limits and contextual token limits, which were solved by filtering out binary and compiled files from the `list_files` output and limiting the character count read by `read_file`.
I also learned how to properly handle API errors and pass them back to the LLM so it can reason about what went wrong (e.g., catching a 500 error due to a missing item_ids check).
The architecture is now robust enough to pass both local and hidden evaluation questions by relying on real data rather than hallucinated knowledge.
Overall, this lab provided a deep understanding of how to build AI-powered developer tools that can navigate a repository and interact with live services.
