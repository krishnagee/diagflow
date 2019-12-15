# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 14:40:18 2019

@author: kg900332
"""

from python_terraform import *
import os

from string import Template

aws_cloud = 'provider "aws" { \n\t version = "~> 2.0" \n\t region  = "us-east-1" \n\t access_key = "AKIAWE3ACI3UTB3W6MSI" \n\t secret_key = "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" \n}\n'
aws_vpc1 = 'resource "aws_vpc" "main" { \n\t cidr_block = "10.0.0.0/16" \n}\n'
aws_subnet = 'resource "aws_subnet" "example" { \n\t vpc_id     = "${aws_vpc.main.id}" \n\tcidr_block = "10.0.0.0/16" \n\t}\n'
aws_rds = 'resource "aws_db_instance" "default" {\n  allocated_storage    = 20\n  storage_type         = "gp2"\n  db_subnet_group_name = "example"  \n  engine               = "mysql"\n  engine_version       = "5.7"\n  instance_class       = "db.t2.micro"\n  name                 = "mydb"\n  username             = "foo"\n  password             = "foobarbaz"\n  parameter_group_name = "default.mysql5.7"\n}\n'
aws_sg = 'resource "aws_security_group" "allow_tls" {\n  name        = "allow_tls"\n  description = "Allow TLS inbound traffic"\n  vpc_id      = "${aws_vpc.main.id}"\n\n  ingress {\n    # TLS (change to whatever ports you need)\n    from_port   = 443\n    to_port     = 443\n    protocol    = "tcp"\n    # Please restrict your ingress to only necessary IPs and ports.\n    # Opening to 0.0.0.0/0 can lead to security vulnerabilities.\n    cidr_blocks = ["10.0.0.0/16"] \n  }\n\n  egress {\n    from_port       = 0\n    to_port         = 0\n    protocol        = "-1"\n    cidr_blocks     = ["0.0.0.0/0"]\n    prefix_list_ids = ["pl-12c4e678"]\n  }\n}\n'
aws_vpc2 = 'resource "aws_vpc" "example" { \n\t cidr_block = "10.1.0.0/16" \n}\n'
aws_vpc_peering = 'resource "aws_vpc_peering_connection" "foo" {\n peer_vpc_id   = "${aws_vpc.example.id}"\n  vpc_id        = "${aws_vpc.main.id}"\n\n  accepter {\n    allow_remote_vpc_dns_resolution = true\n  }\n\n  requester {\n    allow_remote_vpc_dns_resolution = true\n  }\n}\n'

#aws_vpn_connection = 'resource "aws_vpn_connection" "main" {\n  vpn_gateway_id      = "${aws_vpn_gateway.vpn_gateway.id}"\n  customer_gateway_id = "${aws_customer_gateway.customer_gateway.id}"\n  type                = "ipsec.1"\n  static_routes_only  = true\n}\n'
#aws_vpn_gateway = 'resource "aws_vpn_gateway" "vpn_gateway" {\n  vpc_id = "${aws_vpc.vpc.id}"\n}\n'
#aws_customer_gateway = 'resource "aws_customer_gateway" "main" {\n  bgp_asn    = 65000\n  ip_address = "172.83.124.10"\n  type       = "ipsec.1"\n}\n'

aws_alb = 'resource "aws_lb" "alb1" {\n name = "alb-test"\n  internal = false\n  load_balancer_type = "application"\n  security_groups    = ["${aws_security_group.allow_tls.id}"]\n  subnets            = ["${aws_subnet.example.id}"]\n}\n'
aws_nlb = 'resource "aws_lb" "nlb1" {\n name = "nlb-test"\n  internal = false\n  load_balancer_type = "network"\n  security_groups    = ["${aws_security_group.allow_tls.id}"]\n  subnets            = ["${aws_subnet.example.id}"]\n}\n'
aws_igw = 'resource "aws_internet_gateway" "igw" {\n  vpc_id = "${aws_vpc.main.id}"\n}\n'
aws_eip = 'resource "aws_eip" "nat" {\n vpc = true\n\t}\n'
aws_ngw = 'resource "aws_nat_gateway" "ngw" {\n  allocation_id = "${aws_eip.nat.id}"\n  subnet_id     = "${aws_subnet.example.id}"\n}\n'
aws_s3b = 'resource "aws_s3_bucket" "mybucket" {\n\t bucket = "sample" \n\t}\n'
aws_ecs = 'resource "aws_ecs_cluster" "ecserv" {\n\tname = "white-hart"\n\t}\n'
aws_ecr = 'resource "aws_ecr_repository" "ecrepo" {\n\tname = "white-hart"\n\t}\n'
aws_ec2 = 'resource "aws_instance" "server" {\n\t ami = "ami-06d51e91cea0dac8d"\n\tinstance_type = "t2.micro"\n}\n'
aws_route53 = 'resource "aws_route53_zone" "primary" {\n  name = "example.com"\n}\n'
aws_rtab = 'resource "aws_route_table" "rt" {\n  vpc_id = "${aws_vpc.main.id}"\n route {\n cidr_block = "10.0.1.0/24"\n   gateway_id = "${aws_internet_gateway.igw.id}"\n}\n}\n'
aws_rt = 'resource "aws_route" "r" {\n  route_table_id = "${aws_route_table.rt.id}" \n  destination_cidr_block    = "10.0.1.0/22"\n  vpc_peering_connection_id = "${aws_vpc_peering_connection.foo.id}"\n depends_on                = ["aws_route_table.rt"]\n}\n'

os.chdir('C:/Users/kg900332.PROD/Downloads/terraform')
main_tf = open('C:/Users/kg900332.PROD/Downloads/terraform/aws-project/project1/main.tf','w+')
output_tf = open('C:/Users/kg900332.PROD/Downloads/terraform/aws-project/project1/output.tf','w')
main_tf.flush()
main_tf.write(aws_cloud+aws_vpc1+aws_subnet+aws_rds+aws_sg+aws_vpc2+aws_vpc_peering+
              aws_alb+aws_nlb+aws_igw+aws_eip+aws_ngw+aws_s3b+aws_ecs+
              aws_ecr+aws_ec2+aws_route53+aws_rtab+aws_rt)
main_tf.close()

tf = Terraform(working_dir='C:/Users/kg900332.PROD/Downloads/terraform')
return_code, stdout, stderr = tf.init('aws-project/project1')

print(return_code,stdout,stderr)

return_code, stdout, stderr = tf.plan('aws-project/project1')

print(return_code,stdout,stderr)