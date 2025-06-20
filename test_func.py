import os

# Instead of: os.environ["DATABASE_URL"] = getpass.getpass("Enter API key for OpenAI: ")
# Change it to:
os.environ["DATABASE_URL"] = os.getenv("OPENAI_API_KEY") # Or whatever your DB URL is
# You might also want to directly use the API key from an env var
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable not set.")
    # Or raise an exception, exit, etc.
print(OPENAI_API_KEY)