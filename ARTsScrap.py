from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import re
import csv
import time

def navigator_initializer():
    browser = Service('/usr/lib/chromium-browser/chromedriver')
    return webdriver.Chrome(service=browser)

def search_ARTs(browser, art_number, current_app, art_start):
    while art_number < art_start + 100000:
        if search_ART(browser, art_number):
            data = collect_data(browser)
            if data.get('ART') == "":
                data = collect_data(browser)
            titles = collect_titles(browser)
            activities = collect_activities(browser)
            if data == None or titles == None or activities == None:
                break
            save_art(data, titles, activities, art_number, True, current_app)
        else:
            save_art(None, None, None, art_number, False, current_app)
        art_number += 1

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
            warning_message = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span//div[@class="gx-warning-message"]'))
            ).text
            if warning_message == 'Não localizamos este número de ART no banco de dados.' or warning_message == 'ART ainda não registrada no Crea-RS. Só estão disponíveis para consulta as ARTs registradas.':
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
        return None

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
        return None

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
                'Unit': unit
                }
            activities.append(activity)
        return activities
    except:
        print(activity)
        print('Error finding activities')
        return None

def save_art(data, titles, activities, art_number, found, current_app):
    if found:
        art = {
            'Data': data,
            'Titles': titles,
            'Activities': activities,
        }
    else:
        art = {
            'Data': {
                'ART': str(art_number),
                'Situation': 'ART not found'
            },
        }
    save_art_info(art, current_app)

def save_art_info(art, current_app):
    current_archive = get_latest_archive(current_app)
    if os.path.exists(current_archive) and os.path.getsize(current_archive) > 0:
        with open(current_archive, "r+", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                if len(data) == 2500:
                    current_number = get_latest_archive_number(current_app) + 1
                    current_archive = f'data/json{current_app}/art_info_{current_number}.json'
                    with open(current_archive, "w", encoding="utf-8") as json_file:
                        json.dump([art], json_file)
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(art)
    with open(current_archive, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def start_by_last_art(current_archive):
    if os.path.exists(current_archive) and os.path.getsize(current_archive) > 0:
        with open(current_archive, "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                if len(data) == 0:
                    return 12800000
                last_art = data[-1]['Data']['ART']
                last_art_number = int(re.search(r'\d+', last_art).group())
                return last_art_number + 1
            except json.JSONDecodeError:
                return 12800000
    else:
        return 12800000

def get_latest_archive(current_app):
    try:
        files = os.listdir(f'data/json{current_app}')
        if not files:
            new_file = (f'data/json{current_app}/art_info_1.json')
            with open(new_file, "w", encoding="utf-8") as json_file:
                json.dump([], json_file)
            return str(new_file)
        json_files = [f for f in files if f.startswith('art_info_') and f.endswith('.json')]
        if not json_files:
            return None
        json_files.sort(key=lambda f: int(re.search(r'\d+', f).group()), reverse=True)
        return str(f"data/json{current_app}/" + json_files[0])
    except:
        return None
    
def get_latest_archive_number(current_app):
    try:
        files = os.listdir(f'data/json{current_app}')
        if not files:
            return 1
        json_files = [f for f in files if f.startswith('art_info_') and f.endswith('.json')]
        if not json_files:
            return 1
        json_files.sort(key=lambda f: int(re.search(r'\d+', f).group()), reverse=True)
        return int(re.search(r'\d+', json_files[0]).group())
    except:
        return 1

def save_data_to_csv(arts):
    output = 'data/csv/arts_address.csv'
    existing_data = []
    if os.path.exists(output) and os.path.getsize(output) > 0:
        with open(output, "r", encoding="utf-8", newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            existing_data = list(reader)
    
    if isinstance(arts, list):
        existing_data.extend(arts)
    else:
        existing_data.append(arts)
    
    with open(output, "w", encoding="utf-8", newline='') as csv_file:
        if existing_data:
            fieldnames = existing_data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_data)

def start_scrap(art_start, current_app):
    start_time = time.time()
    browser = navigator_initializer()
    current_archive = get_latest_archive(current_app)
    art = start_by_last_art(current_archive)
    if art < art_start:
        art = art_start
    search_ARTs(browser, art, current_app, art_start)
    browser.quit()
    print(f"Time elapsed: {time.time() - start_time}")
