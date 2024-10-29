import requests
import time
import json
import os
import re



def main():
        # 遍歷 output/patient 資料夾中的每個檔案並上傳
    patient_dir = "output/patient"
    for filename in os.listdir(patient_dir):
        file_path = os.path.join(patient_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            patient_data = json.load(file)
            patient_id = patient_data["id"]  # 假設檔案名稱是患者 ID
            Patient_put(patient_id, patient_data)

    # 遍歷 output/BC 資料夾中的每個檔案並上傳
    observation_dir = "output/BC"
    for filename in os.listdir(observation_dir):
        file_path = os.path.join(observation_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            observation_data = json.load(file)
            Observation_put(observation_data)



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
        else:
            print("Failed to update Patient.")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
    except :
        pass

def Observation_put(observation_data):
    time.sleep(0.3)
    
    url = f'{base_url}/Observation/'
    
    headers = {
        "Content-Type": "application/fhir+json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(observation_data))


    if response.status_code == 201:
        subject_reference = observation_data["subject"]["reference"]
        patient_id = re.search(r"Patient/(.*)", subject_reference).group(1)
        time = observation_data["effectiveDateTime"]
        name = observation_data["code"]["coding"][0]["display"].replace(" ", "_")
        total = patient_id + time + name
        print(f"Observation {total} updated successfully.")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    else:
        print("Failed to update Observation.")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        
main()