import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.core.state import AgentState
# Import tool retrieve_booking_status & book_hotel
from app.tools.hotel_tools import check_hotel_availability, book_hotel, retrieve_booking_status
from app.tools.knowledge_tool import consult_travel_guide
from app.tools.calendar_tool import check_user_calendar
# Import tool book_flight BARU
from app.tools.flight_tools import search_flights, book_flight 

load_dotenv()

# Setup LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0, 
    max_retries=2,
)

# Daftar Tools (Total 7 Tools sekarang)
tools = [
    check_user_calendar, 
    search_flights, 
    consult_travel_guide, 
    check_hotel_availability, 
    book_hotel,
    book_flight, # <--- Masukkan Tool Baru
    retrieve_booking_status
]
llm_with_tools = llm.bind_tools(tools)

# --- SYSTEM PROMPT ---
def create_system_prompt(profile_data: str):
    return SystemMessage(content=f"""
Kamu adalah VOYAGER, asisten travel otonom dengan akses database.

INFORMASI USER:
{profile_data}

TUGAS UTAMA:
1. Cek Kalender (`check_user_calendar`).
2. Cari Hotel (`check_hotel_availability`).
3. Cari Pesawat (`search_flights`).
4. Eksekusi Booking Hotel (`book_hotel`).
5. Eksekusi Booking Pesawat (`book_flight`).
6. Cek Status (`retrieve_booking_status`).

ATURAN BOOKING (WAJIB DIPATUHI):
- Jika user ingin booking HOTEL -> Gunakan `book_hotel`.
- Jika user ingin booking PESAWAT -> Gunakan `book_flight` (JANGAN gunakan book_hotel).
- Jangan panggil `search_flights` lagi saat user sudah minta booking.

ATURAN OUTPUT:
Teruskan data JSON dari tool apa adanya jika mengandung marker:
`:::HOTEL_DATA:::`, `:::FLIGHT_DATA:::`, `:::BOOKING_DATA:::`, atau `:::CALENDAR_DATA:::`.
""")

# --- NODE CHATBOT DENGAN INTERCEPTOR ---
def chatbot(state: AgentState):
    messages = state["messages"]
    
    # 1. Identifikasi output tool terbaru
    recent_tool_messages = []
    for msg in reversed(messages):
        if isinstance(msg, AIMessage): 
            break 
        if isinstance(msg, ToolMessage):
            recent_tool_messages.append(msg)
            
    # 2. Interceptor: Jika tool mengembalikan data visual, bypass LLM
    if recent_tool_messages:
        combined_content = "\n".join([m.content for m in recent_tool_messages])
        markers = [":::HOTEL_DATA:::", ":::FLIGHT_DATA:::", ":::BOOKING_DATA:::", ":::CALENDAR_DATA:::"]
        
        if any(marker in combined_content for marker in markers):
            return {"messages": [AIMessage(content=combined_content)]}

    # 3. Normal Flow
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Bangun Graph
graph_builder = StateGraph(AgentState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

app = graph_builder.compile()

# --- WRAPPER UTAMA ---
def process_chat(user_input: str, user_profile: dict):
    context_str = f"""
    - NAMA: {user_profile.get('name', 'Tamu')}
    - BUDGET: {user_profile.get('budget', '0')}
    - PREFERENSI: {user_profile.get('interests', '-')}
    """
    sys_msg = create_system_prompt(context_str)
    inputs = {"messages": [sys_msg, HumanMessage(content=user_input)]}
    result = app.invoke(inputs)
    return result["messages"][-1].content