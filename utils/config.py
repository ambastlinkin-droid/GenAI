import os

def load_system_prompt():
    """Load the system prompt from prompt.txt file"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir    = os.path.dirname(current_dir)
        prompt_path = os.path.join(root_dir,"prompt.txt")

        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()

        return content.strip()
    except FileNotFoundError:
        return "Error: prompt.txt file not found."
    
    except Exception as e:
        return f"Error loading prompt: {str(e)}"
    
def get_system_prompt():
    '''Get the system prompt with user query placeholder.'''
    return load_system_prompt()

#load SYSTEM_PROMPT at module level
SYSTEM_PROMPT = get_system_prompt()

