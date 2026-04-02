from agentic_project.agents.main_agent import Agent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to run the ECommerce Support Agent."""
    try:
        agent = Agent()
        print(agent.greet())

        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = agent.handle_query(user_input)
            print(f"Agent: {response}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()