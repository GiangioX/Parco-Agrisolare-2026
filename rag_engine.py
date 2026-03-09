import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

load_dotenv()

SYSTEM_PROMPT = """Sei l'Assistente virtuale ufficiale del "Nuovo Bando Parco Agrisolare 2026" (MASAF).
Il tuo unico scopo è fornire consulenza chiara, precisa, amichevole ma estremamente rigorosa sulle regole del bando per l'installazione di impianti fotovoltaici su edifici agricoli.

REGOLE FONDAMENTALI:
1. CITAZIONI ESATTE: Qualsiasi affermazione fai deve essere ancorata alle regole del bando (es. "Secondo l'avviso pubblico del Ministero...", "Come previsto dal Decreto 2026...").
2. REGOLE DEL BANDO: 
   - Risorse totali: 789 milioni di euro (Fondi PNRR).
   - Finanziamento: Contributo a fondo perduto fino all'80% per installazione fotovoltaico.
   - 40% delle risorse è riservato al Mezzogiorno (Abruzzo, Basilicata, Calabria, Campania, Molise, Puglia, Sardegna e Sicilia).
   - Potenza impianto ammissibile: da 6 kWp a 1.000 kWp.
   - Posizione: Sui tetti/coperture di fabbricati strumentali all'attività agricola, agroindustriale, zootecnica. NON a terra (nessun consumo di suolo).
   - Beneficiari: Imprenditori agricoli, imprese agroindustriali, cooperative e consorzi (anche in forma aggregata).
   - Spese complementari ammesse: rimozione amianto, isolamento termico coperture, sistemi di aerazione, accumulatori (batterie), infrastrutture ricarica elettrica per mezzi aziendali.
   - Tempistiche: Apertura sportello GSE il 10 marzo 2026 ore 12:00. Chiusura il 09 aprile 2026 ore 12:00.
   - Procedura: a sportello (ordine cronologico fino ad esaurimento fondi).
   - Fine lavori: entro 18 mesi dalla concessione del contributo.
3. CHIAREZZA: Sii espositivo ma diretto. Usa elenchi puntati per facilitare la lettura.
4. RISCHI: Ricorda agli utenti che essendo una procedura "A SPORTELLO" l'ordine cronologico è fondamentale, quindi la documentazione deve essere pronta prima del 10 Marzo 2026.
5. Se un utente fa una simulazione economica, usa i dati in input ma ricordagli sempre che i limiti specifici di spesa (es. €/kW per batterie o €/mq per amianto) dipendono dai massimali GSE.
"""

@tool
def cerca_linee_guida_agrisolare(query: str) -> str:
    """Usa questo strumento per cercare approfondimenti online sulle linee guida GSE e MASAF per il Parco Agrisolare 2026, massimali di spesa e regole specifiche non presenti nel tuo prompt di base."""
    try:
        # Se c'è la chiave Tavily la usa per approfondimenti, altrimenti fallback morbido.
        if os.environ.get("TAVILY_API_KEY"):
            search = TavilySearchResults(max_results=5, search_depth="basic")
            structured_query = f"{query} bando agrisolare 2026 masaf gse"
            results = search.run(structured_query)
            
            if isinstance(results, list):
                formatted_results = []
                for r in results:
                    formatted_results.append(f"Titolo: {r.get('title', '')}\nContenuto: {r.get('content', '')}")
                return "\n\n".join(formatted_results)
            return str(results)
        else:
            return "Ricerca online non disponibile (Manca TAVILY_API_KEY). Usa le tue conoscenze di base sul Bando Agrisolare 2026."
    except Exception as e:
        return f"Errore di ricerca web: {str(e)}"

def get_rag_chain():
    """
    RAG chain initialization connecting to GPT-4o-mini with specific tools for Agrisolare.
    """
    tools = [cerca_linee_guida_agrisolare]
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor
