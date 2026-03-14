import sys
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    load_dotenv(".env.agent.secret")
    
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: uv run agent.py 'question'\n")
        sys.exit(1)
        
    question = sys.argv[1]
    
    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_API_BASE")
    )
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide concise answers."},
                {"role": "user", "content": question}
            ],
	    max_tokens=500
        )
        
        output = {
            "answer": response.choices[0].message.content.strip(),
            "tool_calls": []
        }
        print(json.dumps(output))
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
