from selenium import webdriver
from config import store_input, store_dropdown, continue_buttons, stores, default_shipping
from PIL import Image
import pytesseract
import time
import string
import re
def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print((endTime - startTime)/1000, 's')
        return result
    return wrapper

# will cookies improve load time?
#options = webdriver.ChromeOptions()
#options.add_argument('user-data-dir=www.supremenewyork.com')

################################################################################
##    ###                      #######    #######                      ##    ###
## ##  ##  Reading Image       ######  ##########  Reading Image       ## ##  ##
##    ###                      #########  #######                      ##    ###
## ##  ##############################    ################################ #   ##
################################################################################
def read_image():
    img  = Image.open("./label1.JPG")
    raw_text=pytesseract.image_to_string(img)
    shipping_args=read_shipping(raw_text)
    if shipping_args[2] is "":
        img=img.rotate(180)
        raw_text=pytesseract.image_to_string(img)
        shipping_args=read_shipping(raw_text)
    return shipping_args
def read_shipping(raw_text):

    print(raw_text)
    info_bits=raw_text.split("\n")
    binary_string="" # detect number/letter/number pattern over lines
    count=-1
    for line in info_bits:
        count+=1
        index=0
        for word in line.split():
            for char in word:
                if char.isdigit() or char.isalpha():
                    index+=len(word)+1
                    break
            else:
                line=line[:index]+line[index+len(word)+1:]
                info_bits[count]=line
    print(info_bits)
    while("" in info_bits): 
        info_bits.remove("")
    temp=[]
    for line in info_bits:
        if  not line.isspace():
            temp.append(line)
        else:
            pass
    info_bits=temp
    print(info_bits)
    count=-1
    for line in info_bits:
        count+=1
        try:
            print("TO" in line.split()[0]  or "SHIP" in line.split()[0])
            print("line:", line)
            if "TO:" in line.split()[0] or "SHIP" in line.split()[0]:
                line=line[len(line.split()[0])+1:]
                info_bits[count]=line    
            if line[0].isdigit():
                binary_string += "0"
            elif line[0].isalpha():
                if " CA" in line:
                    binary_string+="C"
                else:
                    binary_string += "1"
            else:
                binary_string += "N"
        except Exception as e:
            print(e)
            binary_string += "N"
    print(binary_string)
    addresses=[m.start() for m in re.finditer('10C', binary_string)]
    shipping_args=["","","","",""]
    print(addresses)
    for address in addresses:
        shipping_args[0]=info_bits[address].split()[0]
        print(shipping_args[0])
        shipping_args[1]=info_bits[address].split()[1]
        shipping_args[2]=info_bits[address+1]
        shipping_args[3]=info_bits[address+2][:re.search(r"\d", info_bits[address+2]).start()]
        shipping_args[4]=info_bits[address+2][len(shipping_args[3])-1:].split()[0]
    print(shipping_args)
    #Shipping args: fname, lname, street_address, city, zip
        
    return shipping_args

        

################################################################################
###    ##                      #######    #######                      ###    ##
##  #####  Shipping @ Payment  ######  ##########  Shipping @ Payment  ##  #####
#####  ##                      #########  #######                      #####  ##
##    ###############################    ################################    ###
################################################################################

def getSandP(fname, lname, street_address, city, zip):
    default=default_shipping
    default["fname"]=fname
    default["lname"]=fname
    default["street_address"]=street_address
    default["city"]=city
    default["zip_code"]=zip
    return default
################################################################################
##     ##                      ######      ######                      ##     ##
#### ####   Typing Functions   ########  ########   Typing Functions   #### ####
#### ####                      ########  ########                      #### ####
################################################################################
################################################################################


def slow_type(element, text):
    for char in text:
        element.send_keys(char)
    return
def fast_type(element, text):
    element.send_keys(text)
    return



## press_continue_iframe() is also depricated but I dont want to move it down yet because I might need to emulate it later
   
def press_continue_iframe():
    try:
        print("started")
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))#contains(@name, 'Stripe')]"))
        press_continue()
        driver.switch_to.parent_frame()
        return True
    except:
        pass
    return False
################################################################################
##     ##                      ######      ######                      ##     ##
#### ####      Input Types     ########  ########      Input Types     #### ####
##     ##                      ######      ######                      ##     ##
################################################################################ 
def store_inputs(info):
    change=False
    for text, xpaths in store_input.items():
        elements=[]
        for xpath in xpaths:
            try: 
                elements.append(driver.find_element_by_xpath(xpath))
            except:
                pass
        for element in elements:
            try:
                fast_type(element, info[text])
                if element.get_attribute('value')!=info[text]:
                    element.clear()
                    slow_type(element, info[text])
                change= True
            except:
                pass
    return change
def store_dropdowns():
    change=False
    for choice_name, dropdown_xpaths in store_dropdown.items():
        dropdowns=[]
        for dropdown_xpath in dropdown_xpaths:
            try:
                dropdowns.append(driver.find_element_by_xpath(dropdown_xpath))
            except:
                pass
        for dropdown in dropdowns:
            try:
                dropdown.find_element_by_xpath(choice_name).click()
                change= True
            except:
                pass
        return change
def page_iframe(info):
    filled=[False]
    try:
        iframes=driver.find_elements_by_xpath("//iframe")
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)#contains(@name, 'Stripe')]"))
                print("iframe found")
                filled.append(page_complete(info))
                driver.switch_to.parent_frame()
            except:
                print("nothing there")
    except:
        pass
    return any(filled)

################################################################################
##     ##                      ######     #######                      ##     ##
##  ##  #      Page Fill       ######  ##  ######      Page Fill       ##  ##  #
##     ##                      ######     #######                      ##     ##
##  #################################  ##################################  #####
################################################################################
def page_complete(info):
    a=[]
    a.append(store_inputs(info))
    a.append(store_dropdowns())
    a.append(page_iframe(info))
    return any(a)

def continue_button():
    for button in continue_buttons:
        try:
            all=driver.find_elements_by_xpath(button)
            print(len(all))
            for those in all:
                try:
                    those.click()
                    print("found iteratively")
                    return True
                except Exception as E:
                    print(E)
                    pass
        except:
            pass
    print("didnt find " + button +" iteratively:")
    return False

def shoplocal_password(product):
    driver.find_element_by_xpath('//*[@id="shopify-section-password-header"]/header/div/p/a').click()
    driver.find_element_by_xpath('//*[@id="password"]').send_keys("savesc2020")
    driver.find_element_by_xpath('//*[@id="login_form"]/div/span/input').click()
    time.sleep(1)
    driver.get(product)
    time.sleep(1)
    return
def shoplocal_localdel():
    driver.get("https://shop-local-sc.myshopify.com/admin/apps/local-delivery/delivery-lists/new")
    driver.find_element_by_xpath('//*[@id="account_email"]').send_keys("ramissirian@gmail.com")
    driver.find_element_by_xpath('//*[@id="body-content"]/div[1]/div[2]/div/form/button').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="account_password"]').send_keys("Phirephox#1")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="login_form"]/div[2]/ul/button').click()
    #driver.find_element_by_xpath('//*[@id="body-content"]/div[1]/div[2]/div/div/a[1]/div[1]/div/div[2]/div[1]').click()
    time.sleep(5)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="AppFrameMain"]/div/div/iframe'))

    driver.find_element_by_xpath('//*[@id="unassigned-orders-content"]/div/div/div/div[2]/div/div[1]/div[2]/div').click()
    driver.find_element_by_xpath('//*[@id="unassigned-orders-content"]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/button/span/span').click()
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/button/span/span').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div/div/div/div[3]/div/div/div[2]/div/div[2]/button/span/span').click()
    driver.switch_to.parent_frame()
    driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[4]/div/div/div[2]/div/div/div[2]/button/span/span').click()
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="AppFrameMain"]/div/div/iframe'))
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/a/span/span').click()
    time.sleep(3)
    print(driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/a').get_attribute('href'))
    
    return link

def section(info):
    a=[]
    a.append(page_complete(info))
    print("A")
    time.sleep(3)
    a.append(continue_button())
    print("B")
    time.sleep(5)
    print(a)
    return any(a)
    #process_payment.click()
@timeme
def orders(info):
    #driver.find_element_by_xpath("//*[text()='CHECKOUT']").click()
    time.sleep(1)
    while section(info):
        pass
    return
def close_popup():
    try:
        driver.find_element_by_xpath("//*[contains(@class, 'leadform-popup-close')]").click()
        #driver.switch_to.parent_frame()
        return True
    except:
        pass
    print("failed at stage: CLOSE")
    return
def add_to_cart():
    # try:
    #     driver.find_element_by_xpath('//*[@id="AddToCartText"]').click()
    #     return
    # except:
    #     pass
    try:
        driver.find_element_by_xpath("//button//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart')]/..").click()
        return
    except Exception as e:
        print(e)
        pass
    try:
        driver.find_element_by_xpath("//*[contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart')]").click()
        return
    except Exception as e:
        print(e)
        pass
    print("failed to add to cart")

def get():
    # add to cart
    try:
        add_to_cart()
    except:
        time.sleep(2)
        close_popup()
        add_to_cart()
    

if __name__ == '__main__':
        # load chrome
    #read_image()
    info=getSandP("Hobert", "Herald", "121 Peach Terrace", "Santa Cruz", "95060")
    driver = webdriver.Chrome()
    product=0
    checkout=0
    for store, products in stores.items():
        for checkout, product in products.items():    
        # get product url
            print(product)
            driver.get(product[0])
            shoplocal_password(product[0])# for shoplocal bot
            get()
            time.sleep(2)
            driver.get(checkout)
            orders(info)
            shoplocal_localdel()


######### DEPRICATED FUNCTIONS ################## DEPRICATED FUNCTIONS #########
#########                      ##################                      #########
################################################################################
#########                      ##################                      #########
######### DEPRICATED FUNCTIONS ##   ########   ## DEPRICATED FUNCTIONS #########
#########                      ####  ######  ####                      #########
####################################  ####  ####################################
#########                      ######  ##  ######                      #########
######### DEPRICATED FUNCTIONS #######    ####### DEPRICATED FUNCTIONS #########
#########                      ######  ##  ######                      #########
####################################  ####  ####################################
#########                      ####  ######  ####                      #########
######### DEPRICATED FUNCTIONS ##   ########   ## DEPRICATED FUNCTIONS #########
#########                      ##################                      #########
################################################################################
#########                      ######      ######                      #########
######### DEPRICATED FUNCTIONS ######      ###### DEPRICATED FUNCTIONS #########
#########                      ######      ######                      #########
################################################################################
#########                      ##################                      #########
######### DEPRICATED FUNCTIONS ##   ########   ## DEPRICATED FUNCTIONS #########
#########                      ####  ######  ####                      #########
####################################  ####  ####################################
#########                      ######  ##  ######                      #########
######### DEPRICATED FUNCTIONS #######    ####### DEPRICATED FUNCTIONS #########
#########                      ######  ##  ######                      #########
####################################  ####  ####################################
#########                      ####  ######  ####                      #########
######### DEPRICATED FUNCTIONS ##   ########   ## DEPRICATED FUNCTIONS #########
#########                      ##################                      #########
################################################################################
#########                      ##################                      #########
######### DEPRICATED FUNCTIONS ################## DEPRICATED FUNCTIONS #########


def press_continue():
    try:
        driver.find_element_by_xpath("//button//*[contains(text(), 'Next')/..]").click()
        return True
    except:
        print("didnt find 'next'")
        pass
    try:
        all=driver.find_elements_by_xpath("//button//*[contains(text(), 'Next')]/..")
        print(len(all))
        for those in all:
            try:
                those.click()
                print("found iteratively")
                return True
            except Exception as E:
                print(E)
                pass
    except Exception as E:
        print("didnt find 'next' iteratively:")
        print(E)
        pass
    # try:
    #     ant=driver.find_element_by_xpath('//*[@id="wsite-content"]/div/div[1]/div/div[4]/div/div[2]/div/section/form/fieldset/section/button/span').click()
    #     print(ant.text())
    #     return True
    # except Exception as E:
    #     print("found Next Manually")
    #     print(E)
    #     pass
    try:
        driver.find_element_by_xpath("//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]").click()
        return True
    except:
        pass
    try:
        driver.find_element_by_xpath("//button//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]/..").click()
        return True
    except Exception as e:
        print(e)
        pass
    return False


def input_fname():
    text=keys['fname']
    elements=[]
    xpaths=['//input[@name="fname"]',"//input[contains(@name, 'name') and contains(@name, 'first')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath('//input[@name="fname"]').send_keys(keys['fname'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//input[contains(@name, 'name') and contains(@name, 'first')]").send_keys(keys['fname'])
    #     return True
    # except:
    #     pass
    # return False
def input_lname():
    text=keys['lname']
    elements=[]
    xpaths=['//input[@name="lname"]',"//input[contains(@name, 'name') and contains(@name, 'last')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath('//input[@name="lname"]').send_keys(keys['lname'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//input[contains(@name, 'name') and contains(@name, 'last')]").send_keys(keys['lname'])
    #     return True
    # except:
    #     pass
    # return False
def input_email():
    text=keys['email']
    elements=[]
    xpaths=["//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_name('email').send_keys(keys['email'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')]").send_keys(keys['email'])
    #     return True
    # except Exception as e:
    #     print(e)
    #     pass
    # return False
def input_phone_number():
    text=keys['phone_number']
    elements=[]
    xpaths=["//*[contains(@data-test, 'phone')]","//input[contains(@name, 'phone')]","//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') and not(contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email'))]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//*[contains(@data-test, 'phone')]").send_keys(keys['phone_number'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//input[contains(@name, 'phone')]").send_keys(keys['phone_number'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') and not(contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email'))]").send_keys(keys['phone_number'])
    #     return True
    # except Exception as e:
    #     print(e)
    #     pass
    # return False
def input_street_address():
    text=keys['street_address']
    elements=[]
    xpaths=["//*[contains(@name, 'street')]","//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'address') and not(contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email'))]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//*[contains(@name, 'street')]").send_keys(keys['street_address'])

    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'address') and not(contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email'))]").send_keys(keys['street_address'])
    #     return True
    # except Exception as e:
    #     print(e)
    #     pass
    # return False
def input_city():
    text=keys['city']
    elements=[]
    xpaths=["//*[contains(@name, 'city')]","//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'city')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//*[contains(@name, 'city')]").send_keys(keys['city'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'city')]").send_keys(keys['city'])
    #     return True
    # except:
    #     pass
    # return False
def input_zip_code():
    text=keys['zip_code']
    elements=[]
    xpaths=["//*[contains(@name, 'zip')]","//input[contains(@name, 'postal') and contains(@name, 'code')]","//input[contains(@placeholder, 'ZIP')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//*[contains(@name, 'zip')]").send_keys(keys['zip_code'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//input[contains(@name, 'postal') and contains(@name, 'code')]").send_keys(keys['zip_code'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//input[contains(@placeholder, 'ZIP')]").send_keys(keys['zip_code'])
    #     return True
    # except:
    #     pass
    # return False
def input_state():
    text=keys['region'] #region?
    elements=[]
    xpaths=['//*[@name="state"]']
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath('//*[@name="state"]').send_keys(keys['state'])
    #     return True
    # except:
    #     pass
    # return False
def input_card_number():
    text=keys['card_number']
    elements=[]
    xpaths=["//input[contains(@name, 'cardnumber')]","//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card') and contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'number')]","//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card number')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                element.clear()
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//input[contains(@name, 'cardnumber')]").send_keys(keys['card_number'])
    #     return True
    # except:
    #     pass 
    # try:
    #     element=driver.find_element_by_xpath("//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card') and contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'number')]")#.send_keys(keys['card_number'])
    #     fast_type(element, keys['card_number'])
    #     return True
    # except Exception as e:
    #     print(e)
    #     pass 
    # try:
    #     driver.find_element_by_xpath("//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card number')]").send_keys(keys['card_number'])
    #     return True
    # except Exception as e:
    #     print(e)
    #     pass 
    # return False
def input_expiry():
    text=keys['card_expiry']
    elements=[]
    xpaths=["//input[contains(@name, 'exp')]","//input[contains(@placeholder, 'MM') and contains(@placeholder, 'YY')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//input[contains(@name, 'exp')]").send_keys(keys['card_expiry'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//input[contains(@placeholder, 'MM') and contains(@placeholder, 'YY')]").send_keys(keys['card_expiry'])
    #     return True
    # except:
    #     pass
    # return False
def input_card_cvv():
    text=keys['card_cvv']
    elements=[]
    xpaths=["//input[contains(@name, 'cvc')]","//input[contains(@placeholder, 'CVV')]","//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'security')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//input[contains(@name, 'cvc')]").send_keys(keys['card_cvv'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//input[contains(@placeholder, 'CVV')]").send_keys(keys['card_cvv'])
    #     return True
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'security')]").send_keys(keys['card_cvv'])
    #     return True
    # except Exception as e:
    #     print(e)
    #     pass 
    # return False
def dropdown_country():
    try:
        country=driver.find_element_by_xpath("//*[contains(@name, 'country')]")
        country.find_element_by_xpath("//*[contains(@value, 'US')]").click()
        return True
    except:
        pass
    return False
def dropdown_state():
    try:
        region=driver.find_element_by_xpath("//*[contains(@name, 'region')]")
        region.find_element_by_xpath(".//*[contains(@value, 'CA')]").click()
        return True
    except:
        pass
    return False
def order():
    
    # wait for checkout button element to load
    
    driver.find_element_by_xpath("//*[text()='CHECKOUT']").click()
    time.sleep(2)
    # fill out checkout screen fields 
    #driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(keys['name'])
    driver.find_element_by_name('email').send_keys(keys['email'])
    driver.find_element_by_xpath("//button[contains(text(), 'continue')]").click()
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@name="fname"]').send_keys(keys['fname'])
    driver.find_element_by_xpath('//*[@name="lname"]').send_keys(keys['lname'])
    driver.find_element_by_xpath("//*[contains(@name, 'address')]").send_keys(keys['street_address'])
    driver.find_element_by_xpath("//*[contains(@name, 'zip')]").send_keys(keys['zip_code'])
    driver.find_element_by_xpath("//*[contains(@name, 'city')]").send_keys(keys['city'])
    #driver.find_element_by_xpath("//*[contains(@name, 'region')]").click()
    driver.find_element_by_xpath("//*[contains(@value, 'CA')]").click()
    driver.find_element_by_xpath("//*[contains(@data-test, 'phone')]").send_keys(keys['phone_number'])
    time.sleep(1)
    driver.find_element_by_xpath("//button[contains(text(), 'continue')]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//button[contains(text(), 'continue')]").click()
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@name, 'Stripe')]"))
    
    driver.find_element_by_xpath("//input[contains(@name, 'cardnumber')]").send_keys(keys['card_number'])
    driver.find_element_by_xpath("//input[contains(@name, 'exp')]").send_keys(keys['card_expiry'])
    driver.find_element_by_xpath("//input[contains(@name, 'cvc')]").send_keys(keys['card_cvv'])
    driver.switch_to.parent_frame()

    driver.find_element_by_xpath('//*[@name="fname"]').send_keys(keys['fname'])
    driver.find_element_by_xpath('//*[@name="lname"]').send_keys(keys['lname'])
    driver.find_element_by_xpath("//*[contains(@name, 'address')]").send_keys(keys['street_address'])
    driver.find_element_by_xpath("//*[contains(@name, 'zip')]").send_keys(keys['zip_code'])
    driver.find_element_by_xpath("//*[contains(@name, 'city')]").send_keys(keys['city'])
    country=driver.find_element_by_xpath("//*[contains(@name, 'country')]")
    country.find_element_by_xpath("//*[contains(@value, 'US')]").click()
    region=driver.find_element_by_xpath("//*[contains(@name, 'region')]")
    print(region.text)
    region.find_element_by_xpath(".//*[contains(@value, 'CA')]").click()
    driver.find_element_by_xpath("//*[contains(@data-test, 'phone')]").send_keys(keys['phone_number'])
    return

def check_iframe():
    filled=[False]
    try:
        iframes=driver.find_elements_by_xpath("//iframe")
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)#contains(@name, 'Stripe')]"))
                print("iframe found")
                filled.append(check_all())
                driver.switch_to.parent_frame()
            except:
                print("nothing there")
    except:
        pass
    return any(filled)

def check_all():
    check_iframe()
    a=[]
    a.append(input_fname())
    a.append(input_lname())
    a.append(input_email())
    a.append(input_phone_number())
    a.append(input_street_address() )
    a.append(input_city() )
    a.append(input_state())
    a.append(input_zip_code() )
    a.append(input_card_cvv())
    a.append(card_name())
    a.append(input_card_number())
    a.append(input_expiry() )
    a.append(dropdown_state() )
    a.append(dropdown_country())
    return any(a)
def card_name():
    text=keys['card_name']
    elements=[]
    xpaths=["//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card') and contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')]","//input[contains(@placeholder, 'CVV')]"]
    for xpath in xpaths:
        try: 
            elements.append(driver.find_element_by_xpath(xpath))
        except:
            pass
    for element in elements:
        try:
            fast_type(element, text)
            if element.get_attribute('value')!=text:
                slow_type(element, text)
            return True
        except:
            pass
    return False
    # try:
    #     driver.find_element_by_xpath("//*[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'card') and contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'name')]").send_keys(keys['card_name'])
    #     return True
    # except Exception as e:
    #     print(e)
    #     pass 
    # return False