Building Multi‑Agent AI Systems – Code Examples
Building Multi-Agent AI Systems: Workflow Orchestration with LangGraph and MCP is a hands-on guide to creating AI agents that work together to automate business workflows.
This repository contains the example code for the LangGraph-based multi-agent project introduced in the book​. By following along, you’ll learn how to build intelligent agents that can converse with users, collaborate with other agents, and leverage external tools via the Model-Context Protocol (MCP) to drive business automation.

Introduction
The book Building Multi-Agent AI Systems walks through designing AI agents using two key frameworks: LangGraph and MCP. LangGraph is a graph-based AI agent framework (developed by the LangChain team) for orchestrating complex workflows as interconnected nodes​. It serves as the “brain” of your agent, controlling dialogue flow and decision-making. MCP (Model-Context Protocol) is a standardized protocol for connecting AI agents to external tools and services​
 – think of it as a universal interface that lets your agents call APIs, databases, or other systems. In this project, LangGraph provides the workflow structure, while MCP (via the FastMCP library) acts as the bridge to a universe of external tools​. Goals of the Book: By the end of the book, you will have a practical understanding of how to build multi-agent AI systems for real-world business automation. Starting from a simple conversational agent, each chapter adds new capabilities – memory, human-in-the-loop oversight, multi-agent collaboration, and tool integrations – culminating in fully-fledged agents that can coordinate workflows and interact with external services. The repository’s code allows you to get hands-on experience with these concepts​
github.com
, creating your own AI agents step by step for tasks like chat automation, workflow orchestration, and data retrieval.
Target Audience
This project is intended for AI developers and enthusiasts interested in large language model (LLM) based agents and workflow automation. If you want to learn how to build intelligent chatbots or multi-agent systems that integrate with real tools, this repository will guide you. The examples assume familiarity with Python and basic concepts of AI/ML. Knowledge of APIs and JSON will help in understanding tool integration (MCP) but is not required to get started. Whether you are a practitioner looking to automate business processes or a researcher exploring agent orchestration, you’ll find value in the clear, incremental approach – from a “hello world” agent to complex multi-agent workflows. Each chapter’s code is organized to teach a specific concept, making it easy to follow along and experiment.
Setup and Installation
To run the examples, you’ll need a Python 3 environment with the required libraries installed. Follow the steps below to set up your development environment:
Python Installation: Ensure you have Python 3.11.10 installed on your system​
github.com
. You can check this by running python --version. Earlier or later Python 3.11.x versions may work, but 3.11.10 is recommended for compatibility.
Clone the Repository: Download or clone this repository from GitHub:
bash
Copy
Edit
git clone https://github.com/netschool-kr/multi-agent.git
cd multi-agent
Create a Virtual Environment (optional): It’s good practice to use a virtual environment to isolate dependencies. You can create one using Python’s built-in venv:
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install Dependencies: Use pip to install all required packages:
bash
Copy
Edit
pip install -r requirements.txt
This will install LangGraph, FastMCP, and all other necessary Python libraries listed in requirements.txt​
github.com
. (The LangGraph and MCP libraries are included here, so you don’t have to install them separately.)
Configure API Keys: Some examples use external services like OpenAI’s GPT models and third-party APIs. For instance, the agents use OpenAI GPT-4 or GPT-3.5 for language understanding, so you’ll need an OpenAI API key. If you plan to run those examples, set your OpenAI API Key as an environment variable or in a .env file:
bash
Copy
Edit
export OPENAI_API_KEY="your-openai-key-here"
Similarly, if you use other services (e.g. the Tavily search API for live web search, or YouTube API for transcripts), obtain those API keys and set them as environment variables (e.g. TAVILY_API_KEY)​
github.com
. No sensitive keys are included in this repo, so you must configure these on your own. (See chapter notes for which examples require additional keys.)
With Python and dependencies set up and any necessary API keys configured, you’re ready to run the example agents.
Running the Examples
Once your environment is prepared, you can start exploring the LangGraph agent examples. Make sure to activate your virtual environment (source venv/bin/activate) if you created one. Each example is a standalone Python script demonstrating a specific concept. For example, to run the simplest agent:
bash
Copy
Edit
(venv) $ python simple_agent.py
This will launch an interactive prompt in your console. You can type messages as the User, and the Agent (powered by an LLM via LangGraph) will respond according to its programmed workflow. For example:
makefile
Copy
Edit
User: Hello!
Agent: Hi there! How can I help you today?
Now you can ask the agent to do something or answer a question. Try typing a query, such as:
csharp
Copy
Edit
User: What is LangGraph?
Agent: LangGraph is an open-source library for orchestrating language model workflows as graphs...&#8203;:contentReference[oaicite:8]{index=8}
You can continue the dialogue, and the agent will keep responding. To exit the session, press Ctrl+C (or use a built-in exit command if the agent defines one)​
github.com
. Each script in this repository is designed to be run similarly. For instance, memory_agent.py, hitl_agent.py, etc., can all be executed from the command line to observe different agent behaviors. The console output will illustrate how each enhancement (memory, HITL, multi-agent, etc.) affects the agent’s interaction pattern. Through these examples, you’ll see how user inputs are processed and how the agent’s replies are generated according to the LangGraph-defined workflow. Below is a sample console session (actual output may vary depending on your AI model and configuration):
bash
Copy
Edit
(venv) $ python simple_agent.py
User: 안녕하세요?  
Agent: Hello! How can I assist you today?  
User: 1 + 1 = ?  
Agent: 1 + 1 equals 2.  
This shows the agent responding to a greeting (in Korean) and a simple arithmetic question​
github.com
. The agent’s replies are composed by the underlying language model following the structure we defined in the code. Feel free to experiment with each example. If an agent uses tools (via MCP), you might need to run or configure the corresponding tool server (see notes below). Most simple examples (like the basic agent, memory agent, etc.) will run out-of-the-box as long as the required API keys are set.
Repository Structure and Chapter Mapping
The repository is organized by scripts that correspond to various chapters of the book. Each chapter introduces new concepts and the code here provides the implementation for those. Below is a chapter-wise mapping of key files to the book content:
Chapter 2: Getting Started with LangGraph – Your first LangGraph Agent.
Code: simple_agent.py – a minimal Hello World conversational agent using LangGraph​
github.com
. This script defines a basic agent workflow and opens an interactive loop. It demonstrates how an LLM-powered agent perceives user input and generates a response autonomously.
Chapter 5: LangGraph Core Concepts – Understanding nodes, edges, and flow.
Code: basic_flow.py – a simple workflow graph example. This script isn’t an interactive chatbot but shows how to create a StateGraph, define node functions, and control flow between steps. It’s used to illustrate LangGraph fundamentals like nodes execution and conditional edges (as discussed in Chapter 5). Use this to see a static workflow in action (useful for learning how LangGraph orchestrates steps).
Chapter 6: State Management and Memory – Adding memory to an agent.
Code: memory_agent.py (and memory.py) – a chatbot agent with short-term memory​
github.com
. This example illustrates how the agent can remember previous user inputs in the conversation. Internally it uses LangGraph’s state persistence (checkpoints) to store dialogue history. By running this script, you can have a multi-turn conversation where the agent recalls context from earlier turns (e.g., remembering names or preferences mentioned earlier). Chapter 6 explains how state is stored and retrieved, and this code demonstrates it in practice​.
Chapter 7: Human-in-the-Loop Workflows – Inserting human approval steps.
Code: hitl_agent.py – an agent that implements a Human-in-the-Loop (HITL) checkpoint​. In critical workflows, the agent should pause and ask for human confirmation before proceeding (for example, before sending an email or making an irreversible action). This script uses LangGraph’s checkpointing mechanism to pause the agent’s execution and wait for a “human approval” (simulated in code or via console input). Chapter 7 covers how checkpoints and state persistence allow pausing and resuming agent flows​. Running hitl_agent.py, you’ll see the agent stop at a certain step and prompt for approval before continuing.
Chapter 8: Multi-Agent Collaboration – Agents working together & workflow control.
Code: two_qa_agent.py – an example of multi-agent collaboration​
github.com
. This script sets up two question-answering agents that cooperate to answer a user’s query. For instance, one agent might fetch information while the other formulates the answer. It demonstrates LangGraph’s capability to manage multiple agents (as nodes in a graph) within one workflow. Chapter 8 discusses how to coordinate multiple agents and control the flow between them (including techniques like dynamic routing of queries)​. By running two_qa_agent.py, you can witness two AI agents chatting behind the scenes to come up with a response. Additional: Chapter 8 also introduces more complex multi-agent patterns. The repository includes project_agent.py, which showcases a scenario with multiple specialized agents (for example, a “researcher” agent, a “summarizer” agent, etc., orchestrated by a supervisor). While not explicitly named in the chapter text, you can explore project_agent.py to see a more elaborate workflow where an agent breaks down a task and delegates subtasks to other agents (this reflects the dynamic routing concept discussed in the book, where an agent’s plan can route through different nodes based on the query)​.
Chapter 9: Integrating External Tools with MCP – Connecting to databases, APIs, etc.
Chapter 9 covers how to extend your agents beyond the closed LLM environment by using MCP to call external tools and services​. In this chapter, the book introduces the concept of an MCP client and server, and simple examples of tool integration (like querying a database). The code user_db_server.py and user_db_client.py are practical implementations of this concept:
Code: user_db_server.py – a simple FastMCP tool server that exposes a mock user database lookup (maps user IDs to names)​. This corresponds to the book’s example of creating a custom MCP server (Anthropic’s Model-Context Protocol reference implementation) to handle a specific tool function​.
Code: user_db_client.py – an example LangGraph agent that acts as an MCP client to the above server​. It shows how the agent can launch the user_db_server (or connect to it) and request a tool function (e.g., get a user’s name by ID) as part of its workflow. Chapter 9 walks through this process of integrating a database call into an agent’s reasoning.
These scripts demonstrate the basics of MCP: the server provides a JSON-RPC interface to a function, and the agent (client) calls it as needed. To run this example, you can start the server in one terminal (python user_db_server.py) and the client agent in another, or let the client spawn the server automatically (as the code is often set up to do). The client will query the server and incorporate the result into the agent’s response.
Chapter 10: Building a LangGraph Agent System (MCP Integration) – End-to-end multi-agent workflows using tools.
In Chapter 10, the book brings together multiple agents and external tool calls into unified workflows. It provides richer workflow examples using MCP in action, such as:
Forex Trading Assistant: An agent that obtains real-time forex pricing, evaluates risk, and suggests trade actions.
Code: forex_server.py and forex_client.py – this pair showcases a scenario of connecting to a financial data source. forex_server.py might simulate or connect to a pricing service (and possibly perform risk analysis), while forex_client.py is a LangGraph agent that uses that service. The book describes this example as “Forex Trading – real-time pricing, risk assessment, trade signal analysis using MCP”​. By running these, you can see an agent pulling live or simulated forex data and making decisions based on it.
(Additional) finance.py – a script that contains a financial analysis agent (for example, it could summarize financial news or perform calculations). This may relate to the forex scenario or other finance-related workflows discussed around Chapter 10. While not explicitly detailed in the text, it’s provided as a reference implementation of how an agent might handle finance domain tasks.
These examples underscore how LangGraph agents can coordinate with external services: the agent might query an API for data, then use that data in its reasoning to produce an answer or decision. Chapter 10’s code gives you a template for structuring such agent+tool interactions using the MCP client/server pattern.
Chapter 11: Building Custom Tool Servers (FastMCP) – Developing and integrating your own tools.
Chapter 11 dives deeper into FastMCP, a Python framework for rapidly creating MCP servers​. It walks through building two useful tool services and integrating them with a LangGraph agent:
Web Search Tool Server – uses the Tavily real-time search API to answer queries with up-to-date information.
Code: tavily_search.py – this script creates a FastMCP server that wraps the Tavily search client​. It exposes a function (e.g., search_web(query)) that the agent can call to perform live web searches. The Tavily API key is required for this to work. In the book, this is the “Web Search tool server” example​.
YouTube Transcript Tool Server – uses the YouTube Transcript API to fetch video transcripts for summarization.
Code: yt_transcript.py – this is another FastMCP server script which provides a function (e.g., get_transcript(video_url)) to retrieve YouTube video transcripts​. It’s useful when an agent needs to summarize or analyze video content.
Alongside these, Chapter 11 shows how to run multiple MCP servers and connect them: it introduces the MultiServerMCPClient, which can manage several tool servers concurrently​. The code multiserver_mcpclient.py demonstrates this – it configures two servers (the Tavily search and YouTube transcript services) and spawns them, then collects their tool interfaces for the LangGraph agent to use​. When you run this example, the LangGraph agent will be able to call both search_web and get_transcript tools seamlessly in one workflow (for example, searching the web and then getting a related video’s transcript)​. Additional files:
news_mcp_server.py and news_summarize.py – These scripts are related to a news summarization scenario (possibly an earlier or alternative example to Tavily). The news_mcp_server.py might serve news articles or headlines (perhaps using a news API or static data), and news_summarize.py would be an agent that fetches news via that server and then summarizes it using the LLM. This is analogous to the web search example but focused on news content. Running these can show an agent that gathers external info (news) and summarizes it.
llm_query_interpreter.py and llm_risk_analyzer.py – These are utility agent components introduced to support tool interactions and HITL. For instance, an agent might use llm_query_interpreter.py to parse or classify user requests (deciding which tool or agent should handle it), and use llm_risk_analyzer.py to evaluate if a response is potentially risky or needs human review. These components tie into the workflow when creating more advanced agents (for example, before executing an action, run a risk analysis step, and possibly trigger the HITL checkpoint if the risk is high).
Chapter 12: Deploying an Interactive Chatbot – Agent servers and streaming responses.
By Chapter 12, the book demonstrates how to turn your agent into a deployed service (e.g., a chatbot accessible via web or API). The repository includes a set of files for a Chatbot application:
Code: chatbot_server.py and chatbot_client.py – These create a simple client-server setup for the AI agent. The server might be a FastAPI or Flask app (or even a simple socket server) that runs a LangGraph agent in the background. The client script can send a query to the server and get a response. This separation shows how you might deploy the agent so that external applications (like a web frontend) can interact with it.
Code: chatbot_server_sse.py and chatbot_client_sse.py – An enhanced version of the above using Server-Sent Events (SSE) for real-time streaming responses. SSE allows the agent’s response to be sent incrementally (token by token) to the client. In practice, this means as the LLM generates an answer, the words can stream in real-time (much like how ChatGPT streams its answers). The book’s conclusion highlights this approach as a way to create interactive, responsive AI systems​
file-1yym3krchu2qjvkmpjderx
.
Code: asyncio_exam.py – A small example showing how to use Python’s asyncio with LangGraph/MCP. Since integrating multiple servers and streaming involves asynchronous operations, this script provides a minimal illustration of running asynchronous tasks (perhaps querying two tools in parallel or handling concurrent user requests). It’s a helpful reference for understanding the asynchronous patterns used in the multi-server client and SSE server.
Chapter 13: E-Commerce Agent Case Study – Product recommendation & inventory check.
The final chapter presents a comprehensive case study: an E-commerce assistant that can recommend products and check inventory in real-time​
file-1yym3krchu2qjvkmpjderx
​
file-1yym3krchu2qjvkmpjderx
. This example brings together everything – a multi-step agent, external tool integration via MCP, and a realistic business scenario:
Code: ecommerce_service_server.py – a FastMCP server providing two tools, Product Recommendation and Inventory Check. It simulates a product database and inventory system, exposing functions like recommend_product(criteria) and check_inventory(product_id). In the book, this corresponds to building an MCP server named "ECommerceService" with those tools​.
Code: ecommerce_agent_client.py – the LangGraph agent that acts as the client to the above service​. This agent can handle user queries like "Find me a cheap gaming laptop that’s in stock." It will invoke the recommendation tool to get a list of products, then call the inventory tool to filter by stock, and finally compose an answer for the user​
file-1yym3krchu2qjvkmpjderx
​
file-1yym3krchu2qjvkmpjderx
. The agent is essentially orchestrating a mini-workflow: user query -> call tool1 -> call tool2 -> respond, using LangGraph to manage these steps.
To try this out, run ecommerce_service_server.py (which will wait for requests), then run ecommerce_agent_client.py. The agent script is set up to automatically launch the server if it’s not already running​
 (using an MCP client that spawns the subprocess). The agent will then process a hardcoded query or interactive input, demonstrating an end-to-end transaction. By studying this code, you’ll understand how to integrate multiple tools in one agent and how LangGraph + MCP can be applied to real business problems. The example shows an AI agent seamlessly bridging natural language understanding and database-like queries, all within a controlled workflow​
file-1yym3krchu2qjvkmpjderx
​
file-1yym3krchu2qjvkmpjderx
.
Utility Modules:
In addition to chapter-specific scripts, the repository contains some utility modules:
utils.py – helper functions and classes used across examples (for things like loading API keys from .env, common prompt strings, or any shared logic).
checkpoint.py – if present, this may contain helper code for LangGraph’s checkpointing/persistence (used by memory and HITL examples, possibly wrapping a SQLite or file-based store for agent state).
perplexity.py, pdf.py, etc. – miscellaneous tools or demos. For instance, pdf.py might show how an agent could read and summarize PDF text (by treating the PDF reading as a tool), and perplexity.py could be an example of calculating text perplexity or using an external QA service. These are not central to the book’s chapters, but provide additional context or experiments related to multi-agent capabilities.
Each script is documented with comments to explain its role. You can refer to the book chapters for a detailed walkthrough of the logic behind each example. The Project Structure section in the book’s README (above) summarizes the main components​
github.com
​
github.com
, and we have expanded on that here with chapter references.
Notes on LangGraph and MCP
LangGraph: All the agent workflows here are built using the LangGraph framework. LangGraph allows you to define an agent’s behavior as a directed graph of states and transitions, rather than a linear script. This makes the agent’s decision process more transparent and maintainable. In practice, you will see LangGraph’s StateGraph being constructed in the code, with nodes (functions) representing actions or steps, and edges determining the next step based on outcomes. The benefit of this approach is the ability to handle complex dialogues and decision branching easily. As you explore the code, notice how each agent script sets up its graph:
Some are simple (e.g., a single loop from START to END for simple_agent.py).
Others are complex (multiple intermediate nodes and conditional edges, e.g., hitl_agent.py where one branch pauses for approval, or two_qa_agent.py where two agents feed into each other).
LangGraph abstracts a lot of the heavy lifting – like tracking the conversation state and managing the execution flow – so you can focus on what each step should do. It also integrates memory and persistence (via “checkpoints”) which we leveraged in the memory and HITL chapters. MCP and FastMCP: MCP stands for Model-Context Protocol, a specification (originating from Anthropic) for how AI agents can talk to external tools in a consistent way​. Instead of each tool having a custom integration, MCP provides a unified JSON-RPC interface. In simple terms, when the agent needs to use a tool (say, a search engine), it sends a JSON request describing the action (tool name, parameters) to an MCP server, and gets back a JSON response with the result. This decouples the agent logic from the tool implementation. FastMCP is an open-source Python library that implements the MCP server/client, making it easy to create new tool endpoints. In our examples, we used FastMCP to stand up servers like user_db_server.py, tavily_search.py, etc., with minimal code​. FastMCP automatically handles the networking or STDIO communication and lets us register Python functions as tools. The book likens MCP to a “USB-C port” for AI agents – a single standardized plug for many tools​. FastMCP in turn is like an easy adapter that lets us create those plugs quickly. Using the FastMCP Servers: For chapters involving MCP, pay attention to how to run the servers:
Some agent scripts will spawn the server automatically (using a subprocess via the MCP client). For example, ecommerce_agent_client.py launches ecommerce_service_server.py on the fly​, and then connects to it. This is convenient for development.
In other cases, you might need to run the server manually in a separate terminal. The book notes that for the Tavily and YouTube tools, you would start tavily_search.py and yt_transcript.py each in its own process, then run the multi-server client to connect to them​. Our multiserver_mcpclient.py script is set up to spawn them for you (via STDIO), but you can also run them yourself for debugging.
If you are experimenting, ensure the required servers are running or configured as needed. For instance, to use the web search agent, obtain a Tavily API key and run tavily_search.py (it will inform you if the key is missing). The LangGraph agent will then call the search_web tool when needed and get live results. Similarly, run yt_transcript.py for the transcript tool. FastMCP will print logs to the console when it receives requests, which helps in understanding the interaction between the agent and tool. OpenAI Models: By default, the LangGraph agents use OpenAI’s GPT models (e.g., GPT-4 or GPT-3.5) for their language reasoning. This means you must have an OpenAI API key set (as mentioned in Setup) and internet access for the API. If you want to use a different model or a local LLM, you might need to modify the LangGraph agent initialization in the scripts. (For example, LangGraph might allow using HuggingFace models or others – see LangGraph documentation for details.) The book’s examples focus on GPT for quality results, so we recommend using GPT-4 if available, or GPT-3.5 as an alternative. Tips for Further Exploration: As you work with this code, you can modify and extend the agents:
Try changing the prompts or behavior of the agents (the system or role prompts are often configurable in the scripts) to see how the output changes.
Add new tools via MCP: for instance, you could create a new server for sending an email or querying a different API, then integrate it into an agent’s graph.
Scale up the multi-agent interactions: the two_qa_agent.py is just two identical agents. You could create heterogeneous agents (e.g., one for math, one for translation) and have the main agent route user questions to the appropriate one (this would use an interpreter like llm_query_interpreter.py to decide which specialist to use).
The combination of LangGraph and MCP is powerful. LangGraph keeps your agent’s workflow organized and deterministic, while MCP makes the agent extensible – it can gain new abilities just by plugging in a new tool server without changing the agent’s core logic​. This modular design is emphasized throughout the book: you can maintain and upgrade parts of the system (like improving a tool or adding memory) independently, which is crucial for real-world applications.
Conclusion
This README has provided an overview of the repository and how it ties into Building Multi-Agent AI Systems. In summary, you have:
A clear path from a simple echo chatbot to a sophisticated multi-agent, tool-using AI system.
Code for each major milestone (memory, HITL, multi-agent, tool integration, deployment) organized by chapter.
Instructions to set up and run the code, plus notes to get the most out of LangGraph and MCP.
We hope this helps you quickly get started with the examples. Clone the repo, set up the environment, and dive into the code — run the scripts, read the inline comments, and cross-reference with the book chapters for deeper explanations. If you encounter any issues or have questions, feel free to open an issue in the repository or consult the book’s troubleshooting sections (each chapter often anticipates common pitfalls). Happy building, and enjoy orchestrating your own multi-agent AI workflows! With LangGraph and MCP, the possibilities for intelligent, extensible agents are vast – from automating business processes to creating smart assistants that coordinate multiple services. We look forward to seeing what you create with these tools. Good luck, and happy coding!
