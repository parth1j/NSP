import json

INPUT_FILES = [
    r'C:\Users\admin\Desktop\Sent2LogicalForm\data\train_spider.json',
]
tables={}
count=0
for INPUT_FILE in INPUT_FILES:
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for entry in data:
            tables[entry['db_id']] = True
            if count==100:
                break
            count+=1


print(list(tables.keys()))