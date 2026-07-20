from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere
from langchain_core.language_models import BaseChatModel
import config

def get_llm(
        provider:   str | None = None,
        gemini_key: str | None = None,
        openai_key: str | None = None,
        cohere_key: str | None = None,
        groq_key:   str | None = None
    ) -> BaseChatModel:
    """
    Instantiates and returns the language model to use.

    ### Selection logic
    - If no provider is set, `DEFAULT_PROVIDER` from .env config is used.  
    - If the provider is `'gemini'`, use the user API key or `GEMINI_API_KEY`.
    - If the provider is `'openai'`, use the user API key or `OPENAI_API_KEY`.
    - If the provider is `'cohere'`, use the user API key or `COHERE_API_KEY`.
    - If the provider is `'groq'`, use the user API key or `GROQ_API_KEY`.
    
    ### Args
    #### `provider`
    LLM provider. Must be `"gemini"`, `"openai"` or `"groq"`.
    #### `gemini_key`
    Google Gemini key
    """
    resolved_provider = (provider or config.DEFAULT_PROVIDER).lower()

    if resolved_provider == "gemini":
        key = gemini_key or config.GEMINI_API_KEY
        if not key:
            raise ValueError("[Factory] No Gemini API key available. Set up GEMINI_API_KEY in .env config or send your own API key.")
        
        return ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL_NAME,
            api_key=key,
            # reasoning_format="hidden", # Only add if the model supports it
            temperature=0.3,
        )
    elif resolved_provider == "openai":
        key = openai_key or config.OPENAI_API_KEY
        if not key:
            raise ValueError("[Factory] No OpenAI API key available. Set up OPENAI_API_KEY in .env config or send your own API key.")
        
        return ChatOpenAI(
            model=config.OPENAI_MODEL_NAME,
            api_key=key,
            # reasoning_format="hidden", # Only add if the model supports it
            temperature=0.3
        )
    elif resolved_provider == "cohere":
        key = cohere_key or config.COHERE_API_KEY
        if not key:
            raise ValueError("[Factory] No COHERE AI API key available. Set up COHERE_API_KEY in .env config or send your own API key.")
        
        return ChatCohere(
            model=config.COHERE_MODEL_NAME,
            cohere_api_key=key,
            # reasoning_format="hidden", # Only add if the model supports it
            temperature=0.3,
        )
    elif resolved_provider == "groq":
        key = groq_key or config.GROQ_API_KEY
        if not key:
            raise ValueError("[Factory] No Groq API key available. Set up GROQ_API_KEY in .env config or send your own API key.")

        return ChatGroq(
            model=config.GROQ_MODEL_NAME,
            api_key=key,
            # reasoning_format="hidden", # Only add if the model supports it
            temperature=0.3,
        )
    
    raise ValueError(
        f"[Factory] Unkown provider '{resolved_provider}'."
        "Supported providers: gemini, openai, groq."
    )