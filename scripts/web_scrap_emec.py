import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    download_dir = "/opt/simapes/emec_web_scrap/downloads"
    
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "/home/seluser/Downloads",  # Pasta no contêiner
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=chrome_options,
    )

    try:
        logger.info("Step 1: Opening the website...")
        driver.get("https://emec.mec.gov.br/emec/nova")
        logger.info("Website opened successfully.")

        logger.info("Step 2: Clicking the radio button...")
        radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#consulta_avancada_rad_buscar_por[value='CURSO']"))
        )
        radio_button.click()
        logger.info("Radio button clicked successfully.")

        logger.info("Step 3: Entering 'medicina' into the input field...")
        input_field = driver.find_element(By.ID, "txt_no_curso")
        input_field.send_keys("medicina")
        logger.info("Text entered successfully.")

        logger.info("Step 4: Checking the checkbox with value '10065'...")
        presencial_checkbox = driver.find_element(By.XPATH, "//input[@id='consulta_avancada_chk_tp_modalidade_gn' and @value='10065']")
        if not presencial_checkbox.is_selected():
            presencial_checkbox.click()
        logger.info("Checkbox checked successfully.")

        logger.info("Step 5: Clicking the 'Advanced Search' button...")
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnPesqAvancada"))
        )
        search_button.click()
        logger.info("Advanced Search button clicked successfully.")

        logger.info("Step 6: Waiting for the table to load...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "tbDataGridNova"))
        )
        logger.info("Table loaded successfully.")

        logger.info("Step 7: Executing the JavaScript function...")
        driver.execute_script("objTelaConsultaPublicaAvandaca.validarFiltrosExportarDetalhado();")
        logger.info("JavaScript function executed successfully.")

        logger.info("Step 8: Waiting for the loading indicator to appear...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.loading"))
        )
        logger.info("Loading indicator appeared.")

        logger.info("Step 9: Waiting for the loading indicator to disappear...")
        WebDriverWait(driver, 600).until( 
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading"))
        )
        logger.info("Loading indicator disappeared.")

        logger.info("Step 10: Verifying the downloaded file...")
        downloaded_files = os.listdir(download_dir)
        logger.info(f"Downloaded files: {downloaded_files}")
        if downloaded_files:
            for file in downloaded_files:
                if file.endswith('csv'):
                    old_path = os.path.join(download_dir, file)
                    new_path = os.path.join(download_dir, 'emec_medicina.csv')
                    os.rename(old_path, new_path)
                    print(f"Arquivo renomeado para: {new_path}")
                    break

    finally:
        logger.info("Step 11: Closing the browser...")
        driver.quit()
        logger.info("Browser closed successfully.")
