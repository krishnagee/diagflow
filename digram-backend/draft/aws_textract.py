# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:17:16 2019

@author: kg900332
"""

import boto3
import os
import json
from fuzzywuzzy import process
from python_terraform import *
import os
from string import Template
# Document
documentName = "C:/Users/kg900332.PROD/Documents/diagflow/digram-backend/draft/processed.jpeg"

aws_cloud = Template('provider "aws" { \n\t version = "~> 2.0" \n\t region  = "us-east-1" \n\t access_key = "AKIAWE3ACI3UTB3W6MSI" \n\t secret_key = "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" \n\t profile = "$name" \n}\n')
aws_vpc = Template('resource "aws_vpc" "$name" { \n\t cidr_block = "10.0.0.0/16" \n}\n')
aws_eip = Template('resource "aws_eip" "$name" {\n vpc = true\n\t}\n')
aws_s3b = Template('resource "aws_s3_bucket" "$name" {\n\t bucket = "sample" \n\t}\n')
aws_ecs = Template('resource "aws_ecs_cluster" "$name" {\n\tname = "white-hart"\n\t}\n')
aws_ecr = Template('resource "aws_ecr_repository" "$name" {\n\tname = "white-hart"\n\t}\n')
aws_route53 = Template('resource "aws_route53_zone" "$name" {\n  name = "example.com"\n}\n')

aws_subnet = Template('resource "aws_subnet" "$name" { \n\t vpc_id     = "${aws_vpc.$vpc_name.id}" \n\tcidr_block = "10.0.0.0/16" \n\t}\n')
aws_ec2 = Template('resource "aws_instance" "$name" {\n\t ami = "ami-06d51e91cea0dac8d"\n\tinstance_type = "t2.micro"\n\t subnet_id = "${aws_subnet.$subnet_name.id}"\n}\n')
aws_sg = Template('resource "aws_security_group" "$name" {\n  name        = "$name"\n  description = "Allow TLS inbound traffic"\n  vpc_id      = "${aws_vpc.$vpc_name.id}"\n\n  ingress {\n    # TLS (change to whatever ports you need)\n    from_port   = 443\n    to_port     = 443\n    protocol    = "tcp"\n    # Please restrict your ingress to only necessary IPs and ports.\n    # Opening to 0.0.0.0/0 can lead to security vulnerabilities.\n    cidr_blocks = ["10.0.0.0/16"] \n  }\n\n  egress {\n    from_port       = 0\n    to_port         = 0\n    protocol        = "-1"\n    cidr_blocks     = ["0.0.0.0/0"]\n    prefix_list_ids = ["pl-12c4e678"]\n  }\n}\n')
aws_igw = Template('resource "aws_internet_gateway" "$name" {\n  vpc_id = "${aws_vpc.$vpc_name.id}"\n}\n')

aws_rds = Template('resource "aws_db_instance" "$name" {\n  allocated_storage    = 20\n  storage_type         = "gp2"\n  db_subnet_group_name = "$subnet_name"  \n  engine               = "mysql"\n  engine_version       = "5.7"\n  instance_class       = "db.t2.micro"\n  name                 = "mydb"\n  username             = "foo"\n  password             = "foobarbaz"\n  parameter_group_name = "default.mysql5.7"\n}\n')
aws_alb = Template('resource "aws_lb" "$name" {\n name = "alb-test"\n  internal = false\n  load_balancer_type = "application"\n  security_groups    = ["${aws_security_group.$sg_name.id}"]\n  subnets            = ["${aws_subnet.$subnet_name.id}"]\n}\n')
aws_nlb = Template('resource "aws_lb" "$name" {\n name = "nlb-test"\n  internal = false\n  load_balancer_type = "network"\n  security_groups    = ["${aws_security_group.$sg_name.id}"]\n  subnets            = ["${aws_subnet.$subnet_name.id}"]\n}\n')
aws_ngw = Template('resource "aws_nat_gateway" "$name" {\n  allocation_id = "${aws_eip.$eip_name.id}"\n  subnet_id     = "${aws_subnet.$subnet_name.id}"\n}\n')


dep0_aws_resource = {'aws_cloud','aws_vpc','aws_eip','aws_s3b','aws_ecs','aws_ecr','aws_route53'}

vpc_aws_resource = {'aws_subnet','aws_igw','aws_vpc_peer'}
sub_aws_resource = {'aws_sg','aws_ec2','aws_rds','aws_ngw','aws_rtab','aws_rt'}
sg_aws_resource = {'aws_alb','aws_nlb'}
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
keys = []
for line in lines:
    keys.append(line[1])    
#print(keys)    
cat_dict = {}

with open('C:/Users/kg900332.PROD/Documents/diagflow/digram-backend/draft/aws_vocab.json','r') as vocab:
    data = vocab.read()
json_object = json.loads(data)

for key in json_object.keys():
#    print("key: {0} | value: {1}".format(key,json_object[key]))
    for value in json_object[key]:
#        print("value: {0}".format(value))
        cat_dict[value]=key
        
tf_script_dict = {}    
tf_script = ''   
resource_dict= {}
#print(cat_dict.keys())
for key in keys:
    ##Using fuzzywuzzy to extract keywords based on pattern matches
    #
    value = process.extract(key,cat_dict.keys(),limit=1)[0][0]
    print(key,value,cat_dict[value])
    if (cat_dict[value] in tf_script_dict.keys()):
        tf_script_dict[cat_dict[value]]=tf_script_dict[cat_dict[value]]+1
    else:
        tf_script_dict[cat_dict[value]]=1

print(tf_script_dict)
tf_script=''
for key in tf_script_dict.keys():
    if (key in dep0_aws_resource):
        resource_dict[key]=[]
        for i in range(0,tf_script_dict[key]):
             tf_script=tf_script+ (vars()[key]).safe_substitute(name='main'+str(i))
             resource_dict[key].append('main'+str(i))
#            tf_script = tf_script+ (vars()key).safe_substitute(name='main'+i)

for key in tf_script_dict.keys():
    if (key in vpc_aws_resource):
        resource_dict[key]=[]
        for i in range(0,tf_script_dict[key]):
            tf_script=tf_script+ (vars()[key]).safe_substitute(
                    name='main'+str(i),vpc_name=resource_dict['aws_vpc'][0])
            resource_dict[key].append('main'+str(i))

for key in tf_script_dict.keys():
    if(key in sub_aws_resource):
       resource_dict[key]=[]
       for i in range(0,tf_script_dict[key]):
            tf_script=tf_script+(vars()[key]).safe_substitute(
                    name='main'+str(i),subnet_name=resource_dict['aws_subnet'][0])
            resource_dict[key].append('main'+str(i))           

for key in tf_script_dict.keys():
    if(key in sg_aws_resource):
       resource_dict[key]=[]
       for i in range(0,tf_script_dict[key]):
            tf_script=tf_script+(vars()[key]).safe_substitute(
                    name='main'+str(i),sg_name=resource_dict['aws_sg'][0],subnet_name=resource_dict['aws_subnet'][0])
            resource_dict[key].append('main'+str(i))  
            
print(tf_script)
print(resource_dict)

os.chdir('C:/Users/kg900332.PROD/Downloads/terraform')
main_tf = open('C:/Users/kg900332.PROD/Downloads/terraform/aws-project/project1/main.tf','w+')
main_tf.flush()
main_tf.write(tf_script)
main_tf.close()

tf = Terraform(working_dir='C:/Users/kg900332.PROD/Downloads/terraform')
return_code, stdout, stderr = tf.init('aws-project/project1')
print(return_code,stdout,stderr)

return_code, stdout, stderr = tf.plan('aws-project/project1')
print(return_code,stdout,stderr)
