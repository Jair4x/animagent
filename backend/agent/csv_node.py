from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from agent.state import AgentState
from pathlib import Path
import pandas as pd
import json
import config

ENTITY_EXTRACTION_PROMPT = ChatPromptTemplate.from_template(
    """
    Eres un extractor de entidades para un sistema de horarios institucional.
    Analiza la pregunta y extrae las entidades relevantes para buscar en un CSV de horarios.

    Programas disponibles: FINEST, Bachillerato
    Ramas disponibles: TIC, Administración (Bachillerato) / Común, Programación web full-stack, Analista de datos (FINEST)
    Grupos disponibles: A, B

    Responde ÚNICAMENTE con un JSON válido, sin explicación ni markdown:
    {{
        "programa": "FINEST" | "Bachillerato" | null,
        "rama": string | null,
        "grupo": "A" | "B" | null,
        "dia": string | null,
        "materia": string | null,
        "año": number | null,
        "semestre": number | null,
    }}

    Si no puedes inferir un valor con certeza, pon null.

    Pregunta: {query}
""")

def _find_csv(program: str | None) -> Path | None:
    """
    Searches for the appropiate timetable CSV according to the extracted program.

    ### Parameters
    #### `program`
    Extracted educational program

    ### Returns
    File Path to csv file / `None` if nothing was found.
    """
    timetables_dir  = config.DOCUMENTS_PATH / "horarios"
    csv_files       = list(timetables_dir.glob("*.csv"))

    if not csv_files:
        return None
    
    if program:
        keyword = program.lower()
        for csv in csv_files:
            if keyword in csv.stem.lower():
                return csv # Found it, returning the file
            
    return csv_files[0] # Fallback: Return the first file found

def _extract_entities(llm: BaseChatModel, query: str) -> dict:
    """
    Uses an LLM to extract the query's entities.

    ### Parameters
    #### `llm`
    LLM instance for the entity extraction agent

    #### `query`
    User query for which to search the appropiate timetable CSV

    ### Returns
    `dict` with the found entities
    """
    chain   = ENTITY_EXTRACTION_PROMPT | llm
    result  = chain.invoke({"query": query})

    content = result.content
    if isinstance(content, list):
        if result.text:
            content = result.text
        else:
            content = " ".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )
    
    content = content.strip()
    if content.startswith("```"):
        content = "\n".join(content.split("\n")[1:-1])

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}
    
def _filter_csv(df: pd.DataFrame, entities: dict) -> pd.DataFrame:
    """
    Filters the DataFrame according to the extracted entities.
    
    Ignores the entities with value `None`.

    ### Parameters
    #### `df`
    Pandas DataFrame.
    #### `entities`
    Entities to filter. From `_extract_entitities(llm, query)`
    ### Returns
    Filtered DataFrame
    """
    filters = {
        "programa": entities.get("programa"),
        "rama": entities.get("rama"),
        "grupo": entities.get("grupo"),
        "dia": entities.get("dia"),
        "materia": entities.get("materia"),
    }

    if entities.get("año"):
        filters["año"] = entities["año"]
    
    if entities.get("semestre"):
        filters["semestre"] = entities["semestre"]
    
    result = df.copy()

    for col, value in filters.items():
        if value is not None and col in result.columns:
            result = result[
                result[col].astype(str).str.lower() == str(value).lower()
            ]
        
    return result

def csv_retriever_node(state: AgentState, llm: BaseChatModel) -> AgentState:
    """
    Specific node for timetable queries.
    
    Extracts entities from the query and filters the appropiate CSV.

    ### Parameters
    #### `state`
    Current agent state
    #### `llm`
    Language model instance

    ### Returns
    Updated `AgentState` instance with context and source fields populated
    """
    query       = state["query"]
    entities    = _extract_entities(llm, query)
    csv_path    = _find_csv(entities.get("programa"))

    if not csv_path:
        return {**state, "context": "No se encontraron archivos de horarios disponibles.", "source": None}
    
    df      = pd.read_csv(csv_path)
    results = _filter_csv(df, entities)

    if results.empty:
        missing = [k for k, v in entities.items() if v is None and k in ("programa", "grupo", "materia")]
        hint    = f" Información faltante para filtrar: {', '.join(missing)}." if missing else ""
        
        return {
            **state,
            "context":  f"No se encontraron horarios con los criterios especificados.{hint}",
            "source":   csv_path.name
        }
    
    rows    = results.ro_dic(orient="records")
    context = "\n".join(
        " | ".join(f"{k}: {v}" for k, v in row.items())
        for row in rows
    )

    print(f"[CSV Retriever] {csv_path.name} -> {len(results)} rows found")

    return {
        **state,
        "context":  context,
        "source":   csv_path
    }