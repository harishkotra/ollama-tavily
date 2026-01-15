from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools import Toolkit
from tavily import TavilyClient
import os
import json
from dotenv import load_dotenv

load_dotenv()

class CustomTavilyTools(Toolkit):
    def __init__(self, api_key: str, max_results: int = 5):
        super().__init__(name="tavily_tools")
        self.client = TavilyClient(api_key=api_key)
        self.max_results = max_results
        self.register(self.web_search)

    def web_search(self, query: str) -> str:
        """
        Search the web using Tavily.
        
        Args:
            query (str): The search query.
            
        Returns:
            str: JSON string of search results.
        """
        try:
            results = self.client.search(query=query, max_results=self.max_results)
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error searching Tavily: {e}"

from agno.db.sqlite.sqlite import SqliteDb

def get_agent():
    return Agent(
        model=Ollama(id="llama3.2:latest"),
        tools=[CustomTavilyTools(api_key=os.getenv("TAVILY_API_KEY"), max_results=5)],
        description="You are a helpful assistant that provides recommendations based on web search.",
        instructions=[
            "You are an expert recommender system.",
            "When asked for a recommendation, use the 'web_search' tool to find high-quality, relevant results.",
            "If the user asks 'why', 'tell me why', or asks for reasoning, explain your reasoning based on the search results you just found.",
            "Do NOT trigger a new search for the 'why' question unless you absolutely lack content.",
            "You have a perfect memory of the previous search results. USE IT.",
            "Never hallucinate unrelated topics (like Python programming) in your reasoning.",
            "Mention the sources or data points you found that led to your recommendation.",
            "Be verbose about your thought process when explaining reasoning.",
            "ENSURE that your tool calls are valid JSON. Check your quotes and keys."
        ],
        db=SqliteDb(db_url="sqlite:///agent_storage.db"),
        add_history_to_context=True,
        read_chat_history=False,
        num_history_messages=6,
        retries=2, # Retry on malformed JSON
        debug_mode=True, # To showcase the inner workings
    )
