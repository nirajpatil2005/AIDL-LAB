from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()
groq_api = os.getenv("test_groq")

class SimpleChatbot:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=groq_api,
            model_name="openai/gpt-oss-20b"
        )
        self.conversation_history = {}
    
    def get_response(self, messages, thread_id='default'):
        try:
            # Store conversation history by thread
            if thread_id not in self.conversation_history:
                self.conversation_history[thread_id] = []
            
            # Add new messages to history
            self.conversation_history[thread_id].extend(messages)
            
            # Get response from LLM
            response = self.llm.invoke(self.conversation_history[thread_id])
            
            # Add AI response to history
            self.conversation_history[thread_id].append(response)
            
            return response.content
            
        except Exception as e:
            print(f"Error in get_response: {e}")
            return "Sorry, I encountered an error. Please try again."

# Create global chatbot instance
chatbot = SimpleChatbot()