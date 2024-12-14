import re

class RuleBasedChatbot:
    def __init__(self):
        # Initialize chatbot with rules and context storage
        self.rules = {
            r"hello|hi|hey": "Hello! How can I assist you today?",
            r"how are you": "I'm just a bot, but I'm doing great! What about you?",
            r"my name is (.+)": self.store_name,
            r"what is your name": "I'm a chatbot created to assist you! What's your name?",
            r"bye|goodbye": "Goodbye! Have a great day!",
            r"help": "I'm here to help! Ask me anything you'd like assistance with.",
            r"what is (\d+)\s*[\+\-*/]\s*(\d+)": self.calculate,
        }
        self.context = {}  # To store user-specific details (like their name)

    def store_name(self, match):
        # Store the user's name in the context
        name = match.group(1).strip()
        self.context["name"] = name
        return f"Nice to meet you, {name}! How can I assist you further?"

    def calculate(self, match):
        # Perform basic arithmetic calculations
        num1, operator, num2 = int(match.group(1)), match.group(0)[-1], int(match.group(2))
        operations = {
            "+": num1 + num2,
            "-": num1 - num2,
            "*": num1 * num2,
            "/": num1 / num2 if num2 != 0 else "undefined (division by zero)",
        }
        return f"The result is {operations.get(operator, 'Invalid operation')}."

    def get_response(self, user_input):
        # Match user input to rules
        user_input = user_input.lower().strip()  # Normalize input
        for pattern, response in self.rules.items():
            match = re.search(pattern, user_input)
            if match:
                if callable(response):  # If response is a function (e.g., for dynamic responses)
                    return response(match)
                return response
        return "I'm sorry, I don't understand that. Could you rephrase?"

    def personalize_response(self, response):
        # Personalize response based on context (e.g., user's name)
        if "name" in self.context:
            response = response.replace("{name}", self.context["name"])
        return response

    def chat(self):
        print("Chatbot: Hello! I'm your assistant. Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "goodbye"]:
                print("Chatbot: Goodbye! Have a nice day!")
                break
            response = self.get_response(user_input)
            response = self.personalize_response(response)  # Add personalization if needed
            print(f"Chatbot: {response}")


# Run the chatbot
if __name__ == "__main__":
    chatbot = RuleBasedChatbot()
    chatbot.chat()
