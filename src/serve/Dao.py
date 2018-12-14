import pymongo

col = ''


def init_dao(address, db_name, table_name):
    global col
    my_client = pymongo.MongoClient(address)
    my_db = my_client[db_name]
    col = my_db[table_name]


def store(msg_list):
    for emotion in msg_list:
        tid = emotion['tid']
        uin = emotion['uin']
        created = emotion['created_time']
        content = emotion['content']

        item = {
            'tid': tid,
            'uin': uin,
            'created': created,
            'content': content,
            'info': emotion
        }
        result = col.find_one({'tid': tid, 'uin': uin})

        if result is None:
            x = col.insert_one(item)
            print("已添加")
            print(x.inserted_id)
        else:
            col.update({'tid': tid}, item)
            print('已更新')
            print(tid)
    return 0
