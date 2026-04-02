import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_input(user_input: str, forbidden_topics: list) -> bool:
    """Validates the user input against forbidden topics."""
    for topic in forbidden_topics:
        if topic.lower() in user_input.lower():
            logging.warning(f"Input blocked due to forbidden topic: {topic}")
            return False
    return True

def filter_content(text: str) -> str:
    """Placeholder for content filtering logic.  In a real application, this would use a content moderation API."""
    # Example: Replace potentially harmful words with asterisks
    harmful_words = ["badword1", "badword2"]  # Replace with actual harmful words
    for word in harmful_words:
        text = text.replace(word, "****")
    return text

# Example usage:
if __name__ == '__main__':
    forbidden_topics = ["payment", "security"]
    user_input = "I have a question about payment."
    if validate_input(user_input, forbidden_topics):
        print("Input is valid.")
    else:
        print("Input is invalid.")

    content = "This is a test with badword1."
    filtered_content = filter_content(content)
    print(f"Original content: {content}")
    print(f"Filtered content: {filtered_content}")