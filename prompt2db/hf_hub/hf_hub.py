import os

from langchain.llms import HuggingFaceHub


class HFHub:
    """Client for getting LLMs from HuggingFace hub"""

    def __init__(self, hf_token: str | None = None) -> None:
        """
        Init instance.

        Args:
             hf_token: str | None - HF token to download LLMs
        """
        self._hf_token = hf_token if hf_token is not None else os.environ['HUGGINGFACEHUB_API_TOKEN']

    def load_model(self, model_name: str, model_params: dict) -> HuggingFaceHub:
        """
        Download model from HF by model_name and model_params.

        Args:
             model_name: str - Model name from the hub (username/model_name).
             model_params: dict - Model params to init model: model(params).
        Returns:
            HuggingFaceHub - Ready-to-use LLM from HF hub.
        """
        return HuggingFaceHub(
            repo_id=model_name,
            model_kwargs=model_params
        )
