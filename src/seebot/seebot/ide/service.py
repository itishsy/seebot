from seebot.utils.http import httpUtil
from datetime import datetime
import json

from seebot.ide.storage import Storage
import uuid


class Service:

    def __init__(self, server, token):
        self.server = server
        self.token = token
        self.storage = Storage()

    def find_all_app(self):
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
        res = httpUtil.post(url=url, param=params, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data["data"]['rows']

    def find_flow(self, app_code):
        url = self.server + "/api/robot/flow/list"
        res = httpUtil.post(url=url, param={"appCode": app_code}, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def find_task(self, app_code):
        url = self.server + "/api/robot/app/client/listAllTask?appCode=" + app_code
        res = httpUtil.post(url=url, headers={"Authorization": self.token})
        data = json.loads(res.content)
        return data

    def find_step(self, flow_code):
        url = self.server + "/api/robot/flow/step/list/" + flow_code
        res = httpUtil.post(url=url, headers={"Authorization": self.token})
        data = json.loads(res.content)["data"]
        return data

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

    def sync_flow_steps(self, flow_code):
        url = self.server + "/api/robot/flow/step/save?flowCode=" + flow_code

        data = self.db.find_flow(flow_code)
        flow_steps = json.loads(data[0]['steps'])
        for step in flow_steps:
            del step['actionArgsVOS']
            del step['targetArgsVOS']
        res = httpUtil.post(url=url, param=flow_steps, headers={"Authorization": self.token})
        data = json.loads(res.content)
        if data['data']:
            self.db.update_flow_sync(flow_code)
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
