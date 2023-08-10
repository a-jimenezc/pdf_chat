from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from gradio_client import Client

class LLM_gradioAPI(LLM):
    """
    This is a wrapper for gradi APIs for LLMs to use with langchain library.
    The attributes to specify are client_api and api_name.
    """
    n: int
    client_api = ""
    api_name = ""

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        # Remove the restriction on the stop parameter
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")


        # Make the API call using the Gradio Client
        client = Client(self.client_api)
        result = client.predict(prompt, api_name=self.api_name)

        # Return the response from the API
        return result

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}