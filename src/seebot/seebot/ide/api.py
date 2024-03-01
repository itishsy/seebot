from seebot.utils.http import httpUtil
import json

server = None
token = None

class Api:
    def server(self, s):
        global server
        server = s

    def login(self, username, password):
        url = server + "/api/oauth/token?client_id=rpa&client_secret=123&grant_type=password&username=" + username + "&password=" + password
        res = httpUtil.post(url=url)
        data = json.loads(res.content)
        global token
        if data.get("access_token") is not None:
            token = "Bearer " + data.get('access_token')
            return True
        return data.get("message")

    def find_app(self):
        url = server + "/api/robot/app/all"
        res = httpUtil.post(url=url, headers={"Authorization": token})
        data = json.loads(res.content)
        return data

    def find_flow(self, app_code):
        url = server + "/api/robot/flow/list"
        res = httpUtil.post(url=url, param={"appCode":app_code}, headers={"Authorization": token})
        data = json.loads(res.content)
        return data

    def find_task(self, app_code):
        url = server + "/api/robot/app/client/listAllTask?appCode=" + app_code
        res = httpUtil.post(url=url, headers={"Authorization": token})
        data = json.loads(res.content)
        return data

    def find_step(self, flow_code):
        url = server + "/api/robot/flow/step/list/" + flow_code
        res = httpUtil.post(url=url, headers={"Authorization": token})
        data = json.loads(res.content)
        return data

    def find_action(self):
        url = server + "/api/robot/action/all"
        res = httpUtil.post(url=url, headers={"Authorization": token})
        data = json.loads(res.content)
        return data

    def find_task_args(self, app_code, task_code):
        url = server + "/api/robot/task/echoConfig?appCode="+app_code+"&taskCode="+task_code
        res = httpUtil.post(url=url, headers={"Authorization": token})
        data = json.loads(res.content)
        return data

    def find_target_args(self, data_code):
        url = server + "/api/robot/action/target/args?dataCode="+data_code
        res = httpUtil.post(url=url, headers={"Authorization": token})
        data = json.loads(res.content)
        return data

    def find_action_args(self, data_code):
        url = server + "/api/robot/action/args?dataCode="+data_code
        res = httpUtil.post(url=url, headers={"Authorization": token})
        data = json.loads(res.content)
        return data
