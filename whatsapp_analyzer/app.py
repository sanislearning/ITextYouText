import re  # Regular expressions module for pattern matching
from collections import defaultdict  # For creating a default dictionary with int (starting from 0)
import os  # Used for file operations like saving/removing temporary files
from flask import Flask, render_template, request  # Flask tools

# render_template: Loads an HTML file from a folder called "templates"
# request: Lets you access files or data sent from the browser

# Create a Flask web application instance
app = Flask(__name__)

def parse_whatsapp_chat(file_path):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), \d{1,2}:\d{2}\s?(?:AM|PM)? - (.*?): (.+)'
    message_counts=defaultdict(int)
    total_words=defaultdict(int)

    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            match=re.match(pattern,line)
            if match:
                sender=match.group(2)
                message=match.group(3)
                message_counts[sender]+=1
                word_count=len(message.split()) #Splits messages by space to count words
                total_words[sender]+=word_count

    result={}
    for sender in message_counts:
        avg_words=total_words[sender]/message_counts[sender]
        result[sender]={
            'message':message_counts[sender],
            'avg_words':round(avg_words,2)
        }

    return result

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
