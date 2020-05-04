
# # import json
# # import requests
# # url = 'http://127.0.0.1:5000/login'
# # values = {"username":"diaa",
# #     'email': 'diaa.elsayedziada@gsdfasdmail.com',
# #           'password': 'aaa'}

# # r = requests.post(url, json=values)
# # content= json.loads(r.content)



# # print(content['token'])




# # import socketio

# # # standard Python
# # # sio = socketio.Client()

# # # asyncio
# # sio = socketio.AsyncClient()
# # sio.connect('http://localhost:5000')

# # @sio.on('message')
# # def on_connect(msg):
# #     print(msg,'\n\n\n\n\n')

# # sio.emit('say', {'foo': 'bar'})

# print('aaaaaa\n\n\n')
# import socketio
# import time 

# import numpy as np
# import pickle

# arr = np.random.randn(300,400,3)
# arr = pickle.dumps(arr)

# sio = socketio.Client()
# sio.connect('http://localhost:5000/', namespaces=["/computer-vision"])

# f = True
# @sio.event
# def connect():
#     print('connection established')
# i=0
# t =time.time()
# data = arr
# @sio.event
# def reciver(data):
#     # print(data)
#     global i, t,f
#     i+=1
#     if time.time() - t >=1:
#         print(f"fps: {i}")
#         i = 0
#         t = time.time()
#     f = False  
#     # print("aaaa")
#     # sio.emit("feedforward",'data',namespace="/computer-vision")
#     # print("aaaa")

#     # print('message received with ', data)
#     # sio.emit('my response', {'response': 'my response'})

# @sio.event
# def disconnect():
#     print('disconnected from server')
import socketio
import time 

import numpy as np
import pickle

arr = np.random.randn(400,300,3)
arr = pickle.dumps(arr)
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
i=0
f=True
t =time.time()
token = "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4ODE5ODQ5NywiZXhwIjoxNTg4MjAwMjk3fQ.eyJ1c2VyX2lkIjoxfQ.ypPF0laj2kcH4JvLF5j9KKJ3CV1NfwUClWUjiJcStXJLRWJPy66iJ64KqqXD694V7jXsbh0LbjGu7QOVdUwtjw"
boxes = None
@sio.event
def reciver(data):
    global boxes
    data = pickle.loads(data)
    # print(data)
    boxes = data.get('faces', [])
    global i, t,f
    i+=1
    if time.time() - t >=1:
        print(f"fps: {i}")
        i = 0
        t = time.time()
    # sio.emit("forward",{"token":token,"inputs":arr},namespace='/streamer')
    f = False
    # print('message received with ', data)
    # sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000',namespaces=["/streamer"])

# while True:
    # time.sleep(0.0001)
# print(1)
# sio.wait()
import cv2 

cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read()
    frame = frame.astype(np.uint8)

    sio.emit("forward",{
        "token":token,
        "inputs":pickle.dumps(frame),
        "opts":{
            "detectors":["face"],
            "from_face":["gender",'expression'],
            "labels":{
                "gender":['Female', 'Male'],
                "expression":['ANGER', 'DISGUST', 'FEAR', 'HAPPINESS', 'NEUTRAL', 'SADNESS', 'SURPRISE']
            }
        }

    },namespace='/streamer')

    while f:
        time.sleep(0.0000000000001)
    f = True
    for box in boxes:
        (startX, startY, endX, endY) = box
      
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
    cv2.imshow('aa', frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cam.release()
cv2.destroyAllWindows()

sio.wait()


d = {
        "inputs":arr,
        "opts":{
            "detectors":["face"],
            "from_face":["gender",'expression'],
            "labels":{
                "gender":['Female', 'Male'],
                "expression":['ANGER', 'DISGUST', 'FEAR', 'HAPPINESS', 'NEUTRAL', 'SADNESS', 'SURPRISE']
            }
        }

    }