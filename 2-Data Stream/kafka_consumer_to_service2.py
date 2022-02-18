import time
import json
import requests
import datetime
import calendar
from datetime import datetime as dt
from confluent_kafka import Consumer,KafkaError

import warnings
warnings.filterwarnings("ignore")

if __name__ != '__main__':
    exit(0)

class KafkaConsumer:
    def __init__(self, topic, broker="172.19.90.104:9092", group="group16"):
        self.broker = broker
        self.group = group
        self.con = Consumer(
            {
                'bootstrap.servers': self.broker,
                'group.id': self.group,
                'auto.offset.reset': 'earliest'
            }
        )
        self.topic = topic
        self.con.subscribe([self.topic])
        print("Kafka Cosumer subscribing to topic ", self.topic)

    def read_messages(self):
        try:
            msg = self.con.poll(5)
            if msg is None:
                return 0
            elif msg.error():
                return 0
            return msg
        except Exception as e:
            print("Exception during reading message :: {}".format(e))
            return 0

con = KafkaConsumer("Iot2")

while True:
    message = con.read_messages()

    if not message:
        print("idle,...")
        continue

    _Dict = json.loads(message.value())
    _Dict['data']['dateHour'] = (datetime.datetime.now()-datetime.timedelta(hours=1)).isoformat()
    _Dict['data']['@timestamp'] =  (datetime.datetime.now()-datetime.timedelta(hours=1)).isoformat() #datetime.datetime.now().isoformat()

    r = requests.post("http://172.19.90.17:6600/search/results", json=_Dict)
    print(_Dict['data']["dateHour"] + " " + _Dict['data']["code"] + " " + str(r.status_code), (_Dict if r.status_code != 200 else "") )

    time.sleep(0.2)





