import re  # Regular expressions module for pattern matching
from collections import defaultdict  # For creating a default dictionary with int (starting from 0)
import os  # Used for file operations like saving/removing temporary files
from flask import Flask, render_template, request  # Flask tools

# render_template: Loads an HTML file from a folder called "templates"
# request: Lets you access files or data sent from the browser

# Create a Flask web application instance
app = Flask(__name__)

# Function to parse the WhatsApp chat file and count messages by each sender
def parse_whatsapp_chat(file_path):
    # Pattern to detect message lines in the format: date, time - name: message
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), \d{1,2}:\d{2}\s?(?:AM|PM)? - (.*?):'
    counts = defaultdict(int)  # Dictionary to store message counts

    # Open and read the chat file
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(pattern, line)  # Check if the line matches the WhatsApp format
            if match:
                sender = match.group(2)  # Extract the sender's name
                counts[sender] += 1  # Increment their message count
    return dict(counts)  # Convert defaultdict to a normal dictionary and return it

# Route for the home page ("/") with both GET and POST methods
@app.route('/', methods=['GET', 'POST'])
def index():
    chat_info = None  # Will store parsed chat data

    # If the form was submitted (POST request)
    if request.method == 'POST':
        file = request.files['chatfile']  # Get the uploaded file

        # Check if it's a .txt file
        if file and file.filename.endswith('.txt'):
            filepath = os.path.join('temp.txt')  # Save it temporarily
            file.save(filepath)

            # Parse the file and get message counts
            chat_info = parse_whatsapp_chat(filepath)

            # Remove the temporary file after processing
            os.remove(filepath)

    # Load the index.html template and pass the chat_info dictionary to it
    return render_template('index.html', chat_info=chat_info)

# Start the Flask development server if this script is run directly
if __name__ == "__main__":
    app.run(debug=True)  # debug=True gives useful error messages while developing
