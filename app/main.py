from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import travel_graph
app = FastAPI(title="Multi-Agent Travel Assistant API")

class TravelRequest(BaseModel):
    user_input: str
    thread_id: str = "travel-session-1"


@app.post("/plan-trip")
def plan_trip(request: TravelRequest):
    result = travel_graph.invoke(
        {
            "user_input": request.user_input,
            "client_name": "",
            "travel_dates": "",
            "destination_city": "",
            "budget": "",
            "interests": "",
            "missing_fields": [],
            "clarification_question": "",
            "flight_result": "",
            "hotel_result": "",
            "itinerary_result": "",
            "final_response": ""
        },
        config={"configurable": {"thread_id": request.thread_id}}
    )

    return {"final_response": result["final_response"]}