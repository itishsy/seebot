from seebot.utils.http import httpUtil
from datetime import datetime
import json

import seebot.utils.sqlite as db
import uuid


class Services:

    def __init__(self, server=None):
        if server is not None:
            self.server = server

    def server(self, server):
        self.server = server

    def login(self, username, password):
        url = self.server + "/api/oauth/token?client_id=rpa&client_secret=123&grant_type=password&username=" + username + "&password=" + password
        res = httpUtil.post(url=url)
        data = json.loads(res.content)
        if data.get("access_token") is not None:
            self.token = "Bearer " + data.get('access_token')
            return True
        return data.get("message")

    def find_setting(self, key):
        data = db.query("select value from setting where key='" + key + "'")
        result = []
        if len(data) > 0:
            result = data[0]['value']
        return result

    def upset_setting(self, key, val):
        db.execute("delete from setting where key='"+key+"'")
        db.execute("insert into setting(key, value) values('"+key+"','" + val + "')")

    def find_app(self):
        url = self.server + "/api/robot/app/getAppData"
        params = {
                "page": 1,
                "start": 0,
                "size": 1000,
                "query": [
                    {
                        "property": "keyWord",
                        "value": ""
                    },
                    {
                        "property": "serviceItemList",
                        "value": []
                    },
                    {
                        "property": "businessList",
                        "value": []
                    },
                    {
                        "property": "onlineList",
                        "value": []
                    },
                    {
                        "property": "appStatusList",
                        "value": []
                    }
                ],
                "sidx": "",
                "sort": ""
            }
        res = httpUtil.post(url=url,param=params, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data["data"]['rows']

    def find_flow(self, app_code):
        url = self.server + "/api/robot/flow/list"
        res = httpUtil.post(url=url, param={"appCode":app_code}, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def find_task(self, app_code):
        url = self.server + "/api/robot/app/client/listAllTask?appCode=" + app_code
        res = httpUtil.post(url=url, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def find_step(self, flow_code):
        res = db.query("SELECT steps FROM flow where is_sync=:is_sync and code=:code", {'is_sync': 0, 'code': flow_code})
        local = False
        if len(res) > 0:
            data = json.loads(res[0]['steps'])
            local = True
        else:
            url = self.server + "/api/robot/flow/step/list/" + flow_code
            res = httpUtil.post(url=url, headers={"Authorization": self.token})
            data = json.loads(res.content)["data"]
        return data, local

    def find_action(self):
        url = self.server + "/api/robot/action/all"
        res = httpUtil.post(url=url, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def find_task_args(self, app_code, task_code):
        url = self.server + "/api/robot/task/echoConfig?appCode="+app_code+"&taskCode="+task_code
        res = httpUtil.post(url=url, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def find_target_args(self, data_code):
        url = self.server + "/api/robot/action/target/args?dataCode="+data_code
        res = httpUtil.post(url=url, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def find_action_args(self, data_code):
        url = self.server + "/api/robot/action/args?dataCode="+data_code
        res = httpUtil.post(url=url, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def save_flow_steps(self, flow_code, flow_steps):
        db.execute('delete from flow where code=:code',{'code': flow_code})
        steps = json.dumps(flow_steps, ensure_ascii=False)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute("insert into flow(code, steps, is_sync, updated) values(:code,:steps,:is_sync,:updated)", {'code': flow_code, 'steps': steps, 'is_sync': 0, 'updated': now})
        return True

    def sync_flow_steps(self, flow_code):
        data = db.query("select steps from flow where code = :code", {'code': flow_code} )
        flow_steps = json.loads(data[0]['steps'])
        for step in flow_steps:
            del step['actionArgsVOS']
            del step['targetArgsVOS']
        url = self.server + "/api/robot/flow/step/save?flowCode=" + flow_code
        res = httpUtil.post(url=url, param=flow_steps, headers={"Authorization": self.token})
        data = json.loads(res.content)
        if data['data']:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.query("update flow set is_sync = 1, synced= :synced where code = :code", {'synced': now, 'code': flow_code})
            return True
        return False

    def debug_flow_step(self, flow_code, flow_args, chrome_args):
        # data =  db.query("select steps from flow where code = :code", {'code': flow_code})
        flow_steps = self.find_step(flow_code)[0]
        # flow_steps = json.loads(data[0]['steps'])
        for step in flow_steps:
            del step['actionArgsVOS']
            del step['targetArgsVOS']

        req_data = {'executionCode': str(uuid.uuid4()), 'flowSteps': flow_steps, 'debugStepCodes': [], 'flowArgs': flow_args,'chromeArgs':chrome_args}

        url = "http://127.0.0.1:9090/api/robot/debug/debugFlowStep"
        res = httpUtil.post(url=url, param=req_data, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data
