import os
import sys
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from groq import APITimeoutError, APIConnectionError

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────────
# TAVILY CLIENT
# ─────────────────────────────────────────────

try:
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
except Exception as e:
    print(f"[Co-Agent-v1] Failed to initialize Tavily client: {e}")
    sys.exit(1)

# ─────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────

@tool
def internet_search(query: str) -> str:
    """Search the internet for up-to-date information."""
    try:
        results = tavily.search(query, max_results=3)
        return str(results)
    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def write_file(filename: str, content: str) -> str:
    """Write content to a file. Only allowed in the current working directory."""
    if "/" in filename or "\\" in filename or ".." in filename:
        return "Error: writing outside the current directory is not allowed."
    try:
        with open(filename, "w") as f:
            f.write(content)
        return f"File '{filename}' created successfully."
    except PermissionError:
        return f"Error: permission denied for '{filename}'."
    except OSError as e:
        return f"Error: could not write file: {str(e)}"
    except Exception as e:
        return f"Unexpected error while writing file: {str(e)}"

# ─────────────────────────────────────────────
# LLM
# ─────────────────────────────────────────────

try:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
        timeout=45,
        max_retries=2,
    )
except Exception as e:
    print(f"[Co-Agent-v1] Failed to initialize LLM: {e}")
    sys.exit(1)

# ─────────────────────────────────────────────
# AGENT
# Only use tools when explicitly needed.
# This prevents llama from calling tools on simple messages like "hello".
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are Co-Agent-v1, a helpful console AI assistant.
Only use tools when explicitly needed:
- Use 'internet_search' only when the user asks for current or real-time information.
- Use 'write_file' only when the user asks to save or create a file.
For casual conversation, greetings, coding questions, or general knowledge, just respond normally without using any tools."""

try:
    agent = create_react_agent(
        model=llm,
        tools=[internet_search, write_file],
        prompt=SYSTEM_PROMPT,
    )
except Exception as e:
    print(f"[Co-Agent-v1] Failed to create agent: {e}")
    sys.exit(1)

# ─────────────────────────────────────────────
# MEMORY SETTINGS
# Keep only the last 20 messages to stay light on memory.
# 20 messages ~ 4k-10k tokens, well within Groq's 32k context window
# and easy on low-to-mid range machines.
# ─────────────────────────────────────────────

MAX_MESSAGES = 20

# ─────────────────────────────────────────────
# CHAT LOOP
# ─────────────────────────────────────────────

print("=" * 40)
print("  Co-Agent-v1 — Console AI Agent")
print("  Type 'exit' to quit.")
print("=" * 40 + "\n")

conversation_history = []

while True:
    try:
        user_input = input("You: ")
    except (KeyboardInterrupt, EOFError):
        print("\n[Co-Agent-v1] Goodbye.")
        break

    if user_input.strip() == "":
        continue

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("[Co-Agent-v1] Goodbye.")
        sys.exit(0)

    conversation_history.append({"role": "user", "content": user_input})

    trimmed_history = conversation_history[-MAX_MESSAGES:]

    try:
        result = agent.invoke({"messages": trimmed_history})
        response = result["messages"][-1].content

    except (APITimeoutError, TimeoutError):
        print("\n[Co-Agent-v1] Request timed out, please try again.\n")
        conversation_history.pop()
        continue

    except APIConnectionError:
        print("\n[Co-Agent-v1] Connection error, check your internet and try again.\n")
        conversation_history.pop()
        continue

    except KeyboardInterrupt:
        print("\n[Co-Agent-v1] Response interrupted.")
        conversation_history.pop()
        continue

    except Exception as e:
        # Catch Groq tool call format errors specifically
        if "tool_use_failed" in str(e) or "tool call validation failed" in str(e):
            print("\n[Co-Agent-v1] Model had a tool formatting error, retrying without tools...\n")
            conversation_history.pop()
            # Retry the same message but with a direct LLM call, bypassing tools
            try:
                direct_response = llm.invoke(trimmed_history)
                response = direct_response.content
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                print(f"\nCo-Agent-v1: {response}\n")
            except Exception as retry_error:
                print(f"\n[Co-Agent-v1] Retry also failed: {str(retry_error)}\n")
            continue

        print(f"\n[Co-Agent-v1] Something went wrong: {str(e)}\n")
        conversation_history.pop()
        continue

    conversation_history.append({"role": "assistant", "content": response})
    print(f"\nCo-Agent-v1: {response}\n")
