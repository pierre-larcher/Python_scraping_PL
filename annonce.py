from selenium.webdriver.common.by import By 


class Annonce:
    """
    """
    def __init__(self, driver): 
        self.annonce = {}
        self.driver = driver
       
             
    def __repr__(self):
        return f"""
            localisation    : {self.localisation}
            prix            : {self.prix}
            pieces          : {self.pieces}
            surface         : {self.surface}
            DPE             : {self.DPE}
            DPE_Effet_serre : {self.DPE_ES}
            depenses_energie: {self.depenses_energ}
            """

    def recuperation(self):
        """Recupère les données d'une annonce"""
        
        self.annonce["localisation"] = self.driver.find_element(By.ID, 'detail_loc').text
        self.annonce["prix"] = self.driver.find_element(By.ID, 'autoprix').text
        self.annonce["pieces"] = self.driver.find_element(By.CLASS_NAME, 'nbp').text
        self.annonce["surface"] = self.driver.find_element(By.CLASS_NAME, 'surf').text
        self.annonce["DPE"] = self.driver.find_element(By.CLASS_NAME, 'DPE_consEnerTxt').text
        self.annonce["DPE_ES"] = self.driver.find_element(By.CLASS_NAME, 'DPE_effSerreTxt').text
        self.annonce["depenses_energ"] = self.driver.find_element(By.CLASS_NAME, 'fin').text
        return self.annonce
    
        