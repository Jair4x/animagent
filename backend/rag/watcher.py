from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from rag.loader import load_all_documents
from rag.embeddings import build_index
from pathlib import Path
import index_store
import threading
import time
import config

class DocumentChangeHandler(FileSystemEventHandler):
    """
    Handles filesystem events in the documents directory.

    Rebuilds the FAISS index when a PDF file is added, modified or deleted.
    """

    def __init__(self, debounce_seconds: float = 3.0):
        self._debounce_seconds = debounce_seconds
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def _schedule_rebuild(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            
            self._timer = threading.Timer(self._debounce_seconds, self._rebuild)
            self._timer.start()

    def _rebuild(self) -> None:
        print("[Watcher] Change detected. Regenerating FAISS index...")
        try:
            documents           = load_all_documents()
            index_store.index   = build_index(documents)
            print("[Watcher] Index regenerated succesfully.")
        except Exception as err:
            print(f"[Watcher] Error while regenerating index: {err}")

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory and event.src_path.endswith(".pdf"):
            self._schedule_rebuild()

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory and event.src_path.endswith(".pdf"):
            self._schedule_rebuild()
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        if not event.is_directory and event.src_path.endswith(".pdf"):
            self._schedule_rebuild()

def start_watcher():
    """
    Starts the filesystem observer in the background.

    ### Returns 
    Observer instance so it can be stopped on shutdown.
    """
    handler     = DocumentChangeHandler()
    observer    = Observer()
    observer.schedule(handler, str(config.DOCUMENTS_PATH), recursive=True)
    observer.start()
    
    print(f"[Watcher] Watching for changes in {config.DOCUMENTS_PATH}")
    return observer