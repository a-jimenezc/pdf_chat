from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from hugchat import hugchat
from hugchat.login import Login
import os

class LLM_hugging_chat(LLM):

    """
    This class represents a language model based on the Hugging Chat API.

    Attributes:
        n (int): words to retrieve.
        sign (Login): An instance of the Login class for Hugging Face authentication.
        cookies (dict): The authentication cookies obtained from signing in.
        chatbot (ChatBot): An instance of the Hugging ChatBot class.

    Methods:
        _llm_type(self) -> str:
            Get the type of the language model.

        _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None) -> str:
            Make an API call to the Hugging ChatBot using the specified prompt and return the response.

        _identifying_params(self) -> Mapping[str, Any]:
            Get the identifying parameters of the language model.
    """

    n: int
    sign = Login(os.environ.get("hugging_face_account"), os.environ.get("hugging_face_psw"))
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        chatbot = chatbot
    ) -> str:
        """
        Make an API call to the Hugging ChatBot using the specified prompt and return the response.

        Parameters:
            prompt (str): The prompt or input text for the API call.
            stop (List[str], optional): List of stop words. Not used in this context.
            run_manager (CallbackManagerForLLMRun, optional): Callback manager for LLM run. Not used in this context.

        Returns:
            str: The response from the Hugging ChatBot.
        """
        # Remove the restriction on the stop parameter
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        result = chatbot.chat(prompt, temperature=0.1)

        # Return the response from the API
        return result

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}