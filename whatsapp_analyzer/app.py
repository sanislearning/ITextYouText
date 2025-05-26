import re  # Regular expressions module for pattern matching
from collections import defaultdict  # For creating a default dictionary with int (starting from 0)
import os  # Used for file operations like saving/removing temporary files
from flask import Flask, render_template, request  # Flask tools

# render_template: Loads an HTML file from a folder called "templates"
# request: Lets you access files or data sent from the browser

# Create a Flask web application instance
app = Flask(__name__)

def parse_whatsapp_chat(file_path):
    patterns = [
        r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?\s?[APMapm\.]*)\]\s(.*?):\s(.+)', #iphone-style pattern
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?\s?[APMapm\.]*)\s*[-\]]\s*(.*?):\s(.+)' #android-style pattern
    ]

    message_counts = defaultdict(int) #tracks number of messages sent by each person
    total_words = defaultdict(int) #tracks total number of words
    current_sender = None #stores sender's name so we can handle multi-line messages

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip() #removes leading and trailing white spaces.
            match = None

            for pattern in patterns: #tries each pattern till a match is found
                match = re.match(pattern, line) 
                if match:
                    if len(match.groups()) == 4:
                        current_sender = match.group(3) #sender's name
                        message = match.group(4) #actual message
                    elif len(match.groups()) == 3:
                        current_sender = match.group(2)
                        message = match.group(3)
                    break

            if match:
                message_counts[current_sender] += 1 #increases sender message count
                total_words[current_sender] += len(message.split()) #adds number of words in the message
            elif current_sender:
                # Multi-line message
                total_words[current_sender] += len(line.split()) #adds words to last sender's count, no increment of message_counts

    result = {
        sender: {
            'message': message_counts[sender], #message: total messages
            'avg_words': round(total_words[sender] / message_counts[sender], 2) #average words per message
        }
        for sender in message_counts
    }

    return {
        'labels': list(result.keys()),
        'messages': [v['message'] for v in result.values()],
        'avg_words': [v['avg_words'] for v in result.values()]
    }


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
