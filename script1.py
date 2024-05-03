import os
import pandas as pd
import logging
import argparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class PropertyScraper:
    def __init__(self):
        self.driver = self.create_driver()
        self.parser_args()
        self.logger = self.create_logger()


    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        return driver

    def create_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(f'{self.output_file}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def parser_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('input_file_path', help='Input File Path')
        parser.add_argument('output_file_name', help="Output File Path")
        args = parser.parse_args()
        input_file = args.input_file_path
        output_file = args.output_file_name
        input_directory, input_filename = os.path.split(input_file)
        output_directory = os.path.join(input_directory, 'output')
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        self.output_file = os.path.join(output_directory, output_file)
        self.input_file = input_file

    def scrape_property(self, url,type):
        try:
            self.dict = {}
            self.lst = []
            self.driver.get(url)
            self.dict["url"] = url
            # self.dict['branchID'] = branch_id
            self.dict['recordType'] = type
            self.get_address()
            self.get_agents()
            self.get_description()
            self.get_features()
            self.get_area_and_type()
            self.other_details()
            self.get_listingstatus()    
            self.lst.append(self.dict.copy())
            # print(self.dict)
            self.logger.info("Scraped property data for URL: %s", url)
        except Exception as e:
            self.logger.error("Error occurred while scraping property data for URL: %s, Error: %s", url, str(e))

    def get_address(self):
        try:
            data=""
            address = WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'item-address'))
            )
            data=data+address.text
            self.dict['address'] = data
        except Exception as e:
            self.logger.error("Unable to fetch address. Error: %s", str(e))
            self.dict['address'] = None

    def get_description(self):
        try:
            description = WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'block-content-wrap'))
            )
            text = description.text
            self.dict['description'] = text
        except Exception as e:
            self.logger.error("Unable to fetch description. Error: %s", str(e))
            self.dict['description'] = None

    def get_area_and_type(self):
        try:
            features = WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'property-overview-data'))
            )

            lines = features.text.strip().split('\n')
            self.dict['availableSpace'] = lines[2]+lines[3] 

            propertyType = lines[0]
            self.dict['spaceType'] = propertyType
            self.dict['listingUseType'] = propertyType
        except Exception as e:
            self.logger.error("Unable to fetch area and type data. Error: %s", str(e))
            self.dict['availableSpace'] = None
            self.dict['spaceType'] = None
            self.dict['listingUseType'] = None

    def get_features(self):
        try:
            self.dict['buildingDetails'] = None
        except Exception as e:
            self.logger.error("Unable to fetch building features data. Error: %s", str(e))
            self.dict['buildingDetails'] = None

    def get_agents(self):
        try:
            agent_list = []
            agents_name = WebDriverWait(self.driver, 5).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, 'agent-name'))
            )
            agent_list.append(agents_name[0].text)
            agents_phone = WebDriverWait(self.driver, 5).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, 'agent-link'))
            )
            agent_list.append(agents_phone[0].text[4:])
            agents_email = WebDriverWait(self.driver, 5).until(
                ec.presence_of_all_elements_located((By.XPATH, '/html/body/main/section/div[4]/div/div[2]/div/aside/div/div/form/input[1]'))
            )
            # print(agents_email[0].get_attribute('value'))
            agent_list.append(agents_email[0].get_attribute('value'))
            # print(agent_list)
            self.get_agent_details([agent_list])
        except Exception as e:
            self.logger.error("Unable to fetch agents data. Error: %s", str(e))
            agent_list = [[None, None, None]]
            self.get_agent_details(agent_list)

    def get_agent_details(self, agent_list):
        # print(agent_list)
        try:
            for i in range(2):
                if len(agent_list)==1 and i==0:
                    temp = agent_list[i]
                    self.dict[f'agentName{i+1}'] = temp[0] if temp[0] else None
                    self.dict[f'agentTel{i+1}'] = temp[1] if temp[1] else None
                    self.dict[f'agentEmail{i+1}'] = temp[2] if temp[2] else None
                elif len(agent_list)>=2 :
                    temp = agent_list[i]
                    self.dict[f'agentName{i+1}'] = temp[0] if temp[0] else None
                    self.dict[f'agentTel{i+1}'] = temp[1] if temp[1] else None
                    self.dict[f'agentEmail{i+1}'] = temp[2] if temp[2] else None
                else:
                    self.dict[f'agentName{i+1}'] = None
                    self.dict[f'agentTel{i+1}'] = None
                    self.dict[f'agentEmail{i+1}'] = None
        except Exception as e:
            self.logger.error("Unable to fetch agent details. Error: %s", str(e))
            for i in range(1, 3):
                self.dict[f'agentName{i}'] = None
                self.dict[f'agentTel{i}'] = None
                self.dict[f'agentEmail{i}'] = None

    def get_listingstatus(self):
        try:
            listingstatus = WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'property-labels-wrap'))
            )
            listing_type = listingstatus.text
            self.dict['suiteStatus'] = listing_type
            self.dict['listingStatus'] = listing_type
        except Exception as e:
            self.logger.error("Unable to fetch listing status data. Error: %s", str(e))
            self.dict['suiteStatus'] = None
            self.dict['listingStatus'] = None

    def other_details(self):
        try:
            price = WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'item-price-wrap'))
            ).text

            self.dict['outgoings'] =price
        except Exception as e:
            self.logger.error("Unable to fetch property price. Error: %s", str(e))
            self.dict['outgoings'] = None

    def write_to_file(self, file_path):
        df = pd.DataFrame(self.lst)
        if os.path.exists(file_path):
            df.to_csv(file_path, header=False, mode="a", index=False, encoding="utf-8")
        else:
            df.to_csv(file_path, header=True, index=False, encoding="utf-8")

    def scrape_properties_from_csv(self):
        self.input_file = pd.read_csv(self.input_file)
        for index, row in self.input_file.iterrows():
            self.scrape_property(row['url'],row['recordType'])
            self.write_to_file(self.output_file)
            self.logger.info("Processed %d records and wrote 1 record", index + 1)
            # break






if __name__ == "__main__":
    scraper = PropertyScraper()
    scraper.scrape_properties_from_csv()