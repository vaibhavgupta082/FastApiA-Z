import google.generativeai as genai
import os

# 1. Setup your API Key
# Replace '' with your actual key
my_api_key = 'YOUR_SECRET_KEY'


# Configure the library
genai.configure(api_key=my_api_key)

# 2. Initialize the Model
# "gemini-1.5-flash" is currently the fastest and most cost-effective model
model = genai.GenerativeModel('gemini-2.5-flash')


try:
    # 3. Send the request
    prompt = "Explain how AI works in one sentence."
    response = model.generate_content(prompt)

    # 4. Print the result
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")