import qq_crawler_model
import json
import datetime
import os
fileds = {
    'real estate': "/html/body/div[1]/div[3]/div/ul/li[13]/a",
    'financial': "/html/body/div[1]/div[3]/div/ul/li[5]/a",
    'news': "/html/body/div[1]/div[3]/div/ul/li[1]/a",
    'technology': "/html/body/div[1]/div[3]/div/ul/li[6]/a",
    'fashion': "/html/body/div[1]/div[3]/div/ul/li[14]/a",
    'car': "/html/body/div[1]/div[3]/div/ul/li[12]/a",
    'financial management': "/html/body/div[1]/div[3]/div/div/div[2]/ul/li[5]/a",
    'security': "/html/body/div[1]/div[3]/div/div/div[2]/ul/li[7]/a",
    'digital': "/html/body/div[1]/div[3]/div/div/div[2]/ul/li[9]/a",
}

if __name__ == "__main__":
    current_time = datetime.datetime.now()
    for field, xp in fileds.items():
        if field != 'real estate':
            model = qq_crawler_model.qq_model(xp, field)
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
                count += 1
                res = dict.fromkeys((idx,), data)
                jsonOrderedFile = json.dumps(res, indent=4, ensure_ascii=False)
                filename = field + "/" + field + \
                    "_" + str(idx).zfill(3) + ".json"
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    jsonfile.write(jsonOrderedFile)
            model.browser.quit()
        else:
            estate_model = qq_crawler_model.estate_model()
            estate_model.run()
    end_time = datetime.datetime.now()
    print("Running Time: ", str(end_time - current_time))
