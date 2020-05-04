import os
from collections import defaultdict
import numpy as np
import torch
from torch.nn import functional as F
from flask import current_app
from iseeya.ai.utils import load_models, ct, transforms

models_path ='./iseeya/ai/models'
gender, expression, multiple, face_detection = load_models(models_path)

from_face = {
    "gender":gender,
    "expression":expression,
    "multiple":multiple,
}
trackers = {
    "ct":ct
}
detectors = {
    "face_detection":face_detection
}







# def models_predictions(output, outputs, model_type):
#     if model_type == "gender":
#         output = output.view(-1)
#         output = F.softmax(output, 0)
#         pred = torch.argmax(output)
#         acc = int(output[pred] * 100.)
#         label = f"{['Female', 'Male'][pred]}"
#         preds = [label, acc]

#     if model_type == "expression":
#         output = output.view(-1)
#         output = F.softmax(output, 0)
#         pred = torch.argmax(output)
#         acc = int(output[pred] * 100.)
#         print(pred)
#         label = f"{['ANGER', 'DISGUST', 'FEAR', 'HAPPINESS', 'NEUTRAL', 'SADNESS', 'SURPRISE'][pred]}"
#         preds = [label, acc]

#     if model_type == "multiple":
#         labels = [['BAD','HIGH','MEDIUM'],
#                 ['DOWN','FRONTAL','LEFT','RIGHT','UP'],
#                 ['BEARD','GLASSES','HAIR','HAND','NONE','ORNAMENTS','OTHERS',],
#                 ['Middle', 'Old', 'Young'],
#                 ['OVER','PARTIAL']]
#         models = ["illumination","pose","occlusion","age","makeup"]
#         preds = defaultdict(list) 
#         for i in range(len(output)):
#             out = output[i]
#             out = out.view(-1)
#             out = F.softmax(out, 0)
#             pred = torch.argmax(out)
#             acc = int(out[pred] * 100.)
#             label = f"{labels[i][pred]}"
#             preds[models[i]].append([label, acc])      
#     outputs[model_type] = preds
#     return outputs


# def get_outputs(image, opts):
#     outputs = {}
#     if 'face' in opts['detectors']:
#         outputs['faces'] = detectors['face_detection'](image)
#         boxes = outputs['faces']

#     print(boxes.shape)

#     faces = []
#     for i in range(boxes.shape[0]):
#         (startX, startY, endX, endY) = boxes[i]
#         face = image[startY:endY, startX:endX]
#         face = cv2.resize(face, (64,64))
#         face = transforms(face)
#         face = face.unsqueeze(0)
#         faces.append(face)
#     if faces:
#         faces = torch.cat(faces) 
        
#         for face_opt in opts['from_face']:
            
#             output = from_face[face_opt](faces)
#             outputs = models_predictions(output, outputs, face_opt)
#     return outputs




# # @streamer.on('forward')
# def forward(data):
#     token = data.get('token')
#     inputs = data.get('inputs')
#     opts = data.get('opts')

#     # if User.verify_reset_token(token):
#     return get_outputs(inputs, opts)
#         # emit('reciver', outputs, namespace='/')
#     # else:
#         # emit('reciv/er', "invalid token", namespace='/')











# import cv2
# import imutils


# camera = cv2.VideoCapture(0)

# frame_width = int(camera.get(3))
# frame_height = int(camera.get(4))

# while True:

#     (ret, frame) = camera.read()
    
#     if not ret: 
#         break

#     frame = imutils.resize(frame, width=400)

#     d = {
#         "inputs":frame,
#         "opts":{
#             "detectors":["face"],
#             "from_face":["gender",'expression'],
#             "labels":{
#                 "gender":['Female', 'Male'],
#                 "expression":['ANGER', 'DISGUST', 'FEAR', 'HAPPINESS', 'NEUTRAL', 'SADNESS', 'SURPRISE']
#             }
#         }

#     }

#     print(forward(d))
    

    
#     cv2.imshow("Faces", frame)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# camera.release()
# cv2.destroyAllWindows()

