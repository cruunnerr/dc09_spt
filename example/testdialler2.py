# ----------------------------
# Test dialler to show use of dc09_msg class
# (c 2018 van Ovost Automatisering b.v.
# Author : Jacq. van Ovost
# ----------------------------
import sys
from time import sleep
sys.path.append('../')
from dc09_spt import dc09_spt

import logging
logging.basicConfig(format='%(module)-12s %(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger()
#handler = logging.StreamHandler()
#logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

"""
    Copyright (c) 2018  van Ovost Automatisering b.v.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    you may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

def callback(type, data):
    print("Callback type " + type + " data :")
    print(data)

# Code-Tabelle:
# Brand: 110
# Überfall / Notruf: 120
# Einbruch: 130
# Sabotage: 137
# Meldung (Alarm): 140
# Störung / Techn. Alarm: 300
# Scharf: 400
# Unscharf: 140
# Wasser: 154
# Gas: 151
# Pumpe: 206
# Grenzwert: 163
# Routine: 602

routine = 1

key1 = b"\x12\x34\x56\x78\x90\x12\x34\x56\x78\x90\x12\x34\x56\x78\x90\x12"
prom1 = "9999"
ip_ae = "123.123.123.123"
port_ae = "50001"
line = 0 #Lprefix
receiver_ae = 0 # Receiver Nr.
#q = 1 # Ausloesung
#q = 3 # Rueckstellung
#q = 6 # Alte Ausloesung

spt1 = dc09_spt.dc09_spt(prom1)
spt1.set_callback(callback)
# line = LPref = Preäfix
spt1.set_path('main', 'primary', ip_ae, port_ae, account=prom1, key = None, type = 'TCP', line= line)
#spt1.start_poll(890, ok_msg={'code':  'YK'},  fail_msg={'code':  'YS'})
#spt1.send_msg('SIA-DCS', {'code':'RR','text': 'Start of dialler'})
#spt1.start_routine([{'start':  10.10,  'interval':  7200,  'time':  'now', 'type': 'SIA-DCS',  'code':  'RP'},
#    {'interval':  3600,  'type': 'SIA-DCS',  'code':  'RP',  'zone':  99,  'time':  'now'}])
if routine == 1:
    spt1.send_msg('ADM-CID', {'account':  prom1,  'code': 602, 'q': 1, 'zone': 0, 'msg_content':'Testmeldung'})


action = '0'

while action != '9':
    if spt1.isConnected():
        print('SPT1 connected')
    print(spt1.state())
    print ("What do we do ?\n 1 = open,\n 2 = close,\n 3 = burglary alarm,\n 4 = burglary restore,\n 5 = burglary trouble,\n 6 = trouble restore,\n 7 = start poll,\n 8 = stop poll,\n 9 = stop")
    action = input("action : ")
    print(action)
    
    if action == '1':
        spt1.send_msg('ADM-CID', {'account':  prom1,  'code': 140, 'q': 1, 'zone': 2, 'msg_content':'Alarm iobroker'})
        #spt1.send_msg('SIA-DCS', {'area': 2, 'areaname':  'Boven etage hoofdgebouw', 'code':'OP','user': 14,  'username': 'Jantje de Groot',  'text': 'Sectie uitgeschakeld',  'time':  'now'})
    
    if action == '2':
        spt1.send_msg('ADM-CID', {'account':  prom1,  'code': 140, 'q': 3, 'zone': 2, 'msg_content':'Klar iobroker'})
        #spt1.send_msg('SIA-DCS', {'area': 2, 'areaname':  'Boven etage hoofdgebouw', 'code':'CL','user': 14,  'username': 'Jantje de Groot',  'text': 'Sectie ingeschakeld'})  
    
    if action == '3':
        spt1.send_msg('SIA-DCS', {'area': 2, 'time':  'now', 'areaname':  'Boven etage hoofdgebouw', 'code':'BA','zone': 3,  'zonename': 'Entree',  'text': 'Inbraakmelding magneetcontact'})

    if action == '4':
        spt1.send_msg('SIA-DCS', {'area': 2, 'time':  'now', 'areaname':  'Boven etage hoofdgebouw', 'code':'BR','zone': 3,  'zonename': 'Entree',  'text': 'Herstelmelding'})

    if action == '5':
        spt1.send_msg('SIA-DCS', {'area': 2, 'time':  'now', 'areaname':  'Boven etage hoofdgebouw', 'code':'BT','zone': 3,  'zonename': 'Entree',  'text': 'Sabotage magneetcontact'})

    if action == '6':
        spt1.send_msg('SIA-DCS', {'area': 2, 'time':  'now', 'areaname':  'Boven etage hoofdgebouw', 'code':'BJ','zone': 3,  'zonename': 'Entree',  'text': 'Sabotage Herstel'})

    if action == '7':
        spt1.start_poll(85, 890)

    if action == '9' or action == '8':
        spt1.stop_poll()

