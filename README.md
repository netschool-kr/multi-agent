This repository contains the code for the LangGraph-based AI agent development project introduced in the book “Building Multi-Agent AI Systems: Workflow Orchestration with LangGraph and MCP” Through this project, you’ll get hands-on practice building AI systems for business automation using the LangGraph framework. By following the example scripts, you’ll create your own AI agents and implement step-by-step features for dialogue handling and workflow automation.

Installation
To run the examples, you’ll need a Python environment and all required libraries. Follow these steps:

Prepare your Python environment
Make sure you have Python 3.11.10 installed:

bash
Copy
Edit
$ python --version
(Optional) Create a virtual environment
For clean dependency management, it’s recommended to use venv:

bash
Copy
Edit
$ python -m venv venv
$ source venv/bin/activate      # On Windows: venv\Scripts\activate
Install required packages
From the project root directory, install everything listed in requirements.txt:

bash
Copy
Edit
(venv) $ pip install -r requirements.txt
This will automatically install LangGraph and all other necessary Python packages.

Usage
Once your environment is ready, you can run the LangGraph agent examples:

Activate your virtual environment (if not already active):

bash
Copy
Edit
$ source venv/bin/activate
Run the simplest example

bash
Copy
Edit
(venv) $ python simple_agent.py
This will launch an interactive prompt in your console where you can type messages and receive agent responses.

Interact with the agent

Type a question or command and press Enter.

For example:

text
Copy
Edit
User: Hello!
Agent: Hi there! How can I help you today?
Exit
Press Ctrl+C (or use the agent’s built-in exit command, if provided) to quit.

Through these examples, you’ll see how the agent interprets your input and follows the LangGraph-defined workflow to produce responses.

Project Structure
This repository is organized into multiple scripts and directories related to different LangGraph agent capabilities:

simple_agent.py
Defines and runs your first LangGraph-based AI agent. Serves as a minimal “hello-world” for conversation flows.

memory_agent.py
Demonstrates how to give your agent short-term memory: it remembers previous turns in the dialogue.

hitl_agent.py
Implements a Human-in-the-Loop (HITL) flow, where the agent pauses for user approval before proceeding with critical actions.

two_qa_agent.py
Shows multi-agent collaboration: two QA agents work together to answer a user’s query.

requirements.txt
Lists exactly which Python packages the project depends on.

README.md
The file you’re reading now—explains installation, usage, and each component’s purpose.

Other directories

utils/, configs/, etc.: helper functions, configuration files, additional examples (e.g. API-key loading, custom settings).

Example Interaction
Below is a sample console session when running simple_agent.py:

bash
Copy
Edit
(venv) $ python simple_agent.py
User: 안녕하세요?
Agent: Hello! How can I assist you today?
User: What is LangGraph?
Agent: LangGraph is an open-source library for linguistic graph analysis…  
User: 1 + 1 = ?
Agent: 1 + 1 equals 2.
Your actual outputs may vary depending on the language model and logic you configure. This example shows that the agent correctly follows the basic request–response cycle.

Additional Information
OpenAI API Key
Some examples (e.g. memory_agent.py) call OpenAI’s GPT models. You’ll need an OPENAI_API_KEY set as an environment variable or in a .env file:

ini
Copy
Edit
OPENAI_API_KEY=<your_api_key_here>
Obtain your key from your OpenAI account.

Other API Keys
If you use additional services (e.g. SerpAPI for web search), set their keys similarly in environment variables.

Security
No sensitive keys are checked into source control. Always manage your credentials securely (for example, via python-dotenv).

Follow these steps to clone, configure, and run the LangGraph AI agent examples. If you run into issues, refer to the corresponding chapter in the book or open an issue on this repository’s tracker. Enjoy building your AI agents!
