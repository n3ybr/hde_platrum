#!/home/ipm/api/venv/bin/python
import sys 
sys.path.insert(1, '/home/ipm/api/') # Путь до вашей папки со скриптом

import requests
import json
from threading import Timer

#обновление статуса в хде 
def updateHDE(check_id):
    headers = {
            "Authorization": "Basic ZHBAcGNoZWxwZXIucnU6N2Y5MjQ4OTctZDk3Yy00NGEzLWJhNTItMDJmN2Q0ZTY4YTAw",
            'Content-type': 'application/json',

        }
    json_dataHDE={
        'status_id':'closed'
    }
    r = requests.put('https://support.pchelper.ru/api/v2/tickets/{}'.format(check_id), headers=headers,json=json_dataHDE)
    print(r)

#обновление статуса в платрум
def updatePlatrum(json_dataUP):
    headers = {
        'Content-type': 'application/json',
        "Api-key": "bc98b0a3-cea6-464d-b35e-685f0fb63ed1"
    }

    r = requests.post('https://stomatologia22.platrum.ru/tasks/api/task/update', headers=headers,json=json_dataUP)
    jsonDataUP = r.json()
#получение id заявки в хде по id из платрума
def taskById(js_tid,check_id):
    headers = {
            "Authorization": "Basic ZHBAcGNoZWxwZXIucnU6N2Y5MjQ4OTctZDk3Yy00NGEzLWJhNTItMDJmN2Q0ZTY4YTAw",
            'Content-type': 'application/json',

        }
    r = requests.get('https://support.pchelper.ru/api/v2/tickets', headers=headers,json=js_tid)
    jsonDatah = r.json()
    dataHT = jsonDatah.get('data')
    data_ht = dataHT.get('{}'.format(check_id))
    if data_ht == None:
        hde_check_st = 0
    else: 
        hde_check_st = data_ht.get("status_id")
    return hde_check_st
#получение статуса заявки в платрум
def status_platrum(json_dataTP):
    headers = {
        'Content-type': 'application/json',
        "Api-key": "bc98b0a3-cea6-464d-b35e-685f0fb63ed1"
    }

    r = requests.get('https://stomatologia22.platrum.ru/tasks/api/task/get', headers=headers,json=json_dataTP)
    jsonDatatp = r.json()
    data_tp = jsonDatatp.get('data')
    return data_tp
#создать заявку в hde
def to_hde(json_datah):
    headers = {
            "Authorization": "Basic ZHBAcGNoZWxwZXIucnU6N2Y5MjQ4OTctZDk3Yy00NGEzLWJhNTItMDJmN2Q0ZTY4YTAw",
            'Content-type': 'application/json',

        }
    r = requests.post('https://support.pchelper.ru/api/v2/tickets', headers=headers,json=json_datah)
    jsonDatah = r.json()
    dataH = jsonDatah.get('data')
    global thde_id

    thde_id= dataH.get('id')
    return thde_id
#получить имя телефон почту по id в платрум
def by_id(id):
    headers = {
        'Content-type': 'application/json',
        "Api-key": "bc98b0a3-cea6-464d-b35e-685f0fb63ed1"
    }
    r = requests.post('https://stomatologia22.platrum.ru/user/api/profile/list', headers=headers)
    jsonDatap = r.json()
    data=(jsonDatap.get('data'))
    key_names = []
    key_names = list(data.keys())

    global names
    names={}
    global phones
    phones={}
    global emails
    emails={}
    i=0
    for key in data:
        names[data[str(key_names[i])]['user_id']]=data[str(key_names[i])]['name']
        phones[data[str(key_names[i])]['user_id']]=data[str(key_names[i])]['phone']
        emails[data[str(key_names[i])]['user_id']]=data[str(key_names[i])]['user_email']
        i+=1
    return names,phones,emails

#получить список задач в платрум
def new_tasks():
    headers = {
        'Content-type': 'application/json',
        "Api-key": "bc98b0a3-cea6-464d-b35e-685f0fb63ed1"
    }
    json_datap = {
        'responsible_user_ids': ['c41500e5c111a2e2894c8c8384acde5c','c41500e5c111a2e2894c8c8384acde5c'],
        'status_key':['new','in_progress','finished']
    }
    r = requests.get('https://stomatologia22.platrum.ru/tasks/api/task/list', headers=headers,json=json_datap)
    jsonDataP = r.json()
    dataP = jsonDataP.get('data')
    return dataP

#поиск контакта по ид в хде
def hde_id(params):
    headers = {
                    "Authorization": "Basic ZHBAcGNoZWxwZXIucnU6N2Y5MjQ4OTctZDk3Yy00NGEzLWJhNTItMDJmN2Q0ZTY4YTAw",
                    'Content-type': 'application/json',
                    'Cache-Control': 'no-cache'
                }
    r = requests.get('https://support.pchelper.ru/api/v2/users', headers=headers,params=params)
    jsonData = r.json()
    data_id = jsonData.get('data')
    user_hde_n = data_id[0].get('id')
    return user_hde_n
#проверка контакта на существование(если есть то взять его ид если нет то создать)
def hde_users(json_datacall,params):
    headers = {
                    "Authorization": "Basic ZHBAcGNoZWxwZXIucnU6N2Y5MjQ4OTctZDk3Yy00NGEzLWJhNTItMDJmN2Q0ZTY4YTAw",
                    'Content-type': 'application/json',
                    'Cache-Control': 'no-cache'
                }
    r = requests.get('https://support.pchelper.ru/api/v2/users', headers=headers,params=params)
    jsonData = r.json()
    data_c = jsonData.get('data')
    if len(data_c) == 0:
        headers = {
                "Authorization": "Basic ZHBAcGNoZWxwZXIucnU6N2Y5MjQ4OTctZDk3Yy00NGEzLWJhNTItMDJmN2Q0ZTY4YTAw",
                'Content-type': 'application/json'
        }
        r = requests.post('https://support.pchelper.ru/api/v2/users', headers=headers,json=json_datacall)
        user_hde = hde_id(params)
    else:user_hde = hde_id(params)
    return user_hde

otp=[]
htp=[]
data = new_tasks()
i=0
desk=[]
co = 0
data_tp=[]
params={}
json_datah1={}
json_datacall={}
json_dataTP={}
h_to_p = {}
js_tid = {}
json_dataUP= {}
fiel = ['status_key']
while True:
    for i in range(0,len(data)):
        if data[i].get('description') == None or data[i].get('description') == "" :
            
            desk.append (" ")

        else:desk.append(data[i].get('description'))

        name = data[i].get('name')
        status = data[i].get('status_key')
        task_id = data[i].get('id')
        if data[i].get('id') == None:
            data = 0
        else: 
            id = data[i].get('owner_user_id')

        otp.append(str(task_id))
        id_info = by_id(id)
        owner = names.get(id)

        params['search']=emails.get(id)
        params['exact_search']=0

        dep = []
        dep.append("1")

        json_datacall['name']=owner
        json_datacall['email']=emails.get(id)
        json_datacall['phone']=phones.get(id)
        json_datacall['organiz_id']="71"
        json_datacall['group_id']="1"
        json_datacall['department']=dep
        json_datacall['password']="134234341234"

        json_datah1['title']=name
        json_datah1['description']=name + desk[i]
        json_datah1['user_email']= emails.get(id)
        json_datah1['user_id']=hde_users(json_datacall,params)

        log = open("lg.txt","r")
        old=log.read()
        log.close()
        if str(task_id) not in old:
            if str(status) == "new":
                thde_id = to_hde(json_datah=json_datah1)
                hde =open('hde.txt','a')
                hde.write('{}:{}\n'.format(str(task_id),str(thde_id)))
                hde.close()
                log=open('lg.txt',"a")
                log.write("{}\n".format(str(task_id)))
                log.close()
                print("отправлено")
                json_dataTP['id']=task_id
                data_tp=status_platrum(json_dataTP)
                id_status = data_tp.get('status_key')
        else:
            print("была")
            json_dataTP['id']=task_id
            data_tp=status_platrum(json_dataTP)
            id_status = data_tp.get('status_key')
            d = {}
            with open("hde.txt") as file:
                for line in file:
                    key1, *value1 = line.split(':')
                    d[key1] = value1

            d1 = {}
            with open("hde.txt") as file:
                for line in file:
                    *value, key = line.split(':')
                    d1[key] = value
                if type(d) == "NoneType":
                   check_id = 0 
                else:
                    check_id =(int(d.get("{}".format(task_id))[0]))
            new_id = (int(d1.get("{}\n".format(check_id))[0]))
            js_tid['id'] = check_id
            hde_check_st = taskById(js_tid,check_id) 

            new_p_st = "review"
            dff = {}
            dff['status_key']=new_p_st
            json_dataUP['id']=new_id
            json_dataUP['fields']= dff
            if hde_check_st == "6" and status == "new":
                updatePlatrum(json_dataUP)
                print("status")
            if status == 'finished':
                updateHDE(check_id)
            else: print('net')