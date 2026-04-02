import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_request(user_input: str):
    """Logs the user request."""
    logging.info(f"User Request: {user_input}")

def log_response(response: str):
    """Logs the agent's response."""
    logging.info(f"Agent Response: {response}")

def log_error(error: Exception, message: str = ""):
    """Logs an error."""
    logging.error(f"Error: {message} - {error}")

def monitor_performance(start_time, end_time):
    """Monitors the performance of the agent."""
    duration = end_time - start_time
    logging.info(f"Request processing time: {duration:.4f} seconds")

# Example usage:
if __name__ == '__main__':
    log_request("Where is my order?")
    log_response("Your order is on its way.")
    try:
        raise ValueError("Example error")
    except ValueError as e:
        log_error(e, "An example error occurred.")