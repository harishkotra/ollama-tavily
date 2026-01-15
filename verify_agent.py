from agent import get_agent
import sys

def verify():
    print("Initializing agent...")
    agent = get_agent()
    
    query = "Recommend a thriller TV series artist"
    print(f"Running query: {query}")
    
    # Run the agent strictly to get a response
    try:
        response = agent.run(query)
        print("Response received:")
        print(response.content)
        
        # Follow-up
        print("\nRunning follow-up: Explain why!")
        # Force disable tools
        original_tools = agent.tools
        agent.tools = []
        response = agent.run("Explain why!", stream=False)
        agent.tools = original_tools
        
        # Check if tool was called in follow-up (it should NOT be)
        tool_calls = response.tools
        if tool_calls and len(tool_calls) > 0:
            print(f"FAILURE: Agent made {len(tool_calls)} tool calls during follow-up! It should use history.")
            for tc in tool_calls:
                # Debug the object
                print(f"Tool call object: {tc}")
                if hasattr(tc, 'name'):
                    print(f" - {tc.name}")
                elif hasattr(tc, 'tool_name'):
                    print(f" - {tc.tool_name}")
            sys.exit(1)
        
        print("SUCCESS: Agent used history and did not call tools for follow-up.")
        print(response.content)
        
    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify()
