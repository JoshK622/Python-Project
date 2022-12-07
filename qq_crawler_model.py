from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time
import os
import json

s = Service(
    'C:\Program Files\Google\Chrome\Application\chromedriver_win32\chromedriver.exe')
more_xpath = "/html/body/div[1]/div[3]/div/div/div[1]"


class qq_model():
    def __init__(self, xpath, field):
        self.xpath = xpath
        self.field = field
        self.browser = webdriver.Chrome(service=s)

    def enter_main_website(self):
        self.browser.get("https://www.qq.com/")
        while self.xpath_exist(self.xpath) == False or self.xpath_exist(more_xpath) == False:
            pass
        self.browser.find_element(By.XPATH, more_xpath).click()
        self.browser.find_element(By.XPATH, self.xpath).click()
        self.browser.switch_to.window(self.browser.window_handles[1])

    def get_links(self):

        xpath = '//li[@class = "item cf itme-ls"]\
                    //div[@class = "detail"]//h3//a'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        links = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for link in links:
            arr.append(link.get_attribute('href'))
        return arr

    def get_title(self):
        xpath = '//li[@class = "item cf itme-ls"]\
                //div[@class = "detail"]//h3//a[@href]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        self.locate(xpath)
        titles = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for title in titles:
            arr.append(title.text)
        return arr

    def get_id(self):
        xpath = '//ul[@class = "list"]//li[@class = "item cf itme-ls"]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        self.locate(xpath)
        ids = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for id in ids:
            arr.append(id.get_attribute('id'))
        return arr

    def get_date(self, id_series):
        date = []
        for id in id_series:
            date.append(id[0:4]+"-"+id[4:6]+"-"+id[6:8])
        return date

    def get_post_time(self):
        xpath = '//*[@id="LeftTool"]/div/div[3]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        post_time = self.browser.find_element(By.XPATH, xpath)
        post_time = post_time.get_attribute("textContent")
        return post_time

    def get_author(self):
        xpath = '//div[@class = "fl"]//*[@class = "source"]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        authors = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for author in authors:
            arr.append(author.text)
        return arr

    # def get_external_links(self):
    #     xpath = '//*[@class = "detail"]//h3//a'
    #     if self.xpath_exist(xpath) == False:
    #         return np.NaN
    #     ex_links = self.browser.find_elements(By.XPATH, xpath)
    #     arr = []
    #     for ex_link in ex_links:
    #         arr.append(ex_link.get_attribute('href'))
    #     return arr

    def get_content(self):
        xpath = '//div[@class = "content-article"]//p[@class = "one-p"]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        content = self.browser.find_elements(By.XPATH, xpath)
        string = ""
        for cont in content:
            string += cont.text
            string += '\n'
        return string

    def enter_art_site(self, links):  # get the information of all the article in the links
        length = len(links)
        content = []
        post_time = []
        count = 0
        for link in links:
            self.browser.get(link)    # enter the article site
            content.append(self.get_content())
            post_time.append(self.get_post_time())
            count += 1
            print("Field: ", self.field, "\nProgress: ", count, "/", length)
        return post_time, content

    def xpath_exist(self, xpath):
        try:
            self.browser.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    def locate(self, xpath):
        try:
            WebDriverWait(self.browser, 20, 0.5).until(EC.visibility_of_element_located(
                (By.XPATH, xpath)))
            return True
        except:
            return False

    def scroll_to_bottom(self):
        temp_height = 0
        while True:
            self.browser.execute_script("window.scrollBy(0, 10000)")
            time.sleep(1.5)
            check_height = self.browser.execute_script(
                "return document.documentElement.scrollTop || \
                window.pageYOffset || document.body.scrollTop;")
            if check_height == temp_height:
                break
            temp_height = check_height

    def run(self):
        self.enter_main_website()
        self.scroll_to_bottom()
        Id = self.get_id()
        Url = self.get_links()
        print("Total", len(Url), "Articles")
        Title = self.get_title()
        Author = self.get_author()
        print(Author)
        Publish_Date = self.get_date(Id)
        Post_time, Content = self.enter_art_site(Url)
        d_arr = []

        for i in range(len(Url)):
            d = {"tags": [self.field], "id": Id[i], "article_url": Url[i], "title": Title[i], "author": Author[i], "date": Publish_Date[i] + " " + Post_time[i],
                 "content": Content[i]}
            d_arr.append(d)
        return d_arr


class estate_model():
    def __init__(self):
        self.browser = webdriver.Chrome(service=s)

    def get_title(self):
        xpath = '//div[@class = "detail"]//h3//a'
        title = self.browser.find_elements(By.XPATH, xpath)
        if not title:
            return np.NaN
        return title.text

    def get_links(self):
        self.browser.get("https://house.qq.com/")
        time.sleep(1)
        self.scroll_to_bottom()
        time.sleep(1)
        xpath = "//ul[@class='arealist area2']//li//div//h3//a"
        if self.xpath_exist(xpath) == False:
            return np.NAN
        arr = []
        for i in range(1, 5):
            l_xpath = '/html/body/div[2]/div[5]/div[1]/div[3]/ul/li[' + \
                str(i) + ']'
            self.browser.find_element(By.XPATH, l_xpath).click()
            links = self.browser.find_elements(By.XPATH, xpath)
            for link in links:
                arr.append(link.get_attribute('href'))
        return pd.Series(arr)

    def enter_art_site(self, links):
        folder = os.path.exists('real estate')
        if not folder:
            os.makedirs('real estate')
            print("New folder for real estate made")
        else:
            print("Saving data into real estate folder")
        count = 0
        size = len(links)

        for link in links:
            self.browser.get(link)
            id = link.split('/')[-1].split('.')[0]
            date = id[:4] + '-' + id[4:6] + '-' + id[6:8]
            content = self.get_content()
            tag = 'real estate'
            post_time = self.get_post_time()
            date = date + " " + post_time
            d = dict(zip(['tags', 'id', 'date', 'content', 'article_url'], [
                tag, id, date, content, link]))
            count += 1
            print("Field: Real Estate", "\nProgress: ", count, "/", size)
            jsonOrderedFile = json.dumps(d, indent=4, ensure_ascii=False)
            filename = 'real estate' + "/" + 'Real_Estate' + \
                "_" + str(count).zfill(3) + ".json"
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                jsonfile.write('[\n')
                jsonfile.write(jsonOrderedFile)
                jsonfile.write('\n]')
        self.browser.quit()

    def scroll_to_bottom(self):
        temp_height = 0
        while True:
            self.browser.execute_script("window.scrollBy(0, 10000)")
            time.sleep(1.5)
            check_height = self.browser.execute_script(
                "return document.documentElement.scrollTop || \
                window.pageYOffset || document.body.scrollTop;")
            if check_height == temp_height:
                break
            temp_height = check_height

    def get_external_links(self):
        xpath = '//*[@class = "detail"]//h3//a'
        if self.xpath_exist(xpath) == False:
            return np.NaN
        ex_links = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for ex_link in ex_links:
            arr.append(ex_link.get_attribute('href'))
        return arr

    def get_content(self):
        xpath = '//div[@class = "content-article"]//p[@class = "one-p"]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        content = self.browser.find_elements(By.XPATH, xpath)
        string = ""
        for cont in content:
            string += cont.text
            string += '\n'
        return string

    def get_post_time(self):
        xpath = '//*[@id="LeftTool"]/div/div[3]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        post_time = self.browser.find_element(By.XPATH, xpath)
        post_time = post_time.get_attribute("textContent")
        return post_time

    def run(self):
        links = self.get_links()
        self.enter_art_site(links)

    def xpath_exist(self, xpath):
        try:
            self.browser.find_element(By.XPATH, xpath)
            return True
        except:
            return False
