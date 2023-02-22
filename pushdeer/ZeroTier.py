# coding:utf-8
import requests
import json

token = 'FSA7dwgCrEc5cb5U7GpHikxc8xp3CifX'
net_work_id = '8bd5124fd6e9f450'
pushkey = 'PDU1TtRhwbxSrMmJ38D4aPOduQdG82WcXOHVa'

get_member_url = 'https://api.zerotier.com/api/v1/network/' + net_work_id + '/member'
push_message = 'http://192.168.192.36:8801/message/push'

headers = {'Content-Type': 'application/json', 'Authorization': 'token ' + token}

response = requests.get(get_member_url, headers=headers)
if response.status_code != 200:
    print('get member error, errorCode: {}'.format(response.status_code))
print(response.content)
load_data = json.loads(response.text)
result = []
for obj in load_data:
    id = obj['id']
    name = obj['name']
    type = obj['type']
    online = obj['online']
    description = obj['description']
    ip = obj['config']['ipAssignments']
    print(id, name, type, online, description, ip)

    result.append({'id': id, 'name': name, 'description': description, 'type': type, 'online': online, 'ip': ip})
print(result)

for member in result:
    markdown = '## ' + member.get('name') + '  ' + '\n- id：' + member.get('id') + '  ' + '\n- type：' + member.get(
        'type') + '  ' + '\n- online：' + str(member.get(
        'online')) + '  ' + '\n- description：' + member.get('description') + '  ' + '\n- ip：' + str(member.get('ip'))
    print(markdown)
    body = {'text': 'zerotier状态', 'desp': markdown, 'pushkey': pushkey}
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    response = requests.post(push_message, data=json.dumps(body), headers=headers)
    load_data = json.loads(response.text)
    print(load_data)
    print(load_data['code'])
