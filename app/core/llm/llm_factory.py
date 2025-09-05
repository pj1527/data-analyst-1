from typing import Dict, Optional
from langchain_litellm.chat_models import ChatLiteLLM


class LLMFactory:
    """
    A simple factory class to create and manage ChatLiteLLM client instances.
    
    This class maintains a registry of LLM model instances to avoid creating
    duplicate instances of the same model configuration.
    """
    _instances: Dict[str, ChatLiteLLM] = {}
    
    @classmethod
    def get_llm(
        cls,
        model: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatLiteLLM:
        """
        Get or create a ChatLiteLLM instance with the specified configuration.
        
        Args:
            model: The name of the LLM model to use
            api_key: The API key for the model's service
            temperature: Controls randomness in the model's output (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional arguments to pass to ChatLiteLLM
            
        Returns:
            An instance of ChatLiteLLM with the specified configuration
        """
        config_key = f"{model}_temp{temperature}_maxtok{max_tokens}"
        
        if config_key in cls._instances:
            return cls._instances[config_key]
            
        llm = ChatLiteLLM(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
            **kwargs
        )
        
        cls._instances[config_key] = llm
        return llm
    
    @classmethod
    def clear_instances(cls) -> None:
        """Clear all stored LLM instances."""
        cls._instances.clear()
