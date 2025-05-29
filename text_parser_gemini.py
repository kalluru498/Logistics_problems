# text_parser_gemini.py
import google.generativeai as genai
import pandas as pd

# Initialize Gemini
API_KEY = "your-gemini-api-key-here"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Prompt template to extract structured data
def extract_structured_data(user_text: str):
    prompt = f"""
    You are a logistics AI assistant. A customer will describe the doors they want to ship and the truck or trailer they'll use. 
    Extract the structured data into two sections:

    1. DOORS: a list of door dictionaries with keys: door_type, width_in, height_in, weight_kg, material
    2. TRAILER: a dictionary with keys: vehicle_type, length_in, width_in, height_in, max_weight_kg

    Input:
    """
    prompt += user_text + "\nOutput in JSON."

    response = model.generate_content(prompt)
    try:
        parsed_json = response.candidates[0].content.parts[0].text
        data = eval(parsed_json)  # You may replace this with `json.loads()` for safer parsing
        doors_df = pd.DataFrame(data['DOORS'])
        trailer = data['TRAILER']
        return doors_df, trailer
    except Exception as e:
        return None, None

# Prompt for human-readable instructions
def generate_guidance(doors_df, instructions):
    door_summary = doors_df.to_dict(orient='records')
    prompt = f"""
    You're a loading assistant. Convert these technical loading steps into human-friendly instructions for the customer.
    Door Batch: {door_summary}
    Instructions: {instructions}
    Respond in a polite and easy-to-follow format.
    """
    response = model.generate_content(prompt)
    return response.text.strip()
