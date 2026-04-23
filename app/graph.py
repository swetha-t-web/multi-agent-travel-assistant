from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.config import MODEL_NAME
from app.state import TravelState
from app.knowledge import build_vectorstore
model = ChatOllama(model=MODEL_NAME)
vectorstore = build_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

interaction_prompt = ChatPromptTemplate.from_template("""
You are a travel intake assistant.

Read the user's trip request and extract:
- client_name
- travel_dates
- destination_city
- budget
- interests

If any field is missing, list it in missing_fields.

User input:
{user_input}

Return plain text exactly like this:
client_name=...
travel_dates=...
destination_city=...
budget=...
interests=...
missing_fields=...
""")

def interaction_agent(state: TravelState):
    chain = interaction_prompt | model
    response = chain.invoke({"user_input": state["user_input"]}).content

    parsed = {
        "client_name": "",
        "travel_dates": "",
        "destination_city": "",
        "budget": "",
        "interests": "",
        "missing_fields": []
    }

    for line in response.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key == "missing_fields":
                parsed["missing_fields"] = [v.strip() for v in value.split(",") if v.strip()]
            elif key in parsed:
                parsed[key] = value

    return parsed

clarification_prompt = ChatPromptTemplate.from_template("""
You are a travel assistant.

The following fields are missing:
{missing_fields}

Ask one friendly follow-up question to collect the missing details from the user.
""")

def clarification_agent(state: TravelState):
    chain = clarification_prompt | model
    response = chain.invoke({
        "missing_fields": ", ".join(state["missing_fields"])
    }).content

    return {
        "clarification_question": response,
        "final_response": response
    }

def flight_booking_agent(state: TravelState):
    return {
        "flight_result": f"Flight: Your flight ticket for {state['client_name']} is confirmed on {state['travel_dates']}."
    }

def hotel_booking_agent(state: TravelState):
    return {
        "hotel_result": f"Hotel: Your hotel booking for {state['client_name']} is confirmed for {state['travel_dates']}."
    }

itinerary_prompt = ChatPromptTemplate.from_template("""
You are a travel itinerary planning assistant.

Destination city:
{destination_city}

User interests:
{interests}

Retrieved travel context:
{context}

If enough city information is available, create a simple day-by-day itinerary.
If not enough information is available, use this default plan:

Day 1: City shopping
Day 2: Movies, beaches, and nearby attractions

Keep the answer clear and practical.
""")

def itinerary_agent(state: TravelState):
    city = state["destination_city"].strip()
    interests = state["interests"].strip()

    if not city:
        return {
            "itinerary_result": "Itinerary:\nDay 1: City shopping\nDay 2: Movies, beaches, and nearby attractions"
        }

    retrieved_docs = retriever.invoke(f"{city} travel itinerary for {interests}")
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    chain = itinerary_prompt | model
    response = chain.invoke({
        "destination_city": city,
        "interests": interests,
        "context": context
    }).content

    return {"itinerary_result": f"Itinerary:\n{response}"}

final_prompt = ChatPromptTemplate.from_template("""
You are the final travel assistant.

Combine the outputs below into one final user-friendly response:

{flight_result}

{hotel_result}

{itinerary_result}
""")

def final_response_agent(state: TravelState):
    chain = final_prompt | model
    response = chain.invoke({
        "flight_result": state["flight_result"],
        "hotel_result": state["hotel_result"],
        "itinerary_result": state["itinerary_result"]
    }).content

    return {"final_response": response}

def route_after_interaction(state: TravelState) -> Literal["clarification_agent", "flight_booking_agent"]:
    if state["missing_fields"]:
        return "clarification_agent"
    return "flight_booking_agent"

builder = StateGraph(TravelState)
builder.add_node("interaction_agent", interaction_agent)
builder.add_node("clarification_agent", clarification_agent)
builder.add_node("flight_booking_agent", flight_booking_agent)
builder.add_node("hotel_booking_agent", hotel_booking_agent)
builder.add_node("itinerary_agent", itinerary_agent)
builder.add_node("final_response_agent", final_response_agent)
builder.add_edge(START, "interaction_agent")
builder.add_conditional_edges("interaction_agent", route_after_interaction)
builder.add_edge("clarification_agent", END)
builder.add_edge("flight_booking_agent", "hotel_booking_agent")
builder.add_edge("hotel_booking_agent", "itinerary_agent")
builder.add_edge("itinerary_agent", "final_response_agent")
builder.add_edge("final_response_agent", END)

checkpointer = InMemorySaver()
travel_graph = builder.compile(checkpointer=checkpointer)