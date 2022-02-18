import json
from flask import Flask, render_template, request, jsonify
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer

app = Flask(__name__)

# Parse the command line.
parser = ArgumentParser()
parser.add_argument('config_file', type=FileType('r'))
args = parser.parse_args()

# Parse the configuration.
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

config_parser = ConfigParser()
config_parser.read_file(args.config_file)
config = dict(config_parser['default'])

# Create Producer instance
producer = Producer(config)

def delivery_callback(err, msg):

    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
        return

    print("Delivery callback to topic {topic}: key = {key:12}".format(
        topic=msg.topic(), key=msg.key().decode('utf-8')))

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    _Payload = request.json

    print(_Payload)

    _datasetType = _Payload ['DatasetType']
    _data = _Payload ['data']
    _pk = "unknown"

    if _datasetType == '1':
        _pk = _data ['code'] + "-" + _data ['dateHour']
    if _datasetType == '2':
        _pk = _data ['code'] + "-" + _data ['dateHour']

    producer.produce("Iot2", json.dumps(_Payload), _pk, callback=delivery_callback)
    producer.poll(10000)
    producer.flush()

    return  jsonify(_Payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)