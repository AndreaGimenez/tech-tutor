import json


flight_ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
hotel_prices = {"citizenm":"$200", "nh":"$179", "hilton":"$250", "sheraton":"$300"}

def get_flight_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return flight_ticket_prices.get(city, "Unknown")

flight_price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

def get_hotel_price(hotel_name):
    hotel = hotel_name.lower()
    return hotel_prices.get(hotel, "Unknown")

hotel_price_function = {
    "name": "get_hotel_price",
    "description": "Get the price per night of a hotel. Call this whenever you need to know the hotel price for a night, for example when a customer asks 'How much is a hotel night in this hotel?'",
    "parameters": {
        "type": "object",
        "properties": {
            "hotel_name": {
                "type": "string",
                "description": "The name of the hotel that the customer wants to spend the night into",
            },
        },
        "required": ["hotel_name"],
        "additionalProperties": False
    }
}

def handle_tool_call(message):
    tool_responses = []

    for tool_call in message.tool_calls:
        arguments = json.loads(tool_call.function.arguments)
        print(f"Arguments: {arguments}")

        if tool_call.function.name == "get_ticket_price":
            city = arguments.get('destination_city')
            price = get_flight_ticket_price(city)
            content = json.dumps({"destination_city": city, "price": price})
        
        elif tool_call.function.name == "get_hotel_price":
            hotel = arguments.get('hotel_name')
            price = get_hotel_price(hotel)
            content = json.dumps({"hotel_name": hotel, "price": price})

        else:
            content = json.dumps({"error": "Unknown tool"})

        tool_responses.append({
            "role": "tool",
            "content": content,
            "tool_call_id": tool_call.id
        })
    
    return tool_responses
