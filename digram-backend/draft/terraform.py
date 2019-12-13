# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 14:40:18 2019

@author: kg900332
"""

from python_terraform import *
import os

from string import Template

aws_provider = 'provider "aws" { \n\t version = "~> 2.0" \n\t region  = "us-east-1" \n\t access_key = "AKIAWE3ACI3UTB3W6MSI" \n\t secret_key = "aRgDOUDGEJLKgT1eYwwgXxuH6DBhoV4SSBbHncAv" \n}'
aws_vpc = 'resource "aws_vpc" "main" { \n\t cidr_block = $cidr \n}'
aws_subnet = 'resource "aws_subnet" "example" { \n\tvpc_id     = "${aws_vpc.default.id}" \n\tcidr_block = $cidr \n\ttags = {\n\tName = $name\n\t}\n\t}'
aws_s3_bucket = 'resource "aws_s3_bucket" "mybucket" {\n\t bucket = $name \n\t}\n'
aws_ecs = 'resource "aws_ecs_cluster" "foo" {\n\tname = "white-hart"\n\t}'

os.chdir('C:/Users/kg900332.PROD/Downloads/terraform')
os.mkdir('aws-project/project1')


tf = Terraform(working_dir='C:/Users/kg900332.PROD/Downloads/terraform')
return_code, stdout, stderr = tf.init('aws-project/project')

print(return_code,stdout,stderr)

return_code, stdout, stderr = tf.plan('aws-project/project')

print(return_code,stdout,stderr)