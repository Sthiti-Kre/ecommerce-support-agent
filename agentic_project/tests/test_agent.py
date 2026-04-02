import unittest
from unittest.mock import patch
from agentic_project.agents.main_agent import Agent

class TestAgent(unittest.TestCase):

    def setUp(self):
        # Initialize the agent with a test configuration file
        self.agent = Agent(config_path="config/config.yaml")

    def test_greet(self):
        self.assertEqual(self.agent.greet(), self.agent.greeting)

    @patch('agentic_project.agents.main_agent.Agent._call_llm')
    def test_handle_query(self, mock_call_llm):
        mock_call_llm.return_value = "Test response from LLM"
        user_query = "What is the meaning of life?"
        response = self.agent.handle_query(user_query)
        self.assertIn("Test response from LLM", response)
        self.assertIn(self.agent.farewell, response)

    def test_validate_input(self):
        self.assertTrue(self.agent._validate_input("Tell me about your products"))
        self.assertFalse(self.agent._validate_input("I have a payment issue"))

    def test_get_product_information(self):
        product_info = self.agent.get_product_information("Awesome T-Shirt")
        self.assertIsNotNone(product_info)
        self.assertIn("Awesome T-Shirt", product_info)

        product_info_none = self.agent.get_product_information("NonExistentProduct")
        self.assertIsNone(product_info_none)

if __name__ == '__main__':
    unittest.main()