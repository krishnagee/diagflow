# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:17:16 2019

@author: kg900332
"""

import boto3
import os

# Document
documentName = "C:/Users/kg900332.PROD/Downloads/aws-images/image20.jpg"

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

# Amazon Textract client
textract = boto3.client('textract',
                        aws_access_key_id='AKIAI5P5I6NGZTAMVDLA',
                        aws_secret_access_key='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',
                        region_name='eu-west-1',verify=False)

# Call Amazon Textract
response = textract.detect_document_text(Document={'Bytes': imageBytes})

#print(response)

# Detect columns and print lines
columns = []
lines = []
for item in response["Blocks"]:
      if item["BlockType"] == "LINE":
        column_found=False
        for index, column in enumerate(columns):
            bbox_left = item["Geometry"]["BoundingBox"]["Left"]
            bbox_right = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]
            bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]/2
            column_centre = column['left'] + column['right']/2

            if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                #Bbox appears inside the column
                lines.append([index, item["Text"]])
                column_found=True
                break
        if not column_found:
            columns.append({'left':item["Geometry"]["BoundingBox"]["Left"], 'right':item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
            lines.append([len(columns)-1, item["Text"]])

lines.sort(key=lambda x: x[0])
for line in lines:
    print (line[1])