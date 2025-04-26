from dotenv import load_dotenv
load_dotenv()

from typing import Literal, Dict, Annotated, List
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
import sqlite3

from langgraph.types import Command
from langgraph.checkpoint.sqlite import SqliteSaver  # SQLite-based checkpoint
from utils import show_graph

class IdeaState(BaseModel):
    topic: str                       # idea topic provided by the user
    ideas: List[str] = []           # list of ideas generated via brainstorming
    research: Dict[str, str] = {}   # research results (keyword -> summarized info)
    summary: str = ""                # final summary

def brainstorm_agent(state: IdeaState):
    """Agent that generates three related ideas for the given topic."""
    topic = state.topic
    # Example implementation: create three variations on the topic
    ideas = [
        f"Idea A related to {topic}",
        f"Idea B related to {topic}",
        f"Idea C related to {topic}"
    ]
    return {"ideas": ideas}

async def web_search_async(query: str):
    """Asynchronously search the web and return top 3 results."""
    # 4. Set User-Agent and Accept-Language headers (to avoid blocking)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }
    # Construct DuckDuckGo search URL
    search_url = f"https://duckduckgo.com/html/?q={query}"

    # 1. Perform asynchronous HTTP GET request using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers) as response:
            html_content = await response.text()

    # 2. Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    results = []
    # 3. Select HTML elements containing search results (top 3 results)
    result_items = soup.find_all('div', class_='result', limit=3)
    for item in result_items:
        title_elem = item.find('a', class_='result__a')
        snippet_elem = item.find(class_='result__snippet')
        link_elem = item.find('a', class_='result__url')

        # Extract text and link if elements exist
        title = title_elem.get_text() if title_elem else ''
        url = link_elem['href'] if link_elem else ''
        snippet = snippet_elem.get_text() if snippet_elem else ''

        results.append({
            "title": title,
            "url": url,
            "snippet": snippet
        })
    # 5. Return the results list
    return results

async def research_agent(state: IdeaState):
    """Agent that asynchronously retrieves information for each idea in the list."""
    ideas = state.ideas
    # Return empty result immediately if the idea list is empty
    if not ideas:
        return {"research": {}}

    results = {}
    # Perform web searches in parallel for each idea
    coros = [web_search_async(idea) for idea in ideas]
    fetched_list = await asyncio.gather(*coros)

    # Organize results into a dict (idea -> info)
    for idea, info in zip(ideas, fetched_list):
        if info:
            # Combine title and snippet for each result
            info_str = "\n".join(
                f"{item.get('title','').strip()} - {item.get('snippet','').strip()}"
                for item in info
            )
        else:
            info_str = ""
        results[idea] = info_str

    return {"research": results}

def summarize_agent(state: IdeaState):
    """Agent that compiles research results into a summary."""
    research_data = state.research
    if not research_data:
        summary_text = "No research data available to summarize."
    else:
        # Combine all research strings into one summary
        combined = " ".join(research_data.values())
        summary_text = combined
    return {"summary": summary_text}


def supervisor(state: IdeaState) -> Command[
    Literal["brainstorm_agent", "research_agent", "summarize_agent", "__end__"]
]:
    """Supervisor agent that directs the workflow based on state."""
    print("supervisor:", state.ideas)
    # If no ideas have been generated yet, start with brainstorming
    if not state.ideas:
        return Command(goto="brainstorm_agent")
    # If ideas exist but research hasn't been done, go to research step
    elif state.ideas and not state.research:
        # If idea count is zero, end immediately
        if len(state.ideas) == 0:
            return Command(goto=END)
        return Command(goto="research_agent")
    # If research is complete and summary isn't, go to summarization
    elif state.research and not state.summary:
        return Command(goto="summarize_agent")
    else:
        # All steps complete or termination condition
        return Command(goto=END)

# Build the graph and register nodes (Supervisor and each agent)
builder = StateGraph(IdeaState)
builder.add_node("supervisor", supervisor)
builder.add_node("brainstorm_agent", brainstorm_agent)
builder.add_node("research_agent", research_agent)
builder.add_node("summarize_agent", summarize_agent)

# Add edges: Supervisor orchestrates the entire workflow
builder.add_edge(START, "supervisor")
builder.add_edge("supervisor", "brainstorm_agent")
builder.add_edge("supervisor", "research_agent")
builder.add_edge("supervisor", "summarize_agent")
builder.add_edge("brainstorm_agent", "supervisor")
builder.add_edge("research_agent", "supervisor")
builder.add_edge("summarize_agent", "supervisor")

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

async def init_checkpointer():
    # Create asynchronous checkpointer
    conn = await aiosqlite.connect(":memory:")
    return AsyncSqliteSaver(conn)

async def main():
    checkpointer = await init_checkpointer()
    graph = builder.compile(checkpointer=checkpointer)
    try:
        # Execute workflow (thread_id is required)
        thread_id = "idea1"
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 100
        }
        # Set initial topic
        state0 = {"topic": "Artificial Intelligence"}
        result = await graph.ainvoke(state0, config)
        print(result)
    except AttributeError as e:
        print(f"AttributeError occurred: {e}")

asyncio.run(main())

