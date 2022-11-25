from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import time
import datetime
s = Service(
    'C:\Program Files\Google\Chrome\Application\chromedriver_win32\chromedriver.exe')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


class qq_model():
    def __init__(self):
        self.url = "https://news.qq.com/"
        self.browser = webdriver.Chrome(service=s)

    def enter_main_website(self):
        self.browser.get(self.url)
        self.scroll_to_bottom()

    def get_links(self):
        xpath = '//ul[@class = "list"]//li[@class = "item cf itme-ls"]\
                //div[@class = "detail"]//h3//a'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        links = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for link in links:
            arr.append(link.get_attribute('href'))
        return pd.Series(arr)

    def get_title(self):
        xpath = '//ul[@class = "list"]//li[@class = "item cf itme-ls"]\
                //div[@class = "detail"]//h3//a[@href]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        self.locate(xpath)
        titles = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for title in titles:
            arr.append(title.text)
        return pd.Series(arr)

    def get_id(self):
        xpath = '//ul[@class = "list"]//li[@class = "item cf itme-ls"]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        self.locate(xpath)
        ids = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for id in ids:
            arr.append(id.get_attribute('id'))
        return pd.Series(arr)

    def get_date(self, id_series):
        date = []
        for id in id_series:
            date.append(id[0:4]+"-"+id[4:6]+"-"+id[6:8])
        return pd.Series(date)

    def get_post_time(self):
        xpath = '//*[@id="LeftTool"]/div/div[3]'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        post_time = self.browser.find_element(By.XPATH, xpath)
        post_time = post_time.get_attribute("textContent")
        return post_time

    def get_author(self):
        xpath = '//ul[@class = "list"]//li[@class = "item cf itme-ls"]\
                //div[@class = "detail"]//div[@class = "binfo cf"]//div[@class = "fl"]//a'
        if self.xpath_exist(xpath) == False:
            return np.NAN
        authors = self.browser.find_elements(By.XPATH, xpath)
        arr = []
        for author in authors:
            arr.append(author.text)
        return pd.Series(arr)

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

    def enter_art_site(self, links):  # get the information of all the article in the links
        length = len(links)
        content = []
        external_links = []
        post_time = []
        count = 0
        for link in links:
            self.browser.get(link)    # enter the article site
            self.scroll_to_bottom()
            content.append(self.get_content())
            external_links.append(self.get_external_links())
            post_time.append(self.get_post_time())
            count += 1
            print("Progress: ", str(count), "/", str(length))
        return pd.Series(post_time), pd.Series(content), pd.Series(external_links)

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
        current_time = datetime.datetime.now()
        self.enter_main_website()
        Id = self.get_id()
        Url = self.get_links()
        print("Total", len(Url), "Articles")
        Title = self.get_title()
        Author = self.get_author()
        Publish_Date = self.get_date(Id)
        Post_time, Content, Recommendation_links = self.enter_art_site(Url)
        result = pd.DataFrame({"Id": Id, "Url": Url, "Title": Title, "Author": Author, "Publish_Date": Publish_Date,
                               "Post_time": Post_time, "Content": Content, "Recommendation_links": Recommendation_links})
        self.browser.quit()
        end_time = datetime.datetime.now()
        print("Running Time: ", str(end_time - current_time))
        return result.transpose()  # return the Pandas DataFrame
