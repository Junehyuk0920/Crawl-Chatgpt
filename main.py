import subprocess, time, os, sys, socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.stdout.reconfigure(encoding='utf-8')

def is_chrome_running(port=9222):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

if not is_chrome_running(port=9222):
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
    time.sleep(2)

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=option)

###################################

# answering = False

if "chatgpt.com" not in driver.current_url:
    driver.get('https://chatgpt.com/')
    time.sleep(3)

def getResult(tag, nest=0, temp=[]):
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

                    getResult(ul_in_li, nest+1, temp)
                    
            return temp + ['\n']

    return None

final = []

def inputQuery(query):
    if not query: return

    global answering

    answering = True
    
    inputDOM = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]/p')
    inputDOM.send_keys(query)
    inputDOM.send_keys(Keys.ENTER)
    time.sleep(7)

    section = driver.find_elements(By.XPATH, '//section')
    currSection = section[-1]
    answers = currSection.find_elements(By.XPATH, './div/div/div/div/div/div/*')
    
    for tag in answers:
        res = getResult(tag)

        if not res: continue

        if type(res) == list:
            for elem in res:
                final.append(elem)
        else:
            final.append(res)

        # file.write(str(res) + '\n')

    # print()
    
    # answering = False
    time.sleep(3)

# talk = len(os.listdir('./logs'))
# full_filename = f"log_{talk}.txt"
# file = open("logs/"+full_filename, "w", encoding="utf-8")
        
query = sys.argv[1] if len(sys.argv) > 1 else '입력값이 없습니다.'             
inputQuery(query)

print('\n'.join(final))

# file.close()