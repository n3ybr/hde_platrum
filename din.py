#!/home/ipm/api/venv/bin/python
import sys 
sys.path.insert(1, '/home/ipm/api/') # Путь до вашей папки со скриптом

import requests
import json
import threading, time
import logging
logging.basicConfig( 
        filename = 'dv.log', 
        level = logging.ERROR, 
        format = '%(levelname)s:%(asctime)s:%(message)s')

#обновление статуса в хде 
def updateHDE(check_id):
    headers = {
            "Authorization": "Basic ",
            'Content-type': 'application/json',

        }
    json_dataHDE={
        'status_id':'closed'
    }
    r = requests.put('https://support.pchelper.ru/api/v2/tickets/{}'.format(int(check_id)), headers=headers,json=json_dataHDE)
    print(r.text + 'zxc')
#комментарий в платрум
def commentPlatrum(json_comment):
    headers = {
        'Content-type': 'application/json',
        "Api-key": ""
    }

    r = requests.post('https://dinvrach.platrum.ru/tasks/api/tasks/comment/save', headers=headers,json=json_comment)
    print(r.status_code)
#комментарий хде
def commentHDE(t_id):
    headers = {
            "Authorization": "Basic ",
            'Content-type': 'application/json',
    }
    json_hdecomm={
        'text':'Заявка из Платрума Династия врачей, для связи используется почта, либо мобильный телефон'
    }
    r = requests.post('https://support.pchelper.ru/api/v2/tickets/{}/comments/'.format(int(t_id)), headers=headers,json=json_hdecomm)
    print(r.status_code)

#обновление статуса в платрум
def updatePlatrum(json_dataUP):
    headers = {
        'Content-type': 'application/json',
        "Api-key": ""
    }

    r = requests.post('https://dinvrach.platrum.ru/tasks/api/task/update', headers=headers,json=json_dataUP)
    print(r.text)
#получение id заявки в хде по id из платрума
def taskById(js_tid,check_id):
    global hde_check
    headers = {
            "Authorization": "Basic ",
            'Content-type': 'application/json',

        }
    r = requests.get('https://support.pchelper.ru/api/v2/tickets', headers=headers,json=js_tid)
    jsonDatah = r.json()
    dataHT = jsonDatah.get('data')
    data_ht = dataHT.get('{}'.format(int((check_id))))
    if data_ht == None:
        hde_check = 0
    else: 
        hde_check = data_ht.get("status_id")
    return hde_check
#получение статуса заявки в платрум
def status_platrum(json_dataTP):
    headers = {
        'Content-type': 'application/json',
        "Api-key": ""
    }

    r = requests.get('https://dinvrach.platrum.ru/tasks/api/task/get', headers=headers,json=json_dataTP)
    jsonDatatp = r.json()
    data_tp = jsonDatatp.get('data')
    return data_tp
#создать заявку в hde
def to_hde(json_datah):
    headers = {
            "Authorization": "Basic ",
            'Content-type': 'application/json',

        }
    r = requests.post('https://support.pchelper.ru/api/v2/tickets', headers=headers,json=json_datah)
    jsonDatah = r.json()
    dataH = jsonDatah.get('data')
    global thde_id
    print(r.text)
    thde_id= dataH.get('id')
    print (thde_id)
    return thde_id
#получить имя телефон почту по id в платрум
def by_id(id):
    headers = {
        'Content-type': 'application/json',
        "Api-key": ""
    }
    r = requests.post('https://dinvrach.platrum.ru/user/api/profile/list/', headers=headers)
    jsonDatap = r.json()
    data=(jsonDatap.get('data'))
    if jsonDatap.get('data') == None:
        return 0
    else:
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
        "Api-key": ""
    }
    json_datap = {
        'responsible_user_ids': ['c41500e5c111a2e2894c8c8384acde5c','c41500e5c111a2e2894c8c8384acde5c'],
        'status_key':['new','in_progress']
    }
    r = requests.get('https://dinvrach.platrum.ru/tasks/api/task/list', headers=headers,json=json_datap)
    jsonDataP = r.json()
    dataP = jsonDataP.get('data')
    return dataP

#поиск контакта по ид в хде
def hde_id(params):
    headers = {
                    "Authorization": "Basic ",
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
                    "Authorization": "Basic ",
                    'Content-type': 'application/json',
                    'Cache-Control': 'no-cache'
                }
    r = requests.get('https://support.pchelper.ru/api/v2/users', headers=headers,params=params)
    jsonData = r.json()
    data_c = jsonData.get('data')
    if len(data_c) == 0:
        headers = {
                "Authorization": "Basic ",
                'Content-type': 'application/json'
        }
        r = requests.post('https://support.pchelper.ru/api/v2/users', headers=headers,json=json_datacall)
        user_hde = hde_id(params)
    else:user_hde = hde_id(params)
    return user_hde

htp=[]
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
thd_id=''
fiel = ['status_key']
while True:
    data4 = new_tasks()

    for i in range(0,len(data4)):
       
        desk = data4[i].get('description')
        if desk == None:
            desk = "1"
        name = data4[i].get('name')
        status = data4[i].get('status_key')
        id = data4[i].get('owner_user_id')

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
        json_datah1['description']=name + str(desk)
        json_datah1['user_email']= emails.get(id)
        json_datah1['user_id']=hde_users(json_datacall,params)

        if str(status) == "new":
            thd_id = to_hde(json_datah=json_datah1)
            commentHDE(t_id=str(thd_id))
            task_id = data4[i].get('id')
            hde =open('hde.txt','a')
            hde.write('{}:{}\n'.format(str(task_id),str(thd_id)))
            hde.close()
            print("отправлено")
            json_dataTP['id']=task_id
            data_tp=status_platrum(json_dataTP)
            id_status = data_tp.get('status_key')
            json_dataP={}
            json_dataP['id']=task_id
            in_p_st = "in_progress"
            ff = {}
            ff['status_key']=in_p_st
            json_dataP['fields']= ff
            updatePlatrum(json_dataUP=json_dataP)
            jsoncomm={
                'task_id': task_id,
                'text': 'Ваше обращение №{} зарегистрировано, если у вас есть вопросы, свяжитесь с нами по номеру 84999638366(WhatsAPP/Telegramm)'.format(str(thd_id)),
            }
            commentPlatrum(json_comment=jsoncomm)
        elif str(status) == "in_progress":

            print("была дин")
            task_id = data4[i].get('id')

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
                if d.get("{}".format(task_id))== None:
                    check_id = 0 
                else:
                    check_id =str(d.get("{}".format(task_id))[0])
            if (d1.get("{}".format(check_id)))== None:
                new_id = 0
            else:new_id = str(d1.get("{}".format(check_id))[0])
            js_tid['id'] = check_id
            hde_check_st = taskById(js_tid,check_id) 
            new_p_st = "finished"
            dff = {}
            dff['status_key']=new_p_st
            json_dataU={}
            json_dataU['id']=new_id
            json_dataU['fields']= dff
            #if status == 'finished' and hde_check_st == "6":
            #    updateHDE(check_id)
            #    print("hde")
            if hde_check_st in("6",'closed'):
                updatePlatrum(json_dataUP=json_dataU)
                print("status")
           # elif status == 'finished' and hde_check_st in ('6', 'open', 'v-processe'):
            #    updateHDE(check_id)
             #   print("hde")
            #else: print('net')
        time.sleep(10.0)

