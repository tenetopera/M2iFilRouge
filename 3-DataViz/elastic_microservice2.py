import json
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, jsonify
import warnings
warnings.filterwarnings("ignore")

if __name__ != '__main__':
    exit(0)

app = Flask(__name__)

class Elastic:

    def __init__(self, _index = "default"):
        self.host = "172.19.90.23"
        self.port = 9200
        self.es = None
        self.connect()
        self.INDEX_NAME = _index
        print("Default Index set to ", self.INDEX_NAME)

    def connect(self):

        #self.es = Elasticsearch([{'host': self.host, 'port': self.port}])

        self.es = Elasticsearch(
            cloud_id="Iot_Projet:dXMtZWFzdDQuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGQzMGE3M2JjYjNhNzQyMTA5NjhiMjAzM2Q3NDJjNzI3JDcxYjU5MTlhMzBmNDQ3OGJiNDY2MGY3M2Q4NjYzMmFj",
            http_auth=("psavoia", "Uriel2022$1")
        )

        print()
        if self.es.ping():
            print("ES connected successfully")
        else:
            print("Not connected")

        print("Connect response is :: {}\n".format(self.es.info()))
        print()

    def create_index(self, _index = "default"):
        #exists(index="my-index"
        if  self.es.indices.exists(_index):
            return

            #print("deleting '%s' index..." % (_index))
            #res = self.es.indices.delete(index=_index)
            #print(" response: '%s'" % (res))

        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
                "refresh_interval": "1s"
            }
        }

        print("creating '%s' index..." % (_index))
        res = self.es.indices.create(index=_index, body=request_body, ignore=400)
        print(" response: '%s'" % (res))


    def push_to_index(self, message=dict(),_index="default"):
        print("pushing to index : ", _index)
        try:
            response= self.es.index(
                index= _index, #self.INDEX_NAME,
                #doc_type= "log",
                refresh = True,
                document=json.dumps(message)
                #body= message
            )
            print("Write   response is :: {}".format(response))
            print("Refresh response is :: {}\n".format(es_obj.es.indices.refresh(index=_index)))
        except Exception as e:
            print("Exception is :: {}".format(str(e)))

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    _Payload = request.json
    print(_Payload)

    print("insert into elasticsearch")

    _index = "iot_v4_"
    es_obj.create_index(_index + _Payload ['DatasetType'])
    es_obj.push_to_index(_Payload ['data'], _index + _Payload ['DatasetType'])

    return  jsonify(_Payload)

es_obj = Elastic()
app.run(host='0.0.0.0', port=6600)