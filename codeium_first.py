from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()

def get_ui_elements(webpage_url):
    # Initialize a dictionary to store UI elements and their XPaths
    ui_elements = {}

    # Initialize a WebDriver (you can choose Chrome, Firefox, etc.)
    driver = webdriver.Chrome()

    try:
        # Open the webpage
        driver.get(webpage_url)
        #time.sleep(5000)
        # Find all elements on the page
        elements = driver.find_elements(By.CSS_SELECTOR, "*")
        for element in elements:
            print(element.tag_name, element.get_attribute('xpath'))

        # Assign unique variable names to each element
        for i, element in enumerate(elements):
            variable_name = f"element_{i}"
            ui_elements[variable_name] = element

        # Print the dictionary with variable names and XPaths
        #for variable_name, element in ui_elements.items():
            #print(f"{variable_name}: {element.tag_name} - {element.get_attribute('xpath')}")    

        return ui_elements

    #print all items from the dictionary    
    except KeyError as e:
        print(e)    
    except Exception as e:
        print(e)    
    finally:

        #click on iphone 6 with price $790 using ui_elements variables
        ui_elements["element_0"].click()

        # Close the WebDriver
        #sleep for 10 seconds
        time.sleep(10)
        driver.quit()

# Example usage
webpage_url = "https://demoblaze.com"
#write wait for 5 seconds

ui_elements = get_ui_elements(webpage_url)


