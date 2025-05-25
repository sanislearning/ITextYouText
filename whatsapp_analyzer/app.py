import re
from collections import defaultdict
import os
from flask import Flask, render_template, request #render_template finds the HTML file in templates and processes it
#request lets you access user content

app=Flask(__name__) #creates a Flask instance

def parse_whatsapp_chat(file_path):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), \d{1,2}:\d{2}\s?(?:AM|PM)? - (.*?):'
    counts=defaultdict(int)

    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            match=re.match(pattern,line)
            if match:
                sender=match.group(2)
                counts[sender]+=1
    return dict(counts)

@app.route('/',methods=['GET','POST'])  #sets up a route, runs function below
# / is the root URL of the website
# GET is default, just a request to view the page
# POST happens when you submit data to the webpage
def index():
    chat_info=None
    if request.method=='POST':
        file=request.files['chatfile']
        if file and file.filename.endswith('.txt'):
            filepath=os.path.join('temp.txt')
            file.save(filepath)
            chat_info=parse_whatsapp_chat(filepath)
            os.remove(filepath)
    return render_template('index.html',chat_info=chat_info)

if __name__=="__main__":
    app.run(debug=True)