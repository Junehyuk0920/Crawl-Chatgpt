import subprocess, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=option)

###################################

answering = False

driver.get('https://chatgpt.com/')
time.sleep(3)

def getResult(tag, nest=0, temp=[], ul_in_li_boolean=False):
    match tag.tag_name:
        case 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'p':
            return tag.text
        
        case 'hr':
            return '-'*30
        
        case 'pre':
            span = tag.find_element(By.XPATH, './code').text
            lines = ['\t' + line for line in list(span.split('\n'))]
            return ['(pre)'] + lines + ['(pre)\n']
        
        case 'ul' | 'ol':
            lis = tag.find_elements(By.XPATH, './li')

            for li in lis:
                temp.append(' ' + ' '*(nest+1) + '- ' + list(li.text.split('\n'))[0])
                
                if li.find_elements(By.XPATH, './ul'):
                    ul_in_li = li.find_element(By.XPATH, './ul')

                    getResult(ul_in_li, nest+1, temp, True)
                    nest -= 1
                    
            return temp + ['\n']

    return None
        

def inputQuery(query):
    if not query: return

    answering = True
    
    inputDOM = driver.find_element(By.XPATH, '//*[@id="mobile-composer-prompt"]')
    inputDOM.send_keys(query)
    inputDOM.send_keys(Keys.ENTER)
    time.sleep(15)

    li = driver.find_elements(By.XPATH, '//li[@class="_wdUoQG_messageTurn"]')
    lastLi = li[-1]

    answers = lastLi.find_elements(By.XPATH, './div/div/div/*')

    print('ChatGPT :\n')
    
    for tag in answers:
        res = getResult(tag)

        if type(res) == list:
            for elem in res:
                print(elem)
        else:
            print(res)

        file.write(str(res) + '\n')

    print()
    
    answering = False
    time.sleep(3)

talk = 1

while True:
    if not answering:
        full_filename = f"log_{talk}.txt"

        file = open("logs/"+full_filename, "w", encoding="utf-8")
        print(f"{full_filename}")
        
        query = input('User : ').strip()                
        inputQuery(query)

        file.close()
        talk += 1
