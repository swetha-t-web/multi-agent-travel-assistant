from typing import TypedDict, List
class TravelState(TypedDict):
    user_input: str
    client_name: str
    travel_dates: str
    destination_city: str
    budget: str
    interests: str
    missing_fields: List[str]
    clarification_question: str
    flight_result: str
    hotel_result: str
    itinerary_result: str
    final_response: str