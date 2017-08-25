# cmc

import cbapi
import sys
import time
import schedule
import sqlite3

from cbapi.response import *
from twilio.rest import Client
cb = CbEnterpriseResponseAPI()

""" twilio config """
account_sid = open('twilio_sid','r').read().strip()
auth_token = open('twilio_secret','r').read().strip()
twilio_client = Client(account_sid, auth_token)

def sensor_online(sid):
    print("checking if {} is online..".format(sid))
    sensor = cb.select(Sensor, sid)
    sensor.refresh()
    if sensor.status == 'Online':
        print("{} is online!".format(sid))
        return True 
    print("{} is NOT online!".format(sid))
    return False

def send_sms(recipient, message):
    print("sending message: {}, to {}..".format(message, recipient))
    message = \
        twilio_client.api.account.messages.create(
            to=recipient,
            from_="+116692717592", #this is my twilio number, there are many like it, but this one is mine
            body=message
        )

def monitor():
    conn = sqlite3.connect('db/targets.db')
    c = conn.cursor()
    c.execute("select cb_sid, cb_hostname,requestor_cellno,requestor_slack_name,last_notified from targets")
    targets = c.fetchall()
    for t in targets:
        sid = t[0]
        cellno = t[2]
        hostname = t[1]
        if sensor_online(sid):
            msg = "Target online: {} ({})".format(sid, hostname) 
            send_sms(cellno, msg)


def main():
    schedule.every(15).minutes.do(monitor)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

