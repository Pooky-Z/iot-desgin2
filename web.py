from flask import Flask, request, render_template,jsonify
from model import Info, Input
import asyncio
from orm import create_pool
from connect import socketOpen
import threading
import json

def count(list):
    time = []
    count1 = []
    time_clipse = []
    for i in list:
        time_clipse.append(str(i["time"])[11:16])
    print(time_clipse)
    start = int(time_clipse[0].split(":")[0])
    end = int(time_clipse[-1].split(":")[0])
    if ((end - start) == 0):
        time.append(":".join([str(start), "00"]))
        time.append(":".join([str(start), "30"]))
    else:
        for i in range(2 * (end - start)):
            time.append(":".join([str(start), "00"]))
            time.append(":".join([str(start), "30"]))
            start += 1
    time.append(":".join([str(end+1), "00"]))
    for j in range(len(time) - 1):
        c = 0
        for t in time_clipse:
            if ((time[j] < t and t < time[j + 1]) or t == time[j]):
                c += 1
        count1.append(c)
    print(count1)
    print(time)
    return count1, time


async def compare(loop):
    valid_name = []
    all_name = []
    unvalid_name = []
    await create_pool(
        loop=loop,
        host='127.0.0.1',
        port=3306,
        user="root",
        password="admin",
        db="data")
    valid_persons = Info()
    all_persons = Input()
    valid_list = await valid_persons.findAll()
    count1, time = count(valid_list)
    all_list = await all_persons.findAll()
    for person in valid_list:
        valid_name.append(person["name"])
    for person in all_list:
        all_name.append(person["name"])
    allnumber, validnumber = len(all_name), len(valid_name)
    length = allnumber - validnumber

    if (length > 0):
        for i in all_name:
            t = 0
            for j in valid_name:
                if (j == i):
                    t += 1
            if (t == 0):
                unvalid_name.append(i)
    unvalid_list = []
    for i in unvalid_name:
        for person in all_list:
            if (person["name"] == i):
                unvalid_list.append(person)
    return valid_list, unvalid_list, allnumber, validnumber, count1, time


app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def index():
    method=request.method
    print(method)
    # data=socketOpen()
    # print(data)
    # threading.Thread(target=socketOpen,args=())
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)
    coroutine = compare(loop1)
    task = asyncio.ensure_future(coroutine)
    loop1.run_until_complete(task)
    valid_persons, unvalid_persons, allnumber, validnumber, count1, time = task.result()
    
    if(method=="GET"):
        return render_template(
            "table1.html",
            valid_persons=valid_persons,
            unvalid_persons=unvalid_persons,
            allnumber=allnumber,
            validnumber=validnumber,
            count=count1,
            time=time)
    if(method=="POST"):
        dic={"valid_persons":valid_persons,"unvalid_persons":unvalid_persons,"allnumber":allnumber,"validnumber":validnumber,"count":count1,"time":time}
        print("nmsl")
        return jsonify(dic)

@app.route("/ajax", methods=["GET","POST"])
def update():
    print("nmsl")
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)
    coroutine1 = compare(loop1)
    task = asyncio.ensure_future(coroutine1)
    loop1.run_until_complete(task)
    valid_persons, unvalid_persons, allnumber, validnumber = task.result()
    print(valid_persons)
    return "nmsl"


if __name__ == "__main__":
    app.run(debug=True,port=8080)
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # coroutine = compare(loop)
    # task = asyncio.ensure_future(coroutine)
    # loop.run_until_complete(task)
    # valid_persons, unvalid_persons, allnumber, validnumber = task.result()
