import requests
import json
import urllib
import base64
import os
import time

class madkuduAPI():
    def __init__(self):
        self.url = "https://api.madkudu.com/v1/%s"
        self.api_key = ''
        self.load_auth_from_file()
        self.cache_dir = './cache/madkuduAPI/'
        self.ensure_dir(self.cache_dir)
        self.cache_requests = True

    def load_auth_from_file(self):
        if self.api_key == '':
            with open ("./auth_madkudu.txt", "r") as myfile:
                text_parse = [x for x in myfile.readlines()][0] + ":"
                self.api_key = base64.b64encode(bytes(text_parse.replace("\n","")))

    def send_request(self,endpoint=None,parameters=None):
        if parameters is None:
            return
        self.parameters = parameters
        url = self.url % (endpoint)
        headers = {'authorization': "Basic " + self.api_key,'cache-control': "no-cache"}
        path = self.cache_dir + self.construct_filename_from_args()
        self.path = path
        if os.path.isfile(path):
            print "Loading " + self.path + " from cache..."
            return self.load_cached_results_from_query()
        print "Fetching for " + self.path
        self.r = requests.request("GET", url, headers=headers, params=parameters)
        results = json.loads(self.r.content)
        self.results_list = results
        if self.cache_requests:
            self.save_result_to_cache(self.r.content)
        return self.results_list

    def load_results_from_file_path(self,path=None):
        if path is None:
            path = 'tswift.json'
        with open(path,"rb") as myfile:
            results = myfile.read().strip()
        results = json.loads(results)
        self.results_list = results
        return self.results_list

    def save_result_to_cache(self,results_list):
        filename = self.construct_filename_from_args()
        path = self.cache_dir + filename
        file = open(path, "wb")
        for item in results_list:
            file.write(item)
        file.close()
        return path

    def load_cached_results_from_query(self):
        filename = self.construct_filename_from_args()
        path = self.cache_dir + filename
        return self.load_results_from_file_path(path)

    def construct_filename_from_args(self):
        domain = self.parameters['domain']
        filename = domain + "_madkudu_.json"
        return filename

    def ensure_dir(self,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

if __name__ == "__main__":
    b = madkuduAPI()
