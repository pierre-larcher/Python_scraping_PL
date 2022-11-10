from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import json
import annonce as an

# Pour le setup du chromeprofile : https://stackoverflow.com/questions/49270109/how-to-open-a-chrome-profile-through-python. ça permet d'installer adblock sur un profil chrome spécifique et donc de pas être embêté par les pubs 

def setup(url):
    """Mise en place des éléments pour le scraping, setup du webdriver et lancement de la page."""
    
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("--profile-directory=Profile 1")
    # REMPLACER LE USERNAME AVANT UTILISATION 
    option.add_argument("--user-data-dir=C:/Users/gamato/AppData/Local/Google/Chrome/User Data")
    #Re-size la taille de la fenêtre
    option.add_argument("window-size=1920,1000")
    # Ajoute un useragent différent
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    driver.maximize_window()
    
    return driver

def kill_banner(driver):
    """Ferme la banner si elle apparait"""
    
    try:
        banner=driver.find_element(By.XPATH, '//*[@id="layr_paruvendupourvous"]/div/span')
        banner.click()
    except:
        pass

def scroll_shim(driver, item):
    """Scroll jusqu'à voir l'objet demandé"""
    
    x = item.location['x']
    y = item.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    driver.execute_script(scroll_by_coord)
    driver.execute_script(scroll_nav_out_of_way)
    
def page(driver):
    """Récupère toutes les annonces de la page (et les pubs malheureusement)"""
    
    kill_banner(driver)

    block_liste = driver.find_element(By.ID, "bloc_liste")

    liste_annonces = [block_liste.find_elements(By.XPATH, '//*[@id="bloc_liste"]/div[{}]/div[1]'.format(i)) for i in range(1,100)]

    liste_annonce_clean = clean_notice(liste_annonces)
    
    return liste_annonce_clean

def get_page_details(driver, liste_annonce_clean, dict_annonces):
    """Ouvre toutes les pages pour récupérer les informations de celles-ci grâce à la classe Annonce."""
    
    for page in liste_annonce_clean:

        kill_banner(driver)
        scroll_shim(driver, page)
        time.sleep(1)
        n=0
        while n<2:
            try:            
                ActionChains(driver) \
                .key_down(Keys.CONTROL) \
                .click(page) \
                .key_up(Keys.CONTROL) \
                .perform()

                driver.switch_to.window(driver.window_handles[1])
                try:
                    new_page = an.Annonce(driver).recuperation()

                    for i in dict_annonces.keys():

                        dict_annonces[i].append(new_page[i])

                    time.sleep(1)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])  
                    time.sleep(1)
                    break

                except Exception as e:
                    print(e)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])  
                    break

            except Exception as e:
                print(e)
                n+=1
                time.sleep(2)
                kill_banner(driver)
                
    return dict_annonces

def clean_notice(liste_annonces):
    """Nettoie la liste des annonces en retirant les objets vides."""
    
    liste_annonce_clean = []
    for i in liste_annonces:
        try:
            liste_annonce_clean.append(i[0])
            
        except:
            pass
    return liste_annonce_clean



def main(url, dict_annonces):
    """Main, enregistre le dictionnaire sous forme de json dans le wd."""
    
    driver = setup(url)
    dict_annonces = get_page_details(driver, page(driver), dict_annonces)
        
    with open("file.json", "w") as fp:
        json.dump(dict_annonces, fp, indent = 4)