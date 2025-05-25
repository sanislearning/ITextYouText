#Simple script version of the project
import re
from collections import defaultdict
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
chatinfo=parse_whatsapp_chat() #add your file path here
print(chatinfo)