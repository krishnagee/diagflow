# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:52:12 2019

@author: kg900332
"""

import grpc
import numpy as np

from model_server import server_pb2, server_pb2_grpc
from model_server.utils import create_tensor_proto
from model_server.utils import create_predict_request
from model_server.utils import create_array_from_proto
from model_server.utils import create_model_info_proto

channel = grpc.insecure_channel('localhost:5001')  # default port
# create a stub (client)
stub = server_pb2_grpc.ModelServerStub(channel)
input_array_dict = {"input1":create_tensor_proto(np.array([1,2]).astype(np.uint8)),
                    "input2":create_tensor_proto(np.array([[10.0,11.0], [12.0,13.0]]).astype(np.float32)),
                    "input3":create_tensor_proto(np.array(["Hi".encode(), "Hello".encode(), "test".encode()]).astype(object))
                   }
# create the prediction request
predict_request= create_predict_request(input_array_dict, name="simple_call")
# make the call
response = stub.GetPredictions(predict_request)

# decode the response
print(create_array_from_proto(response.outputs["output_array1"]))

# prints: array([100., 200.], dtype=float32)

# Getting the model status

model_info_proto = create_model_info_proto([])  # you can pass an empty list also
response = stub.GetModelInfo(model_info_proto)