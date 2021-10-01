import re

def validate_username(content):
    if re.match("^[a-zA-Z0-9]+$", content) and len(content)>=6:
        return True  
            

def validate_password(content):
    if re.match("^[a-zA-Z0-9]+$", content) and len(content)>=6:
        return True  
            