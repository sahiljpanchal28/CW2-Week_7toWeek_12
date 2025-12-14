class OpenAIService:
    def get_ai_response(self, user_input, domain):
        if domain == "Cybersecurity":
            return f"Cybersecurity analysis for: {user_input}"
        elif domain == "Data Analytics":
            return f"Data analysis for: {user_input}"
        elif domain == "IT Operations":
            return f"IT solution for: {user_input}"
        return f"Response to: {user_input}"

ai_service = OpenAIService()