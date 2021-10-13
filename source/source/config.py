import getmac
import socket

serverid = "TR" + str(getmac.get_mac_address()).replace(":", "")
ipin = socket.gethostbyname(socket.gethostname())
ipout = socket.gethostbyname(socket.gethostname())

host = "3.36.46.213"
port = 8576
vhost = "/"
mqid = "robot"
mqpw = "robot2021!"

sqlite_host = "/home/robot/robot/db/robot_211008.db"
