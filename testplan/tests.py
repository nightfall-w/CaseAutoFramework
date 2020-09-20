import requests
import json

headers = {
    "Content-Type": "application/json",
    "charset": "utf-8",
    "Referer": "{}/web/rcs/rcs/simulationAdd".format(),
}
login_url = "{}/evo/login".format("http://deploy-1592815424.flashhold.com")
login_data = {"userName": "admin", "password": "admin"}
session = requests.session()
response = session.post(url=login_url, headers=headers, data=json.dumps(login_data))
print(" [+]%s" % response.text)
agv_add_url = "{}/evo/api/rcsSimulation/simulationAdd/form/newOperate/form".format(
    "http://deploy-1592815424.flashhold.com")
data = {"0agvType": "M100A(S)", "0agvSum": "{}".format(60), "0speed": "1.5", "0initPower": "1",
        "0simuBootPosition": True}
response = session.post(url=agv_add_url, headers=headers, data=json.dumps(data))
print(" [+]%s" % response.text)
# time.sleep(3)
# restart_service(environ, 'evo-agv-simulation-carrier')
