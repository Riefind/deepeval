from .azure_model import AzureOpenAIModel
from .openai_model import GPTModel
from .local_model import LocalModel

try:
    from .ollama_model import OllamaModel
except Exception:  # pragma: no cover - optional dependency
    OllamaModel = None

try:
    from .gemini_model import GeminiModel
except Exception:  # pragma: no cover - optional dependency
    GeminiModel = None

try:
    from .anthropic_model import AnthropicModel
except Exception:  # pragma: no cover - optional dependency
    AnthropicModel = None

try:
    from .amazon_bedrock_model import AmazonBedrockModel
except Exception:  # pragma: no cover - optional dependency
    AmazonBedrockModel = None

try:
    from .litellm_model import LiteLLMModel
except Exception:  # pragma: no cover - optional dependency
    LiteLLMModel = None

__all__ = ["AzureOpenAIModel", "GPTModel", "LocalModel"]
if OllamaModel is not None:
    __all__.append("OllamaModel")
if GeminiModel is not None:
    __all__.append("GeminiModel")
if AnthropicModel is not None:
    __all__.append("AnthropicModel")
if AmazonBedrockModel is not None:
    __all__.append("AmazonBedrockModel")
if LiteLLMModel is not None:
    __all__.append("LiteLLMModel")
