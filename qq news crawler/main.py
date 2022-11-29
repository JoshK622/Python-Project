import qq_crawler_model
import json
import datetime
import os
fileds = {'news': "http://news.qq.com/",
          'financial': "https://new.qq.com/ch/finance/",
          'technology': "https://new.qq.com/ch/tech/",
          'fashion': "https://new.qq.com/ch/fashion/",
          'car': "https://new.qq.com/ch/auto/",
          'real estate': "http://house.qq.com/",
          'financial management': "https://new.qq.com/ch/finance_licai/",
          'security': "https://new.qq.com/ch/finance_stock/",
          'digital': "https://new.qq.com/ch/digi/"}

if __name__ == "__main__":
    current_time = datetime.datetime.now()
    for field, url in fileds.items():
        model = qq_crawler_model.qq_model(url, field)
        result = model.run()
        result = result.to_dict()
        size = len(result)
        count = 0
        folder = os.path.exists(field)
        print(result)
        if not folder:
            os.makedirs(field)
            print("New folder for", field, "made")
        else:
            print("Saving data into", field, "folder")
        for idx, data in result.items():
            print(idx)
            count += 1
            res = dict.fromkeys((idx,), data)
            jsonOrderedFile = json.dumps(res, indent=4, ensure_ascii=False)
            filename = field + "/" + field + "_" + str(idx).zfill(3) + ".json"
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                jsonfile.write(jsonOrderedFile)
        model.browser.quit()
    end_time = datetime.datetime.now()
    print("Running Time: ", str(end_time - current_time))
