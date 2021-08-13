import json

from flask_restful import Resource

from SpeedTest import test


class RunTest(Resource):
    def get(self):
        results = test()

        dict_results = {
            "Server": results[0],
            "Jitter": results[1],
            "Ping": results[2],
            "Download": results[3],
            "Upload": results[4]
        }

        return dict_results
