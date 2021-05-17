import os, sys, csv
import requests
import hashlib
import datetime
import pandas as pd
import base64
from pprint import pprint
from time import sleep

ip = 'http://127.0.0.1:8080'

time_limit = 1

SALT='BlackboxOperator'
def generate_task_uuid(input_string):
    print(input_string)
    s = hashlib.sha256()
    data = (input_string+SALT).encode("utf-8")
    s.update(data)
    return s.hexdigest()

def get_timestamp():
    return int(datetime.datetime.now().utcnow().timestamp())

def question(image_base64):

    task_uuid = generate_task_uuid(str(datetime.datetime.now().utcnow().timestamp()))

    print('task_uuid:', task_uuid)

    #for retry in range(2, -1, -1):
    #    check_data = {
    #        "esun_uuid" : task_uuid,
    #        "esun_timestamp" : get_timestamp(),
    #        "retry" : retry
    #    }
    #    try:
    #        hr = None
    #        hr = requests.post('{}/healthcheck'.format(ip),
    #                json = check_data,
    #                timeout = time_limit)
    #    except Exception as e:
    #        print(e)
    #    if hr and hr.status_code == requests.codes.ok:
    #        break
    #else: raise Exception("err, health check failed")

    #print("pass health check")

    for retry in range(2, -1, -1):
        stmp = get_timestamp()
        inference_data = {
            "esun_uuid" : task_uuid,
            #"server_uuid" : hr.json()['server_uuid'],
            "esun_timestamp" : stmp,
            "image" : image_base64,
            "retry" : retry
        }
        try:
            ir = None
            ir = requests.post('{}/inference'.format(ip),
                    json = inference_data,
                    timeout = time_limit)
            if ir.status_code == requests.codes.ok:
                print(ir.json()['answer'])
            #else:
            #    print("invalid answer.")
            print("total cost {} secs.".format(get_timestamp() - stmp))
        except Exception as e:
            print(e)
        if ir and ir.status_code == requests.codes.ok:
            break
    else:
        raise Exception("inference failed, NO SCORE")

    return ir.json()['answer']

def recall(tr, pr):
    return len(set(tr) & set(pr)) / len(tr)

def precision(tr, pr):
    return len(set(tr) & set(pr)) / len(pr) if len(pr) else 0.0

def f1(tr, pr):
    rc = recall(tr, pr)
    pc = precision(tr, pr)
    return 2 / ((rc ** -1) + (pc ** -1)) if rc and pc else 0.0

def scoring(tr, pr):
    s = []
    for t, p in zip(tr, pr):
        if not isinstance(tr, list) or not isinstance(pr, list):
            s.append(0.0)
        elif not t and not p:
            s.append(1.0)
        elif not t and p:
            s.append(0.0)
        elif t and not p:
            s.append(0.0)
        else:
            s.append(f1(t, p))
    return s

def emit_question(fpath):
    with open(fpath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        try:
            answer = question(encoded_string)
        except Exception as e:
            print(e)
            answer = 'error'
        sleep(0.2)
        return answer

if __name__ == '__main__':
    #queries = pd.read_csv(queryFile)
    if len(sys.argv) < 2:
        print("Usage: {} [... path to image file or directory]".format(sys.argv[0]))
        exit(0)

    for path in sys.argv[1:]:
        if os.path.isfile(path):
            pred = emit_question(path)
            print("{} ?=> {}".format(path, pred))
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    fpath = os.path.join(root, name)
                    pred = emit_question(fpath)
                    print("{} ?=> {}".format(fpath, pred))
                    #lab = name.split('_')[1].split('.')[0]
        else: print("no such file or directory: {}".format(path))


    #for idx, (q_id, q_cap, q_cont, *_) in \
    #        enumerate(zip(queries['index'],queries['title'], queries['content'])):
    #    print('Query{}: {}'.format(idx, q_cap))
    #    index.append(q_id)
    #    truth.append(sorted(am.get(q_id, [])))
    #    try:
    #        answer = question(q_cont)
    #    except Exception as e:
    #        print(q_id, e)
    #        answer = [str(e)]
    #    predict.append(sorted(answer))
    #    sleep(0.2)
    #result = open("result.txt", "w")
    #score = scoring(truth, predict)
    #result.write('question: {} score: {}\n'.format(len(score), sum(score)))
    #result.write('index,score,pred,truth\n')
    #for idx, sc, tr, pr in zip(index, score, truth, predict):
    #    result.write('{},{},{},{}\n'.format(idx, sc, pr, tr))
    #result.close()
    #print('score: {}'.format(sum(score)))
