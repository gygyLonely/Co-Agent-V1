
# Co-Agent-v1

A fast and lightweight CLI agent built on LangChain, leveraging free API keys for accessible AI automation , capable of searching the web and managing files directly from your terminal. It leverages Groq for high-speed reasoning and Tavily for real-time web search.

## Requirements
- Python 3.10 or higher
- A Groq API key (Free): https://console.groq.com
- A Tavily API key (Free): https://app.tavily.com

## Installation

### 1. Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone https://github.com/gygyLonely/Co-Agent-V1
cd Co-Agent-V1
```

### 2. Create a Virtual Environment
Follow the instructions below based on your operating system.

#### For Linux / macOS
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate
```

#### For Windows
Open Command Prompt or PowerShell:
```cmd
# Create the virtual environment
python -m venv venv

# Activate the environment
venv\Scripts\activate
```
*Note: If using PowerShell and you get an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first.*

### 3. Install Dependencies
With the virtual environment activated (you should see `(venv)` at the start of your line), install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
You must create a `.env` file to store your API keys securely.

1.  Copy the example file:
    ```bash
    cp .env.example .env
    ```
    *(On Windows Command Prompt, use: `copy .env.example .env`)*

2.  Open the `.env` file with a text editor (e.g., nano, notepad, vscode):
    ```bash
    nano .env
    ```

3.  Paste your API keys as shown below. Do not add spaces around the `=` sign.
    ```text
    GROQ_API_KEY=gsk_your_actual_groq_key_here
    TAVILY_API_KEY=tvly_your_actual_tavily_key_here
    ```

4.  Save and close the file.

#### How to get your API Keys
- **Groq**: Go to [console.groq.com/keys](https://console.groq.com/keys), log in, and click "Create API Key". This key is free and does not require a credit card.
- **Tavily**: Go to [app.tavily.com](https://app.tavily.com), sign up, and copy your API key from the dashboard. This offers a generous free tier for developers.

## Usage

Ensure your virtual environment is still activated, then run the agent:

#### Linux / macOS
```bash
python3 Co-Agent-V1.py
```

#### Windows
```cmd
python Co-Agent-V1.py
```

## Troubleshooting
- **ModuleNotFoundError**: Ensure you activated the virtual environment before running `pip install`.
- **Authentication Error**: Check that your keys in `.env` are correct and have no extra spaces.
- **Permission Denied (Linux)**: If you cannot activate the venv, ensure `python3-venv` is installed (`sudo apt install python3-venv`).


 ## Author
Created by **gygyLonely**.  
Feel free to contribute or open an issue on [GitHub](https://github.com/gygyLonely/Co-Agent-V1).    
