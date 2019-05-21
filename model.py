from orm import Model, StringField, BooleanField, FloatField, TextField, create_pool, IntegerField

import time, uuid, asyncio
import os


def next_id():
    # id='%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)
    id = "%.f" % (float(time.time() * 1000))
    return str(int(id) - 155360000000)


class Info(Model):
    __table__ = "info"

    id = IntegerField(primary_key=True)
    name = StringField(ddl="varchar(500)")
    gender=StringField(ddl="varchar(10)")
    time = StringField(ddl="varchar(20)")


class Input(Model):
    __table__ = "input"

    id = IntegerField(primary_key=True)
    name = StringField(ddl="varchar(10)")
    gender = StringField(ddl="varchar(10)")
    url = StringField(ddl="varchar(20)")


async def test(loop):
    await create_pool(
        loop=loop,
        host='127.0.0.1',
        port=3306,
        user="root",
        password="admin",
        db="data")
    # for file in os.listdir("./img"):
    #     name=file[:-4]
    #     worker=Input(name=name,gender="1",url="./img/"+file)
    #     await worker.save()
    i=0
    # for file in os.listdir("./img"):
    #     i+=1
    #     if(i==15):
    #         break
    #     arrivetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     name = file[:-4]
    #     medical_person = Info(name=name, gender="男",time=arrivetime)
    #     await medical_person.save()
    person=Info()
    name=await person.findNumber("id")
    
    print(name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
