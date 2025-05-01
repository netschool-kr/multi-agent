# Building Multi-Agent AI Systems – Code Examples

**Building Multi-Agent AI Systems: Workflow Orchestration with LangGraph and MCP** is a hands-on guide to creating AI agents that work together to automate business workflows. This repository contains the example code for the LangGraph-based multi-agent project introduced in the book. By following along, you’ll learn how to build intelligent agents that can converse with users, collaborate with other agents, and leverage external tools via the Model-Context Protocol (MCP) to drive business automation.

## Introduction

The book **Building Multi-Agent AI Systems** walks through designing AI agents using two key frameworks: **LangGraph** and **MCP**. LangGraph is a graph-based AI agent framework for orchestrating complex workflows as interconnected nodes. It serves as the “brain” of your agent, controlling dialogue flow and decision-making. MCP (Model-Context Protocol) is a standardized protocol for connecting AI agents to external tools and services—think of it as a universal interface that lets your agents call APIs, databases, or other systems. In this project, LangGraph provides the workflow structure, while MCP (via the FastMCP library) acts as the bridge to a universe of external tools.

**Goals of the Book:** By the end of the book, you will have a practical understanding of how to build multi-agent AI systems for real-world business automation. Starting from a simple conversational agent, each chapter adds new capabilities—memory, human-in-the-loop oversight, multi-agent collaboration, and tool integrations—culminating in fully-fledged agents that can coordinate workflows and interact with external services. The repository’s code allows you to **get hands-on experience**, creating your own AI agents step by step for tasks like chat automation, workflow orchestration, and data retrieval.

## Target Audience

This project is intended for **AI developers** and enthusiasts interested in large language model (LLM)-based agents and workflow automation. If you want to learn how to build intelligent chatbots or multi-agent systems that integrate with real tools, this repository will guide you. The examples assume familiarity with Python and basic concepts of AI/ML. Knowledge of APIs and JSON will help in understanding tool integration (MCP) but is not required to get started.

Whether you are a practitioner looking to automate business processes or a researcher exploring agent orchestration, you’ll find value in the clear, incremental approach—from a “hello world” agent to complex multi-agent workflows. Each chapter’s code is organized to teach a specific concept, making it easy to follow along and experiment.

## Setup and Installation

To run the examples, you’ll need a Python 3 environment with the required libraries installed. Follow the steps below to set up your development environment:

1. **Python Installation**  
   - Ensure you have **Python 3.11.10** installed.  
   - Check your version with:
     ```bash
     python --version
     ```

2. **Clone the Repository**  
   ```bash
   git clone https://github.com/netschool-kr/multi-agent.git
   cd multi-agent

3. Create a Virtual Environment (optional)
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   
4. Install Dependencies
pip install -r requirements.txt

5. Configure API Keys to .env file
   OPENAI_API_KEY=your-openai-key-here
   For other services (e.g., TAVILY_API_KEY), set similarly.

## Running the Examples
Each example is a standalone Python script demonstrating a specific concept. Activate your virtual environment and run:

python simple_agent.py
This will start an interactive console session. Type as the User, and the Agent will respond.

To exit, press Ctrl+C or use the agent’s built-in exit command (if provided).

## Repository Structure and Chapter Mapping
| Chapter | Description                                       | Script(s)                              |
|---------|---------------------------------------------------|----------------------------------------|
| 2       | Getting Started with LangGraph                    | `simple_agent.py`                      |
| 5       | LangGraph Core Concepts                           | `basic_flow.py`                        |
| 6       | State Management and Memory                       | `memory_agent.py`, `memory.py`         |
| 7       | Human-in-the-Loop Workflows                       | `hitl_agent.py`                        |
| 8       | Multi-Agent Collaboration                         | `two_qa_agent.py`, `project_agent.py`  |
| 9       | Integrating External Tools with MCP               | `user_db_server.py`, `user_db_client.py` |
| 10      | Building a LangGraph Agent System with MCP        | `forex_server.py`, `forex_client.py`, `finance.py` |
| 11      | Building Custom Tool Servers (FastMCP)            | `tavily_search.py`, `yt_transcript.py`, `multiserver_mcpclient.py`, `news_mcp_server.py`, `news_summarize.py` |
| 12      | Deploying an Interactive Chatbot                  | `chatbot_server.py`, `chatbot_client.py`, `chatbot_server_sse.py`, `chatbot_client_sse.py`, `asyncio_exam.py` |
| 13      | E-Commerce Agent Case Study                       | `ecommerce_service_server.py`, `ecommerce_agent_client.py` |
| –       | Utilities and Helpers                             | `utils.py`, `checkpoint.py`, `perplexity.py`, `pdf.py` |

## Notes on LangGraph and MCP
LangGraph
Define agent workflows as directed graphs of states and transitions. Nodes represent actions or decisions; edges control flow. LangGraph handles state tracking and execution, allowing you to focus on each step’s logic.

MCP (Model Context Protocol)
A JSON-RPC based protocol for AI agents to call external tools. FastMCP makes it easy to turn Python functions into tool endpoints. MCP decouples agent logic from tool implementation, enabling plug-and-play integrations.

## Conclusion
This README has provided an overview of the repository and how it ties into Building Multi-Agent AI Systems. You now have:

A clear path from a simple echo chatbot to a sophisticated, tool-using multi-agent AI system.

Code for each major milestone, organized by chapter.

Setup instructions and notes to get the most out of LangGraph and MCP.

Clone the repo, set up your environment, and dive into the code. Happy building, and enjoy orchestrating your own multi-agent AI workflows!
