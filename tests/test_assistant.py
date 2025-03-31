import unittest
from src.assistant import BusinessInsightsAssistant

class TestBusinessInsightsAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = BusinessInsightsAssistant("dummy_key")

    def test_preprocess_query(self):
        query = "Improve marketing for Q4"
        result = self.assistant.preprocess_query(query)
        self.assertEqual(result["function"], "marketing")

    def test_generate_prompt(self):
        query_info = {"text": "company X", "function": "finance"}
        prompt = self.assistant.generate_prompt(query_info)
        self.assertIn("financial analysis", prompt)

   

if __name__ == "__main__":
    unittest.main()