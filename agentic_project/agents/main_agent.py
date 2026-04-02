import json
import logging
import os
import time
from typing import Dict, List, Optional

import requests
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Agent:
    """
    A customer support agent for an e-commerce platform.
    """

    def __init__(self, config_path="config/config.yaml"):
        """
        Initializes the Agent with configuration settings.
        """
        self.config = self._load_config(config_path)
        self.llm = self._initialize_llm()
        self.data_sources = self._load_data_sources()
        self.greeting = self.config['agent_behavior']['greeting']
        self.farewell = self.config['agent_behavior']['farewell']
        self.forbidden_topics = self.config['agent_behavior']['forbidden_topics']
        self.retry_attempts = self.config['error_handling']['retry_attempts']
        self.retry_delay = self.config['error_handling']['retry_delay']
        self.circuit_breaker_threshold = self.config['error_handling']['circuit_breaker_threshold']
        self.circuit_breaker_timeout = self.config['error_handling']['circuit_breaker_timeout']
        self.circuit_breaker_failures = 0
        self.circuit_breaker_open = False
        self.circuit_breaker_last_failure = None
        self.product_catalog = self._load_product_catalog()

    def _load_config(self, config_path: str) -> Dict:
        """Loads the configuration from the specified YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing configuration file: {e}")
            raise

    def _initialize_llm(self):
        """Initializes the language model."""
        model_name = self.config['llm']['model_name']
        api_key = self.config['llm']['api_key']
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service_account.json" # Replace with your service account path
        aiplatform.init(project="your-gcp-project-id", location="us-central1") # Replace with your project ID and location
        return GenerativeModel(model_name)

    def _load_data_sources(self) -> Dict:
        """Loads and initializes data sources based on the configuration."""
        data_sources = {}
        for name, config in self.config['data_sources'].items():
            try:
                if config['type'] == 'POSTGRES':
                    # Placeholder for PostgreSQL connection
                    logging.info(f"Connecting to PostgreSQL database: {name}")
                    # Implement PostgreSQL connection here
                    data_sources[name] = "PostgreSQL Connection"  # Replace with actual connection object
                elif config['type'] == 'CSV':
                    file_path = config['file_path']
                    logging.info(f"Loading CSV file: {file_path}")
                    # Implement CSV loading here
                    data_sources[name] = self._load_csv(file_path) # Replace with actual data
                elif config['type'] == 'API':
                    logging.info(f"Connecting to API: {name}")
                    data_sources[name] = config['url'] # Replace with actual API client
                else:
                    logging.warning(f"Unsupported data source type: {config['type']}")
            except Exception as e:
                logging.error(f"Failed to load data source {name}: {e}")
        return data_sources

    def _load_csv(self, file_path: str) -> List[Dict]:
        """Loads data from a CSV file."""
        try:
            with open(file_path, 'r') as f:
                import csv
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            logging.error(f"CSV file not found: {file_path}")
            return []
        except Exception as e:
            logging.error(f"Error loading CSV file: {e}")
            return []

    def _load_product_catalog(self) -> List[Dict]:
        """Loads the product catalog from the configured data source."""
        if 'product_catalog' in self.data_sources:
            return self.data_sources['product_catalog']
        else:
            logging.warning("Product catalog not found in data sources.")
            return []

    def _is_circuit_breaker_open(self) -> bool:
        """Checks if the circuit breaker is open."""
        if self.circuit_breaker_open:
            time_since_failure = time.time() - self.circuit_breaker_last_failure
            if time_since_failure > self.circuit_breaker_timeout:
                logging.info("Circuit breaker timeout reached. Resetting.")
                self.circuit_breaker_open = False
                self.circuit_breaker_failures = 0
            else:
                return True
        return False

    def _record_failure(self):
        """Records a failure and potentially opens the circuit breaker."""
        self.circuit_breaker_failures += 1
        self.circuit_breaker_last_failure = time.time()
        if self.circuit_breaker_failures > self.circuit_breaker_threshold:
            logging.warning("Circuit breaker opened.")
            self.circuit_breaker_open = True

    def _execute_with_retry(self, func, *args, **kwargs):
        """Executes a function with retry logic and circuit breaker."""
        if self._is_circuit_breaker_open():
            return "Service unavailable. Please try again later."

        for attempt in range(self.retry_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                self._record_failure()
                if attempt == self.retry_attempts - 1:
                    logging.error("Max retries reached.")
                    return f"An error occurred. Please try again later. Error: {e}"
                time.sleep(self.retry_delay)

    def _call_llm(self, prompt: str) -> str:
        """Calls the language model with the given prompt."""
        try:
            model = self.llm
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error calling LLM: {e}")
            raise

    def _validate_input(self, user_input: str) -> bool:
        """Validates the user input against forbidden topics."""
        for topic in self.forbidden_topics:
            if topic.lower() in user_input.lower():
                return False
        return True

    def _format_response(self, response: str) -> str:
        """Formats the response to be polite and easy to understand."""
        return f"{response}\n{self.farewell}"

    def get_product_information(self, product_name: str) -> Optional[str]:
        """Retrieves product information from the product catalog."""
        for product in self.product_catalog:
            if product['product_name'].lower() == product_name.lower():
                return f"Product Name: {product['product_name']}, Description: {product['description']}, Price: {product['price']}"
        return None

    def handle_query(self, user_input: str) -> str:
        """Handles the user query and returns a response."""
        if not self._validate_input(user_input):
            return "I am sorry, but I cannot assist with that topic. Please contact human support for payment, security, or technical issues."

        prompt = f"""You are an e-commerce customer support agent. Your name is SupportBot.
        You are helping a customer with their query. Be polite, friendly, and patient.
        If the user input is unclear, ask follow-up questions. Guide users step by step.
        Here is the user input: {user_input}
        """

        try:
            response = self._execute_with_retry(self._call_llm, prompt)
            return self._format_response(response)
        except Exception as e:
            logging.error(f"Error handling query: {e}")
            return "I am sorry, I encountered an error processing your request. Please try again later."

    def greet(self) -> str:
        """Returns the agent's greeting."""
        return self.greeting

# Example usage (for local testing)
if __name__ == '__main__':
    agent = Agent()
    print(agent.greet())
    user_query = "Where is my order?"
    response = agent.handle_query(user_query)
    print(response)
    product_info = agent.get_product_information("Awesome T-Shirt")
    if product_info:
        print(product_info)