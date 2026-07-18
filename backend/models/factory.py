from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
import config

def get_llm(provider: str | None = None, gemini_key: str | None = None) -> BaseChatModel:
    """
    Instantiates and returns the language model to use.

    ### Selection logic
    - If no provider is set, `DEFAULT_PROVIDER` from .env config is used.  
    - If the provider is `'gemini'`, use the API key set by the user,
    if they didn't set one, use `GEMINI_API_KEY` from .env config as fallback.
    - If the provider is 'groq', use `GROQ_API_KEY` from .env config.
    
    ### Args
    #### `provider`
    LLM provider. Must be 'gemini' or 'groq'
    #### `gemini_key`
    Google Gemini key
    """
    resolved_provider = (provider or config.DEFAULT_PROVIDER).lower()

    # If the user selects "gemini" as the provider
    if resolved_provider == "gemini":
        key = gemini_key or config.GEMINI_API_KEY
        if not key:
            raise ValueError("[Factory] No Gemini API key available. Set up GEMINI_API_KEY in .env config or send your own API key.")
        
        return ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL_NAME,
            api_key=key,
            temperature=0.3,
        )
    
    # Or use Groq
    return ChatGroq(
        model=config.GROQ_MODEL_NAME,
        api_key=config.GROQ_API_KEY,
        # reasoning_format="hidden", # Only add if the model supports it
        temperature=0.3,
    )