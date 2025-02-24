from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
import re

def navigator_initializer():
    return webdriver.Firefox()

def search_ART(browser, art_number):
    browser.get('https://servicos.crea-rs.org.br/ServicosPrd/servlet/com.servicos.srv.wbpsrvartres')

    try:
        searchbox = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[title="Informe o número da ART"]'))
        )
        searchbox.send_keys(str(art_number))
        update_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img[title="Atualizar"]'))
        )
        update_button.click()

        try:
            time.sleep(2)
            warning_message = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span//div[@class="gx-warning-message"]'))
            ).text
            if warning_message == 'Não localizamos este número de ART no banco de dados.' or warning_message == 'ART ainda não registrada no Crea-RS. Só estão disponíveis para consulta as ARTs registradas.':
                print('ART not found')
                return False
            else:
                return True
        except:
            return True
    except:
        print('Error finding searchbox')
        return False

def collect_data(browser):
    try:
        art = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_NRO2"]'))
        )
        art_text = art.text

        situation = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_DSCSTC"]'))
        )
        situation_text = situation.text

        art_sub = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARNBXA_ARTTRANSF"]'))
        )
        art_sub_text = art_sub.text

        professional = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_NMEPRF"]'))
        )
        professional_text = professional.text

        crea = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_CODCRTPRF"]'))
        )
        crea_text = crea.text

        executing_company = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vART_NMEEMP"]'))
        )
        executing_company_text = executing_company.text

        art_type = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_DSCTPO"]'))
        )
        art_type_text = art_type.text

        reason = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_DSCMOT"]'))
        )
        reason_text = reason.text

        tecnical_participation = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_DSCPARTEC"]'))
        )
        tecnical_participation_text = tecnical_participation.text

        contractor = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_NMECTN"]'))
        )
        contractor_text = contractor.text

        owner = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_NMEPRP"]'))
        )
        owner_text = owner.text

        address = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vENDERECO"]'))
        )
        address_text = address.text

        city_state = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_NMEMUN1"]'))
        )
        city_state_text = city_state.text

        start_date = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_DTAINIOBR"]'))
        )
        start_date_text = start_date.text

        art_payment_date = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_DTAPGT"]'))
        )
        art_payment_date_text = art_payment_date.text

        discharge_date = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="row"]//span[@id="span_vARN_DTABAI"]'))
        )
        discharge_date_text = discharge_date.text

        return {
            'ART': art_text,
            'Situation': situation_text,
            'ART Sub': art_sub_text,
            'Professional': professional_text,
            'CREA': crea_text,
            'Executing Company': executing_company_text,
            'ART Type': art_type_text,
            'Reason': reason_text,
            'Tecnical Participation': tecnical_participation_text,
            'Contractor': contractor_text,
            'Owner': owner_text,
            'Address': address_text,
            'City/State': city_state_text,
            'Start Date': start_date_text,
            'Payment Date': art_payment_date_text,
            'Discharge Date': discharge_date_text,
            }
    except:
        print('Error finding ART data')

def collect_titles(browser):
    try:
        titles = []
        titles_webelements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@id="TituloContainerTbl"]/tbody/tr/td[@data-colindex="1"]//span'))
        )
        for title in titles_webelements:
            titles.append(title.text)
        
        return titles

    except:
        print('Error finding titles')

def collect_activities(browser):
    try:
        activities = []
        activities_webelements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@id="ArnContainerTbl"]/tbody/tr/td//span'))
        )
        for i in range(0, len(activities_webelements), 6):
            tec_activity = activities_webelements[i].text
            spec_activity = activities_webelements[i+1].text
            item = activities_webelements[i+2].text
            quantity = activities_webelements[i+3].text
            unit = activities_webelements[i+5].text
            activity = {
                'Technical Activity': tec_activity,
                'Specifical Activity': spec_activity,
                'Item Description': item,
                'Quantity': quantity,
                'Unit': unit,
                }
            activities.append(activity)
            
        return activities
    
    except:
        print('Error finding activities')

def save_art_info(art_info, output_json_file):
    existing_data = []
    if os.path.exists(output_json_file) and os.path.getsize(output_json_file) > 0:
        with open(output_json_file, "r", encoding="utf-8") as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    if isinstance(art_info, list):
        existing_data.extend(art_info)
    else:
        existing_data.append(art_info)

    with open(output_json_file, "w", encoding="utf-8") as json_file:
        json.dump(existing_data, json_file, indent=4, ensure_ascii=False)

def start_by_last_art(output_json_file):
    if os.path.exists(output_json_file) and os.path.getsize(output_json_file) > 0:
        with open(output_json_file, "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                last_art = data[-1]['Data']['ART']
                last_art_number = int(re.search(r'\d+', last_art).group())
                return last_art_number + 1
            except json.JSONDecodeError:
                return 13406010
    else:
        return 13406010

def main():
    output_json_file = 'art_info.json'
    browser = navigator_initializer()
    art_number = start_by_last_art(output_json_file)
    count = 0
    while True:
        if search_ART(browser, art_number):
            start_time = time.time()
            time.sleep(2)
            data = collect_data(browser)
            titles = collect_titles(browser)
            activities = collect_activities(browser)
            art_info = {
                'Data': data,
                'Titles': titles,
                'Activities': activities
            }
            save_art_info(art_info, output_json_file)
            end_time = time.time()
            print(f'ART {art_number} collected in {end_time - start_time} seconds')
            print(count)
        else:
            art_info = {
                'Data': {
                    'ART': str(art_number),
                    'Situation': 'ART not found'
                },
            }
            save_art_info(art_info, output_json_file)
            
        art_number = art_number + 1
        count = count + 1

if __name__ == "__main__":
    main()
