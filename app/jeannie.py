import google.generativeai as genai

GOOGLE_API_KEY = "<YOUR-API-KEY>"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_content(prompt):

    response = model.generate_content(prompt)

    return response.text
