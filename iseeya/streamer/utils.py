from collections import defaultdict
import numpy as np
import cv2
import torch
from torch.nn import functional as F
from iseeya.ai import from_face, trackers, detectors, transforms, from_face, trackers

def models_predictions(output, outputs, model_type):
    if model_type == "gender":
        preds = []
        for out in output:
            out = out.view(-1)
            out = F.softmax(out, 0)
            pred = torch.argmax(out)
            acc = int(out[pred] * 100.)
            label = f"{['Female', 'Male'][pred]}"
            preds.append([label, acc])

    if model_type == "expression":
        preds = []
        for out in output:
            out = out.view(-1)
            out = F.softmax(out, 0)
            pred = torch.argmax(out)
            acc = int(out[pred] * 100.)
            label = f"{['ANGER', 'DISGUST', 'FEAR', 'HAPPINESS', 'NEUTRAL', 'SADNESS', 'SURPRISE'][pred]}"
            preds.append([label, acc])

    if model_type == "multiple":
        labels = [['BAD','HIGH','MEDIUM'],
                ['DOWN','FRONTAL','LEFT','RIGHT','UP'],
                ['BEARD','GLASSES','HAIR','HAND','NONE','ORNAMENTS','OTHERS',],
                ['Middle', 'Old', 'Young'],
                ['OVER','PARTIAL']]
        models = ["illumination","pose","occlusion","age","makeup"]
        preds = defaultdict(list) 
        for i in range(len(output)):
            for out in output[i]:
                out = out.view(-1)
                out = F.softmax(out, 0)
                pred = torch.argmax(out)
                acc = int(out[pred] * 100.)
                label = f"{labels[i][pred]}"
                preds[models[i]].append([label, acc])      
    outputs[model_type]= preds
    return outputs


def get_outputs(image, opts):
    
   
    outputs = defaultdict(list)
    if 'face' in opts['detectors']:
        outputs['faces'] = detectors['face_detection'](image)
        boxes = outputs['faces']
    faces = []
    for i in range(boxes.shape[0]):
        (startX, startY, endX, endY) = boxes[i]
        face = image[startY:endY, startX:endX]
        face = cv2.resize(face, (64,64))
        face = transforms(face)
        face = face.unsqueeze(0)
        faces.append(face)
    if faces:
        faces = torch.cat(faces) 
        
        for face_opt in opts['from_face']:
            
            output = from_face[face_opt](faces)
            outputs = models_predictions(output, outputs, face_opt)
    return outputs
