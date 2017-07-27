import requests
import json
import urllib
import os
import time

class datanyzeAPI():
    def __init__(self):
        self.url = "http://api.datanyze.com/%s/?email=%s&token=%s&%s"
        self.api_key = ''
        self.api_email = ''
        self.load_auth_from_file()
        self.cache_dir = './cache/datanyzeAPI/'
        self.ensure_dir(self.cache_dir)
        self.cache_requests = True

    def load_auth_from_file(self):
        if self.api_key == '':
            with open ("./auth_datanyze.txt", "r") as myfile:
                text_parse = [x for x in myfile.readlines()]
                self.api_email = text_parse[0]
                self.api_key = text_parse[1]

    def send_request(self,endpoint=None,parameters=None):
        if parameters is None:
            return
        self.parameters = parameters
        query = urllib.urlencode(parameters)

        url = self.url % (endpoint,self.api_email,self.api_key,query)
        url = url.replace("\n","")

        path = self.cache_dir + self.construct_filename_from_args()
        self.path = path
        if os.path.isfile(path):
            print "Loading " + self.path + " from cache..."
            return self.load_cached_results_from_query()
        self.r = requests.get(url)
        time.sleep(1.5)
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
        filename = domain + "_datanyze_.json"
        return filename

    def ensure_dir(self,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

if __name__ == "__main__":
    b = datanyzeAPI()
