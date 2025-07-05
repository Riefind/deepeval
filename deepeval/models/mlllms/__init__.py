from .openai_model import MultimodalOpenAIModel

try:
    from .ollama_model import MultimodalOllamaModel
except Exception:  # pragma: no cover - optional dependency
    MultimodalOllamaModel = None

try:
    from .gemini_model import MultimodalGeminiModel
except Exception:  # pragma: no cover - optional dependency
    MultimodalGeminiModel = None
__all__ = ['MultimodalOpenAIModel']
if MultimodalOllamaModel is not None:
    __all__.append('MultimodalOllamaModel')
if MultimodalGeminiModel is not None:
    __all__.append('MultimodalGeminiModel')
