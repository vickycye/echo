from flask import Flask, render_template, request
import openai
import requests

# Set up Flask app
app = Flask(__name__)

# Initialize conversation history list
conversation_history = []

# Function to call OpenAI API
def get_openai_response(prompt):

    # Define your OpenAI API key
    api_key = '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'

    # Define the API endpoint
    endpoint = 'https://api.openai.com/v1/chat/completions'

    # Set up request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Define your prompt message
    prompt_message = prompt

    # Set up request body
    data = {
        'model': 'gpt-3.5-turbo',  # Specify the model you want to use
        'messages': [{'role': 'system', 'content': prompt_message}],
        'max_tokens': 50  # Adjust max_tokens as needed
    }

    # Make API call to OpenAI to generate completions
    response = requests.post(endpoint, json=data, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        # Print the completion response
        return data['choices'][0]['message']['content']
    else:
        # Print error message if request was not successful
        return response.status_code + ": " + response.text

# Route to home page
@app.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        user_message = request.form['user_message']
        ai_response = get_openai_response(user_message)
        
        # Add user message and AI response to conversation history
        conversation_history.append(('user', user_message))
        conversation_history.append(('AI', ai_response))
        
        return render_template('chatdemo.html', conversation_history=conversation_history)
    
    return render_template('chatdemo.html', conversation_history=[])
if __name__ == '__main__':
    app.run(debug=True)