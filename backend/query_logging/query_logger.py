from pathlib import Path
from datetime import datetime, timezone
import json
import threading

LOG_PATH    = Path("logs/queries.jsonl")
_lock       = threading.Lock()

def log_query(
    query:      str,
    response:   str,
    source:     str | None,
    provider:   str | None,
    duration:   float,
) -> None:
    """
    Appends a query log entry to the JSONL log file.
    
    Each entry is a JSON object on a single line.

    ### Args
    #### `query`
    User's query
    #### `response`
    Agent's response
    #### `source`
    Source document(s) used
    #### `provider`
    LLM provider used (groq, gemini, etc.)
    #### `duration`
    Time taken to generate the response in seconds
    """
    entry = {
        "timestamp":    datetime.now(timezone.utc).isoformat(),
        "provider":     provider,
        "query":        query,
        "response":     response,
        "source":       source,
        "duration":     round(duration, 3),
    }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with _lock:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")