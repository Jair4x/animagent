import pytest
from pathlib import Path
import config

def test_host_is_string():
    assert isinstance(config.HOST, str)

def test_port_is_int():
    assert isinstance(config.PORT, int)

def test_port_in_valid_range():
    assert 1024 <= config.PORT <= 65535

def test_frontend_url_is_string():
    assert isinstance(config.FRONTEND_URL, str)

def test_default_llm_is_valid():
    assert config.DEFAULT_PROVIDER in ("groq", "gemini")

def test_groq_model_name_is_string():
    assert isinstance(config.GROQ_MODEL_NAME, str)
    assert len(config.GROQ_MODEL_NAME) > 0

def test_gemini_model_name_is_string():
    assert isinstance(config.GEMINI_MODEL_NAME, str)
    assert len(config.GEMINI_MODEL_NAME) > 0

def test_documents_path_exists():
    assert config.DOCUMENTS_PATH.exists(), f"DOCUMENTS_PATH no existe: {config.DOCUMENTS_PATH}"

def test_documents_path_is_directory():
    assert config.DOCUMENTS_PATH.is_dir()

def test_chunk_size_is_positive():
    assert config.CHUNK_SIZE > 0

def test_chunk_overlap_less_than_chunk_size():
    assert config.CHUNK_OVERLAP < config.CHUNK_SIZE