from flask import Flask, jsonify, request
import sqlite3
import openai

app = Flask(__name__)
openai.api_key = 'your-openai-api-key' # use your own api-key

# Function to query the database
def query_database(query):
    conn = sqlite3.connect('myntra_data.db')
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.close()
    return results

# Function to query GPT
def query_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[{"role": "system", "content": "You are a helpful assistant."},  # You can customize this
                  {"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7,
    )
    
    # Extract and return the message from the response
    return response['choices'][0]['message']['content']
        
# Main endpoint for querying products via a prompt
@app.route('/query', methods=['POST'])
def query_products():
    user_prompt = request.json['prompt']

    query = "SELECT * FROM electronics"
    
    # Fetch product data
    products = query_database(query)

    # Convert products into a human-readable form to feed into GPT
    product_descriptions = "\n".join([
        f"{p[1]} - Price: {p[2]}, Rating: {p[5]}, Reviews: {p[6]}"
        for p in products
    ])

    # Create a prompt for GPT-3 that includes the user's query and the product data
    prompt = f"Here are some electronics products:\n\n{product_descriptions}\n\nNow, based on this information, {user_prompt}"

    # Query GPT with the prompt
    gpt_response = query_gpt(prompt)

    # Return the GPT response to the user
    return jsonify({"response": gpt_response})

if __name__ == '__main__':
    app.run(debug=True)
