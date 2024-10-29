import requests
import shutil
import time
import json
import copy
import os
import re



def main():
    
    check_and_build()
    
    patient_dir = "output/patient"
    for filename in os.listdir(patient_dir):
        file_path = os.path.join(patient_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            patient_data = json.load(file)
            patient_id = patient_data["id"]  
            tf = Patient_put(patient_id, patient_data)
        if tf:
            shutil.move(f"output/Patient/{filename}", f"output/success/Patient/{filename}")

    observation_dir = "output/BC"
    for filename in os.listdir(observation_dir):
        file_path = os.path.join(observation_dir)
        with open(file_path, 'r', encoding='utf-8') as file:
            observation_data = json.load(file)
            tf = Observation_put(observation_data, filename)
        if tf:
            shutil.move(f"output/BC/{filename}", f"output/success/BC/{filename}")


base_url = "https://kcfhir.dicom.tw/fhir"
def Patient_put(id, patient_data):
    time.sleep(0.3)
    # FHIR 伺服器 URL
    url = f'{base_url}/Patient/{id}'

    # 設定 headers，確保使用 JSON 格式
    headers = {
        "Content-Type": "application/fhir+json"
    }

    # 發送 PUT 請求
    response = requests.put(url, headers=headers, data=json.dumps(patient_data))

    # 檢查響應
    try:
        if response.status_code == 201:
            print(f'Patient {patient_data["id"]} updated successfully.')
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            return True
        else:
            print("Failed to update Patient.")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            return False
    except :
        return False

def Observation_put(observation_data):
    time.sleep(0.3)
    
    url = f'{base_url}/Observation/'
    
    headers = {
        "Content-Type": "application/fhir+json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(observation_data))
    try:
        if response.status_code == 201:
            od = copy.deepcopy(observation_data)
            subject_reference = od["subject"]["reference"]
            patient_id = re.search(r"Patient/(.*)", subject_reference).group(1)
            dtime = od["effectiveDateTime"]
            name = od["code"]["coding"][0]["display"].replace(" ", "_")
            total = patient_id + dtime + name
            print(f"Observation {total} updated successfully.")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            return True
        else:
            print("Failed to update Observation.")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            return False
    except :
        return False
        
def check_and_build():
    if not os.path.exists("./output/success"):
        os.makedirs("./output/success")
    if not os.path.exists("./output/success/BC"):
        os.makedirs("./output/success/BC")
    if not os.path.exists("./output/success/Patient"):
        os.makedirs("./output/success/Patient")
main()