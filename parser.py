import requests
import time
import json
import csv

from datetime import datetime
from api_datanyze import datanyzeAPI
from api_madkudu import madkuduAPI
from segment_mapping import segment_web_tech
from csv_output import CSVOutput

class Parser():
    def __init__(self,start_date,end_date,mapping,read_in_file,read_out_file):
        self.company_list = []
        self.unable_to_process = []
        self.output_array = []
        self.mapping = mapping
        self.read_in_companies(read_in_file)
        self.out_file = read_out_file
        self.api_datanyze = datanyzeAPI()
        self.api_madkudu = madkuduAPI()
        self.endpoints = {"datanyze":"domain_history","madkudu":"companies"}
        self.start_date = start_date
        self.end_date = end_date

    def read_in_companies(self,read_in_file):
        company_reader = csv.reader(open(read_in_file, 'r+U'), delimiter=',', quoting=csv.QUOTE_NONE)
        company_counter = 0
        for company in company_reader:
            if len(company)>0 and company_counter<500:
                self.company_list.append({"alexa_rank":company[0],"company_name":company[1]})
            company_counter += 1
        return self.company_list

    def domain_scoring(self):
        analysis_dictionary = dict()

        for company_item in self.company_list:
            self.data = {"domain":company_item['company_name']}
            api_datanyze_resp = self.api_datanyze.send_request(self.endpoints['datanyze'],self.data)
            api_madkudu_resp = self.api_madkudu.send_request(self.endpoints['madkudu'],self.data)

            madkudu_score = api_madkudu_resp['properties']['customer_fit']['segment']
            for date, subdict in api_datanyze_resp.iteritems():
                try:
                    if date == 'message':
                        self.unable_to_process.append(company_item['company_name'])
                        break
                    date = date.replace(",","").replace(" ","-")
                    date = datetime.strptime(date, "%B-%d-%Y").date()

                    if date >= self.start_date and date <= self.end_date:
                        for status, service_list in subdict.iteritems():
                            for platform_name in service_list:
                                if platform_name in self.mapping:
                                    platform_name = self.mapping[platform_name]
                                date = str(date)
                                status = status.encode('ascii','ignore')
                                platform_name = platform_name.encode('ascii','ignore')
                                madkudu_score = madkudu_score.encode('ascii','ignore')
                                output = (company_item['company_name'],madkudu_score,company_item['alexa_rank'],platform_name,status,date)
                                self.output_array.append(output)

                except Exception as e:
                    self.unable_to_process.append(company_item['company_name'])
                    raise

    def write_out(self):
        self.ep_fh = CSVOutput(self.out_file)
        for item in self.output_array:
            self.ep_fh.write_row(item)

        print "\nCompleted with the following Exceptions\n"
        print self.unable_to_process

if __name__ == "__main__":
    #set up read in/write out files
    read_in = raw_input("Enter full name of the input file: ")
    read_out = raw_input("Enter full name of desired output file: ")

    #Get Start and End Dates
    input_start_date = raw_input("Enter a Start Date (DD/MM/YYYY): ")
    input_end_date = raw_input("Enter an End Date (DD/MM/YYYY): ")
    dt_start = datetime.strptime(input_start_date, '%d/%m/%Y').date()
    dt_end = datetime.strptime(input_end_date, '%d/%m/%Y').date()

    #Start Parser
    b = Parser(dt_start,dt_end,segment_web_tech,read_in,read_out)
    b.domain_scoring()
    b.write_out()
