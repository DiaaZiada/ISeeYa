# ISeeYa

**_Machine learning APIs for developers_**

Iseeya brings machine learning expertise to any kind of developers in a powerful and easy-to-use package that interacts with Iseeya's API in realtime performance
# Install & Run
```
$pip install -r requirements.txt
$python run.py
```

# How to ISeeya

## Token

First, you have to get your token to be able to access all ISeeya services. You can easily get your token by clicking on the  **"Token"** button near to el Account button on the navigation bar after login. This will direct you to token page when you reach it press to  **"Generate Token"** button and your token will appears, copy the token to use it in your request

## Packages

we had prepared a python Package that handles all requests for you you can download it from  [here](https://drive.google.com/file/d/12pYm0glhgC3ga1TjL3hGjlC9LLeo85IY/view?usp=sharing).

# Face Detection

With ISeeya face detection API, you can detect faces in an image.

by sending an image and return the dimensions of boxes that round the faces in the image

## How to get face detection

You only need to add  **"face"** keyword into the list of detectors

**Example**
```py
requset_for = {
    "detectors":["face"]
}
```

and the result will be in the return result dictionary you can simply access by the key  **"faces"**

faces = results['faces']

faces: is a list of NumPy arrays every array contains (startX, startY, endX, endY) of the box that contains the face


# Gender Detection

With ISeeya face detection API, you can detect the gender of the person using only his/her image or image that contains more than one person.

by sending an image and return list evey element contains string of his/her gender (Male/Female) with the confidence in percentage of that decision

## How to get gender detection

You only need to add  **"gender"** keyword into the list of from_face

**Example**
```py
requset_for = {
    "from_face":["gender"]
}
```

and the result will be in the return result dictionary you can simply access by the key  **"gender"**

genders = results['gender']

gender: is a list of lists every list contains two elements the first element is a string of ("Male", "Female"), the second element is an integer of the percentage of confidence of that decision

# Expression Detection

With ISeeya face detection API, you can detect the Expressions of the person using only his image or image that contains more than one person.

by sending an image and return list evey element contains string of the expersion with the confidence in percentage of that decision

## Expersions

-   'ANGER'
-   'DISGUST'
-   'FEAR'
-   'HAPPINESS'
-   'NEUTRAL'
-   'SADNESS'
-   'SURPRISE'

## How to get expression detection

You only need to add  **"expression"** keyword into the list of from_face

**Example**
```py
requset_for = {
    "from_face":["expression"]
}
```

and the result will be in the return result dictionary you can simply access by the key  **"expression"**

expressions = results['expression']

expressions: is a list of lists every list contains two elements the first element is a string of the expression, the second element is an integer of the percentage of confidence of that decision

# Collection Detection

With ISeeya face detection API, you can group of information of a person using only his image or image that contains more than one person.

by sending an image and return list every element contains a list of information that detected from the face with the confidence in the percentage of that decision

## Collection

Illumination:

-   'BAD'
-   'HIGH'
-   'MEDIUM'

Pose:

-   'DOWN'
-   'FRONTAL'
-   'LEFT'
-   'RIGHT'
-   'UP'

Occlusion:

-   'BEARD'
-   'GLASSES'
-   'HAIR'
-   'HAND'
-   'NONE'
-   'ORNAMENTS'
-   'OTHERS'

Age:

-   'Middle'
-   'Old'
-   'Young'

Makeup:

-   'OVER'
-   'PARTIAL'

## How to get collection detection

You only need to add  **"multiple"** keyword into the list of from_face

**Example**
```py
requset_for = {
    "from_face":["multiple"]
}
```

and the result will be in the return result dictionary you can simply access by the key  **"multiple"**

multiple = results['multiple']

multiple: is a dictionary its value is a list of lists every list contains two elements the first element is a string of a collection model detection, the second element is an integer of the percentage of confidence of that decision

**_Example_**

retsult["illumination"][0]

retsult["pose"][0]

retsult["occlusion"][0]

retsult["age"][0]

retsult["makeup"][0]

## FULL Example

```py
import socketio
import time
import numpy as np
import pickle  
import cv2

sio = socketio.Client()

@sio.event
def  connect():
	print('connection established')

i=0
f=True
t =time.time()

token =  "eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwNzUyODc4NCwiZXhwIjoxNjA3NTMwNTg0fQ.eyJ1c2VyX2lkIjoxM30.Om0ltm7YHtJwXciPbRFZhMLXdbhRcehujAURL2sIBYRg661QUUSkN8v7sSIeAA3jlXoFoxaIfnYrUlOXPcKAIg"

boxes, data =  None,  None

@sio.event
def  reciver(dat):
	global boxes,data
	data = pickle.loads(dat)
	boxes = data.get('faces',  [])
	global i, t,f
	i+=1
	if time.time()  - t >=1:
		print(f"fps: {i}")
		i =  0
		t = time.time()
	f =  False 

@sio.event
def  disconnect():
	print('disconnected from server')
	
sio.connect('http://localhost:5000',namespaces=["/streamer"]) 

cam = cv2.VideoCapture(0)

while  True:

	_, frame = cam.read()
	frame = frame.astype(np.uint8)
	sio.emit("forward",{
		"token":token,
		"inputs":pickle.dumps(frame),
		"opts":{
			"detectors":["face"],
			"from_face":["gender",'expression',"multiple"],
			"labels":{

			"gender":['Female',  'Male'],
			"expression":['ANGER',  'DISGUST',  'FEAR',  'HAPPINESS',  'NEUTRAL',  'SADNESS',  'SURPRISE']
			}
		}  
	},namespace='/streamer')

	  

while f:

	time.sleep(0.0000000000001)

	f =  True

	box = data.pop("faces")

	for box in boxes:
		(startX, startY, endX, endY)  = box
		cv2.rectangle(frame,  (startX, startY),  (endX, endY),  (0,  255,  0),  2)
		cv2.putText(frame,f"{data['gender'][0][0]}:{data['gender'][0][1]}%",  (endX, startY), cv2.FONT_HERSHEY_SIMPLEX,1,  (0,  255,  255),  1, cv2.LINE_AA)
		cv2.putText(frame,f"{data['expression'][0][0]}:{data['expression'][0][1]}%",  (endX, startY+25), cv2.FONT_HERSHEY_SIMPLEX,1,  (0,  255,  255),  1, cv2.LINE_AA)
		data = data["multiple"]
		cv2.putText(frame,f"{data['illumination'][0][0]}:{data['illumination'][0][1]}%",  (endX, startY+50), cv2.FONT_HERSHEY_SIMPLEX,1,  (0,  255,  255),  1, cv2.LINE_AA)
		cv2.putText(frame,f"{data['pose'][0][0]}:{data['pose'][0][1]}%",  (endX, startY+75), cv2.FONT_HERSHEY_SIMPLEX,1,  (0,  255,  255),  1, cv2.LINE_AA)
		cv2.putText(frame,f"{data['occlusion'][0][0]}:{data['occlusion'][0][1]}%",  (endX, startY+100), cv2.FONT_HERSHEY_SIMPLEX,1,  (0,  255,  255),  1, cv2.LINE_AA)
		cv2.putText(frame,f"{data['age'][0][0]}:{data['age'][0][1]}%",  (endX, startY+125), cv2.FONT_HERSHEY_SIMPLEX,1,  (0,  255,  255),  1, cv2.LINE_AA)
		cv2.putText(frame,f"{data['makeup'][0][0]}:{data['makeup'][0][1]}%",  (endX, startY+150), cv2.FONT_HERSHEY_SIMPLEX,1,  (0,  255,  255),  1, cv2.LINE_AA)

	cv2.imshow('aa', frame)
	if cv2.waitKey(1)  &  0xFF  ==  ord("q"):
		break

cam.release()
cv2.destroyAllWindows()
sio.wait()
```
## Example using Streamer module
```py
from time import time
import pickle
import numpy as np
import cv2
from iseeya.streamer import streamer


def write_predictions(labels, image, box, i):
    (_, startY, endX, _) = box
    cv2.putText(image, labels, (endX + 10, startY + 25*i), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255),2)


token = "past your token here"
requset_for = {
        "detectors":["face"],
        "from_face":["gender",'expression', 'multiple']
    }

streamer.token(token)
streamer.request_for(requset_for)

cam = cv2.VideoCapture(0)
t = time()
i=0
while True:
    _, frame = cam.read()

    results = streamer.forward(frame)

    n  = len(results['faces'])

    for i in range(n):
        (startX, startY, endX, endY) = results['faces'][i]

        gender =  f"{results['gender'][i][0]} {results['gender'][i][1]} %"
        write_predictions(gender, frame, (startX, startY, endX, endY), 0)

        expression =  f"{results['expression'][i][0]} {results['expression'][i][1]}%"
        write_predictions(expression, frame, (startX, startY, endX, endY), 1)

        multiple =  f"{results['multiple']['illumination'][i][0]} {results['multiple']['illumination'][i][1]}%"
        write_predictions(multiple, frame, (startX, startY, endX, endY), 2)

        multiple =  f"{results['multiple']['pose'][i][0]} {results['multiple']['pose'][i][1]}%"
        write_predictions(multiple, frame, (startX, startY, endX, endY), 3)

        multiple =  f"{results['multiple']['occlusion'][i][0]} {results['multiple']['occlusion'][i][1]}%"
        write_predictions(multiple, frame, (startX, startY, endX, endY), 4)

        multiple =  f"{results['multiple']['makeup'][i][0]} {results['multiple']['makeup'][i][1]}%"
        write_predictions(multiple, frame, (startX, startY, endX, endY), 5)

        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
    cv2.imshow('aa', frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    i+=1
    if time()-t>=1:
        print(f"fps {i}")
        i=0
        t = time()

cam.release()
cv2.destroyAllWindows()
```
dowload streamer module from [here](https://drive.google.com/file/d/12pYm0glhgC3ga1TjL3hGjlC9LLeo85IY/view?usp=sharing).

### Dowload Streamer & Install Requirements
dowload streamer module from [here](https://drive.google.com/file/d/12pYm0glhgC3ga1TjL3hGjlC9LLeo85IY/view?usp=sharing).
`$pip install python-opencv numpy`

## Other Languages

other languages packages will come soon you can feel free to check the python package behavior and build your own package using your favorite language
