from names_dataset import NameDataset
import random
import hashlib
import uuid
import json
import copy
import os
import re

always_check_hash2uuid = True
enable_meta_data = True

def main():
    H2U,U2PN = check_and_build()
    with open("./setting/ex.json", 'r', encoding='utf8') as jfile:
        ex = json.load(jfile)
    files = os.listdir('./input/')
    for file_name in files:
        if file_name.endswith('.json'):
            with open(os.path.join('./input/', file_name), 'r', encoding='utf8') as jfile:
                BC = json.load(jfile)
                
            if not isinstance(BC, list):
                print(f"錯誤：{file_name} 中的資料不是陣列，跳過該檔案")
                continue
            
            for body in BC:
                
                if body.get("main_type") != "Physiology":
                    print(f"資料格式錯誤，main_type 並非 Physiology，跳過該資料：{body}")
                    continue
                
                if body["user_id_hash"] not in H2U or always_check_hash2uuid:
                    generated_uuid = str(hash2uuid(H2U,body["user_id_hash"]))
                    print(f'add user:{body["user_id_hash"]}')
                    Patient = copy.deepcopy(ex["Patient"])
                    Patient["identifier"][0]["value"] = generated_uuid
                    Patient["id"] = generated_uuid
                    Patient["name"][0]["text"] = name_create()
                    uuid2patient_name(U2PN,generated_uuid,Patient["name"][0]["text"])
                    if body["gender"] == "女":
                        Patient["gender"] = "female"
                    elif body["gender"] == "男":
                        Patient["gender"] = "male"
                    elif body["gender"] != "":
                        Patient["gender"] = "other"
                    else:
                        Patient["gender"] = "unknown"
                    match = re.search(r'\[(.+?)-(.+?)\]', body["birth_year"])
                    year = (match.group(1) + "0" * (4 - len(match.group(1))))[:4]
                    # month = str(random.randint(1, 12)).zfill(2)
                    # day = str(random.randint(1, 28)).zfill(2)
                    Patient["birthDate"] = f"{year}-01-01"
                    with open(f"./output/Patient/{generated_uuid}.json", 'w', encoding='utf8') as jfile:
                        json.dump(Patient, jfile, ensure_ascii=False)
                else:
                    generated_uuid = H2U[body["user_id_hash"]]["uuid"]
                
                time = body["start_date"].replace(" ", "T").replace(":", "-").replace("/", "-")
                if body["height"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["height"]["code"]
                        N_BC["valueQuantity"] = ex["height"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["height"])
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["height"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_height.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)
                        print(f'add BodyComposition:{generated_uuid}_height')
                    except:
                        pass
                if body["weight"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["weight"]["code"]
                        N_BC["valueQuantity"] = ex["weight"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["weight"])     
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["weight"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_weight.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False) 
                        print(f'add BodyComposition:{generated_uuid}_weight')
                    except:
                        pass
                if body["waist_circumference"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["waist"]["code"]
                        N_BC["valueQuantity"] = ex["waist"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["waist_circumference"])
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["waist"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_waist.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)   
                        print(f'add BodyComposition:{generated_uuid}_waist') 
                    except:
                        pass    
                if body["systolic_blood_pressure"] and body["diastolic_blood_pressure"]:   
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["bloodpressure"]["code"]
                        N_BC["component"] = ex["bloodpressure"]["component"]
                        N_BC["component"][0]["valueQuantity"]["value"] = float(body["systolic_blood_pressure"])        
                        N_BC["component"][1]["valueQuantity"]["value"] = float(body["diastolic_blood_pressure"])
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["bloodpressure"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_bloodpressure.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)   
                        print(f'add BodyComposition:{generated_uuid}_bloodpressure') 
                    except:
                        pass 
                if body["peripheral_oxyhemoglobin_saturation"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["SpO2"]["code"]
                        N_BC["valueQuantity"] = ex["SpO2"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["peripheral_oxyhemoglobin_saturation"])
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["SpO2"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_SpO2.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)    
                        print(f'add BodyComposition:{generated_uuid}_SpO2')    
                    except:
                        pass
                if body["blood_sugar"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["glucose"]["code"]
                        N_BC["valueQuantity"] = ex["glucose"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["blood_sugar"])
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["glucose"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_glucose.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)     
                        print(f'add BodyComposition:{generated_uuid}_glucose') 
                    except:
                        pass  
                if body["heart_rate"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["heartrate"]["code"]
                        N_BC["valueQuantity"] = ex["heartrate"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["heart_rate"])     
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["heartrate"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_heartrate.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)
                        print(f'add BodyComposition:{generated_uuid}_heartrate')
                    except:
                        pass
                if body["resting_heart_rate"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["restingheartrate"]["code"]
                        N_BC["valueQuantity"] = ex["restingheartrate"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["resting_heart_rate"])    
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"  
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["restingheartrate"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_restingheartrate.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False) 
                        print(f'add BodyComposition:{generated_uuid}_restingheartrate')
                    except:
                        pass
                if body["average_heart_rate"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["meanheartrate"]["code"]
                        N_BC["valueQuantity"] = ex["meanheartrate"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["average_heart_rate"])    
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"  
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["meanheartrate"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_meanheartrate.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False) 
                        print(f'add BodyComposition:{generated_uuid}_meanheartrate')
                    except:
                        pass
                if body["heart_rate_variability"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["heartratevariability"]["code"]
                        N_BC["valueQuantity"] = ex["heartratevariability"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["heart_rate_variability"])       
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["heartratevariability"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_heartratevariability.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)
                        print(f'add BodyComposition:{generated_uuid}_heartratevariability')
                    except:
                        pass
                if body["temperature"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["temperature"]["code"]
                        N_BC["valueQuantity"] = ex["temperature"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["temperature"])        
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["temperature"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_temperature.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)
                        print(f'add BodyComposition:{generated_uuid}_temperature')
                    except:
                        pass
                if body["respiratory_rate"]:
                    try:
                        N_BC = copy.deepcopy(ex["common"])
                        N_BC["code"] = ex["respiratoryrate"]["code"]
                        N_BC["valueQuantity"] = ex["respiratoryrate"]["valueQuantity"]
                        N_BC["valueQuantity"]["value"] = float(body["respiratory_rate"])
                        N_BC["effectiveDateTime"] = body["start_date"].replace(" ", "T").replace("/", "-") + "Z"
                        N_BC["subject"]["reference"] = f"Patient/{generated_uuid}"
                        N_BC["meta"] = ex["respiratoryrate"]["meta"]
                        with open(f'./output/BC/{generated_uuid}_{time}_respiratoryrate.json', 'w', encoding='utf8') as jfile:
                            json.dump(N_BC, jfile, ensure_ascii=False)
                        print(f'add BodyComposition:{generated_uuid}_respiratoryrate')
                    except:
                        pass

def check_and_build():
    if not os.path.exists("./input"):
        os.makedirs("./input")
    if not os.path.exists("./output"):
        os.makedirs("./output")
    if not os.path.exists("./output/Patient"):
        os.makedirs("./output/Patient")
    if not os.path.exists("./output/BC"):
        os.makedirs("./output/BC")
    if not os.path.exists("./setting"):
        os.makedirs("./setting")
    if not os.path.exists("./setting/ex.json"):
        ex = {"Patient":{"resourceType":"Patient","id":"","identifier":[{"type":{"coding":[{"system":"http://terminology.hl7.org/CodeSystem/v2-0203","code":"NNxxx"}]},"system":"http://www.moi.gov.tw","value":"A123456789"}],"name":[{"use":"anonymous","text":"連小妹"}],"gender":"female","birthDate":"1990-01-01"},"common":{"resourceType":"Observation","status":"final","category":[{"coding":[{"system":"http://terminology.hl7.org/CodeSystem/observation-category","code":"vital-signs","display":"Vital Signs"}]}],"subject":{"reference":"Patient/patient-ex-example"},"effectiveDateTime":""},"height":{"code":{"coding":[{"system":"http://loinc.org","code":"8302-2","display":"Body height"}],"text":"Body height"},"valueQuantity":{"value":160,"unit":"cm","system":"http://unitsofmeasure.org","code":"cm"}},"weight":{"code":{"coding":[{"system":"http://loinc.org","code":"29463-7","display":"Body weight"}],"text":"Body weight"},"valueQuantity":{"value":50,"unit":"kg","system":"http://unitsofmeasure.org","code":"kg"}},"waist":{"code":{"coding":[{"system":"http://loinc.org","code":"8280-0","display":"Waist Circumference at umbilicus by Tape measure"}],"text":"Waist Circumference at umbilicus by Tape measure"},"valueQuantity":{"value":63,"unit":"cm","system":"http://unitsofmeasure.org","code":"cm"}},"bloodpressure":{"code":{"coding":[{"system":"http://loinc.org","code":"85354-9","display":"Blood pressure panel with all children optional"}],"text":"Blood pressure panel with all children optional"},"component":[{"code":{"coding":[{"system":"http://loinc.org","code":"8480-6","display":"Systolic blood pressure"}]},"valueQuantity":{"value":110,"unit":"mmHg","system":"http://unitsofmeasure.org","code":"mm[Hg]"}},{"code":{"coding":[{"system":"http://loinc.org","code":"8462-4","display":"Diastolic blood pressure"}]},"valueQuantity":{"value":56,"unit":"mmHg","system":"http://unitsofmeasure.org","code":"mm[Hg]"}}]},"SpO2":{"code":{"coding":[{"system":"http://loinc.org","code":"2708-6","display":"Oxygen saturation in Arterial blood"}],"text":"Oxygen saturation in Arterial blood"},"valueQuantity":{"value":98,"unit":"%","system":"http://unitsofmeasure.org","code":"%"}},"glucose":{"code":{"coding":[{"system":"http://loinc.org","code":"2339-0","display":"Glucose [Mass/volume] in blood"}],"text":"Glucose [Mass/volume] in blood"},"valueQuantity":{"value":80,"unit":"mg/dl","system":"http://unitsofmeasure.org","code":"mg/dl"}},"heartrate":{"code":{"coding":[{"system":"http://loinc.org","code":"8867-4","display":"Heart rate"}],"text":"Heart rate"},"valueQuantity":{"value":80,"unit":"/min","system":"http://unitsofmeasure.org","code":"/min"}},"restingheartrate":{"code":{"coding":[{"system":"http://loinc.org","code":"40443-4","display":"Heart rate --resting"}],"text":"Heart rate --resting"},"valueQuantity":{"value":50,"unit":"/min","system":"http://unitsofmeasure.org","code":"/min"}},"meanheartrate":{"code":{"coding":[{"system":"http://loinc.org","code":"103205-1","display":"Mean heart rate"}],"text":"Mean heart rate"},"valueQuantity":{"value":75,"unit":"/min","system":"http://unitsofmeasure.org","code":"/min"}},"heartratevariability":{"code":{"coding":[{"system":"http://loinc.org","code":"80404-7","display":"R-R interval.standard deviation (Heart rate variability)"}],"text":"R-R interval.standard deviation (Heart rate variability)"},"valueQuantity":{"value":50,"unit":"ms","system":"http://unitsofmeasure.org","code":"ms"}},"temperature":{"code":{"coding":[{"system":"http://loinc.org","code":"8310-5","display":"Body temperature"}],"text":"Body temperature"},"valueQuantity":{"value":36.5,"unit":"C","system":"http://unitsofmeasure.org","code":"Cel"}},"respiratoryrate":{"code":{"coding":[{"system":"http://loinc.org","code":"9279-1","display":"Respiratory rate"}],"text":"Respiratory rate"},"valueQuantity":{"value":15,"unit":"min","system":"http://unitsofmeasure.org","code":"/min"}}}
        if enable_meta_data:
            ex["Patient"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/TWCorePatient"]}
            ex["height"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/Height-sport"]}
            ex["weight"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/Weight-sport"]}
            ex["waist"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/Waist-sport"]}
            ex["bloodpressure"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/BloodPressure-sport"]}
            ex["SpO2"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/SpO2-sport"]}
            ex["glucose"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/Glucose-sport"]}
            ex["heartrate"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/HeartRate-sport"]}
            ex["restingheartrate"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/RestingHeartRate-sport"]}
            ex["meanheartrate"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/MeanHeartRate-sport"]}
            ex["heartratevariability"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/HRV-sport"]}
            ex["temperature"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/BodyTemperature-sport"]}
            ex["respiratoryrate"]["meta"] = {"profile":["https://hapi.fhir.tw/fhir/StructureDefinition/RespiratoryRate-sport"]}
        with open("./setting/ex.json", 'w', encoding='utf8') as jfile:
            json.dump(ex, jfile)
            
    if not os.path.exists("./setting/hash2uuid.json"):
        with open("./setting/hash2uuid.json", 'w', encoding='utf8') as jfile:
            json.dump({}, jfile)
            H2U = {}
    else:
        with open("./setting/hash2uuid.json", 'r', encoding='utf8') as jfile:
            H2U = json.load(jfile)
            
    if not os.path.exists("./setting/uuid2patient_name.json"):
        with open("./setting/uuid2patient_name.json", 'w', encoding='utf8') as jfile:
            json.dump({}, jfile)
            U2PN = {}
    else:
        with open("./setting/uuid2patient_name.json", 'r', encoding='utf8') as jfile:
            U2PN = json.load(jfile)
    return H2U,U2PN

def hash2uuid(H2U,original_hash:str):
    sha1_hash = hashlib.sha1(original_hash.encode()).hexdigest()
    selected_part = sha1_hash[:32]
    generated_uuid = uuid.UUID(selected_part)
    H2U[original_hash] = {"sha1_hash":sha1_hash,"uuid":str(generated_uuid)}
    with open('./setting/hash2uuid.json','w',encoding='utf8') as jfile:
        json.dump(H2U,jfile, ensure_ascii=False,indent=4)
    return generated_uuid

def uuid2patient_name(U2PN,uuid:str,name:str):
    U2PN[uuid] = name
    with open('./setting/uuid2patient_name.json','w',encoding='utf8') as jfile:
        json.dump(U2PN,jfile, ensure_ascii=False,indent=4)
def name_create():
    surnames = ['王', '李', '張', '劉', '陳', '楊', '趙', '黃', '周', '吳']
    first_names = ['偉', '芳', '娜', '敏', '靜', '麗', '強', '磊', '軍', '洋', '勇', '艷', '傑', '浩', '鑫']
    surname = random.choice(surnames)
    first_name = ''.join(random.choice(first_names) for _ in range(2))
    # total_name = "連大刀"
    # return total_name
    return surname + first_name
    
main()