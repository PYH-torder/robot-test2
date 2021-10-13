import config
import setdb
import time
import setmq
import sys

queue2 = "robot_main2"
cut_time = 60 * 5
now_ordercode = ""
now_count = 0
now_step = 1
run_time = 0
now_robot_step1 = ""
now_robot_step2 = ""
now_robot_step3 = ""


def selectRobot(rtype, rcorp):
    devices = setdb.getDevice()
    for device in devices:
        # print(str(device[10]) + " / " + device[6])
        if(device[10] == rtype and (rcorp == device[1] or rcorp == "")): # 1: 로봇팔 / 2: 서빙로봇
            if(device[6] == "Ready" or device[6] == "Home" or device[6] == "none"): #준비상태
                return device[3]
                break
    return ""

def getRobotStatus(deviceid):
    devices = setdb.getDevice()

    rtnvalue = {
        "status" : "",
        "pstatus" : "",
        "stype" : "",
        "id" : "",
        "appkey" : ""
    }

    for device in devices:
        if(deviceid == device[3]):
            rtnvalue["status"] = device[6]
            rtnvalue["pstatus"] = device[2]
            rtnvalue["stype"] = device[1]
            rtnvalue["id"] = device[3]
            rtnvalue["appkey"] = device[4]
            break
    
    return rtnvalue

def setStatus(ocode, step1, step2, step3, step4, status, now_count):
    setdb.setChangeOrder(ocode, step1, step2, step3, step4, status, now_count)
    setmq.send(queue2, {
        "tp" : "orderstatus",
        "id" : config.serverid,
        "ocode" : ocode,
        "step1" : step1,
        "step2" : step2,
        "step3" : step3,
        "step4" : step4,
        "status" : status,
        "nqty" : now_count
    })

while True:

    rows = setdb.getOrderOne()

    for row in rows:

        seq = row[0]
        otype = row[1]
        ocode = row[2]
        oname = row[3]
        omenu = row[4]
        step1 = row[5]
        step2 = row[6]
        step3 = row[7]
        step4 = row[8]
        status = row[9]
        oqty = row[12]
        otable = row[14]
        ice = 0
        ade = 0
        camera = 0

        if(omenu == "9"):
            omenu = "coffeeice"
            ice = 1

        if(omenu == "coffeeice" or omenu == "ade1" or omenu == "ade2" or omenu == "ade3" or omenu == "ade4" or omenu == "ade5" or omenu == "spacle"):
            ice = 1
        
        if(omenu == "ade1" or omenu == "ade2" or omenu == "ade3" or omenu == "ade4" or omenu == "ade5" or omenu == "spacle"):
            ade = 1

        if(ocode != now_ordercode):
            now_ordercode = ocode
            now_count = 0
            run_time = 0
            now_step = 1
            now_robot_step1 = ""
            now_robot_step2 = ""
            now_robot_step3 = ""

        print(row, flush = True)

    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'sleep', flush=True)
    time.sleep(1)      #1초단위로 실행