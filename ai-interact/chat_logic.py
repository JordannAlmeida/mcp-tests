import os
from typing import Optional
from google.genai.chats import Chat
from dotenv import load_dotenv
from llm.type_llm import LLMType
from llm.gemini.gemini_manager import GeminiManager
from llm.base_llm import BaseLLM
from io import BytesIO

class ChatLogic:

    def __init__(self):
        self.__load_env()
        self.llm_type: LLMType = LLMType.GEMINI
        self.llm: BaseLLM = self.__select_llm(self.llm_type)

    def __load_env(self):
        """Loads the .env file."""
        environment = os.getenv("ENVIRONMENT", "local")
        if environment == "local":
            load_dotenv(".env.local")
        else:
            load_dotenv(".env")

    def __select_llm(self, llm_type: LLMType) ->  Optional[BaseLLM]:
        """Selects the appropriate LLM based on the type."""
        model: BaseLLM = None
        if llm_type == LLMType.GEMINI:
            model = GeminiManager()
        elif llm_type == LLMType.OPENAI:
            #TODO: Implement OpenAI LLM selection
            return None
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
        model.initialize_model()
        return model
    
    def start_new_chat(self, llm_model_selected: LLMType) -> Chat:
        """Initializes new chat"""
        self.llm = self.__select_llm(llm_model_selected)

    def get_response(self, prompt: str, files: list[dict[str, BytesIO]] = None) -> str:
        """Generates a response from the LLM model. Optionally accepts files as BytesIO."""
        if self.llm is None:
            raise ValueError("LLM model not initialized. Please call start_new_chat() first.")
        return self.llm.generate_response(prompt, files=files)

