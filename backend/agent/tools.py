from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from rag.retriever import retrieve, format_context
import pandas as pd
import config

def make_search_documents_tool(index: FAISS):
    @tool
    def search_documents(query: str, category: str | None = None) -> str:
        """
        Searches the institutional document index for information relevant to the query.

        Use this tool for questions about convivencia, aranceles, faq, or general institutional info.

        ### Args
        #### `query`
        The user's question or search terms.
        #### `catergory`
        Optional filter. One of: 'convivencia', 'aranceles', 'faq'. Leave None to search all.
        """
        documents = retrieve(index, query, category=category, k=6)
        if not documents:
            return "No se encontró información relevante en los documentos."
        
        context = format_context(documents)
        sources = list({doc.metadata.get("source", "¿?") for doc in documents})
        source  = ", ".join(sources)

        return f"{context}\n__source__:{source}"
    
    return search_documents

def make_search_timetables_tool():
    @tool
    def search_timetables(program: str | None, group: str | None = None, subject: str | None = None, day: str | None = None, branch: str | None = None) -> str:
        """
        Searches the timetable CSV files for schedule information.

        Use this tool for questions about class schedules, subjects, teachers, or groups.

        ### Args
        #### `program`
        Educational program. One of: 'FINEST', 'Bachillerato'. None if unknown.
        #### `group`
        Student group. One of: 'A', 'B'. None if unknown.
        #### `subject`
        Subject name. e.g. 'Back-end', 'Front-end', 'Matemática'. None if unknown.
        #### `day`
        Day of the week in Spanish, e.g. 'Lunes', 'Martes'. None if unknown.
        #### `branch`
        Program branch, e.g. 'TIC', 'Administración', 'Común'. None if unknown.
        """
        timetable_dir   = config.DOCUMENTS_PATH / "horarios"
        csv_files       = list(timetable_dir.glob("*.csv"))

        if not csv_files:
            return "No se encontraron archivos de horarios."
        
        VALID_PROGRAMS = ["finest", "bachillerato"]

        # Select CSV based on program
        csv_path = csv_files[0]
        if program:
            keyword = program.lower()
            if keyword not in VALID_PROGRAMS:
                return f"Programa inválido: '{program}'. Los programas disponibles son: FINEST, Bachillerato.\n__source__:none"
            for csv in csv_files:
                if keyword in csv.stem.lower():
                    csv_path = csv
                    break

        df = pd.read_csv(csv_path)

        filters = {
            "programa": program,
            "grupo":    group,
            "materia":  subject,
            "día":      day,
            "rama":     branch,
        }

        result = df.copy()
        for col, value in filters.items():
            if value is None or col not in result.columns:
                continue
            
            col_normalized = result[col].astype(str).str.lower().str.replace("-", "").str.replace(" ", "")
            val_normalized = str(value).lower().replace("-", "").replace(" ", "")
            
            result = result[col_normalized == val_normalized]
        
        if result.empty:
            return f"No se encontraron horarios con los criterios especificados. Archivo consultado: {csv_path.name}\n__source__:{csv_path.name}"
        
        if len(result) > 30:
            return f"Se encontraron {len(result)} filas con esos criterios, es demasiado para procesar. Por favor especifica más: grupo, día, materia o rama.\n__source__:{csv_path.name}"

        rows = result.to_dict(orient="records")
        context = "\n".join(
            " | ".join(f"{k}: {v}" for k, v in row.items())
            for row in rows
        )

        print(f"[Tool: search_timetables] {csv_path.name} -> {len(result)} rows found")
                        
        return f"{context}\n__source__:{csv_path.name}"
    
    return search_timetables