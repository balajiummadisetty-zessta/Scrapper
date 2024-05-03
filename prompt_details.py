def get_prompt_messages(website_text_stripped):

    prompt_messages = [
            {
            "role": "system",
            "content": "You are a helpful assistant that can access external functions. The responses from these function calls will be appended to this dialogue. Please provide responses based on the information from these function calls.",
            },
            {
            "role": "user",
            "content": f"""I am giving you text scraped from a webpage that contains a real estate listing, text_data: ```{website_text_stripped}``` Please check the given function calling json schema and convert the text into json format with key and pair value in json structure and give me all the required fields as mandatory and where you can't find any data set that as NULL. Given json format: """,
            }
        ]
    return prompt_messages


def get_prompt_functions(schema):
    prompt_functions = [
            {
                
            
                "name": "get_listing_details",
                "description": f"Given a piece of text that contains real estate listing information for a property, this function pulls out the relevant fields described in the schema below, NOTE: if you didn't find any value then just give it as NULL please give the value only if proper value is found else None",
                "parameters": {
                    "type": "object",
                    "properties": schema,
                    "required": list(schema.keys())
                    }
            }
            
        ]
    return prompt_functions


prompt_function_call = {"name":"get_listing_details"}

prompt_model = "gpt-3.5-turbo"