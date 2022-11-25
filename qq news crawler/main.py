import qq_crawler_model
import json

if __name__ == "__main__":
    model = qq_crawler_model.qq_model()
    result = model.run()
    result = result.to_dict()
    jsonOrderedFile = json.dumps(result, indent=4, ensure_ascii=False)
    with open('qq_news.json', 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(jsonOrderedFile)
