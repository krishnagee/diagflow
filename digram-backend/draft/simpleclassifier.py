# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:51:14 2019

@author: kg900332
"""

import numpy as np
from model_server import Servable
from model_server import server_pb2_grpc


class my_custom_servable(Servable):
    def __init__(self, args):
        # args contains values from ArgumentParser
        # Thus you can pass any kwargs via command line and you get them here
        pass

    def predict(self, input_array_dict):
        """This method is responsible for the gRPC call GetPredictions().
        All custom servables must define this method.

        Arguments:
            input_array_dict (dict): The PredictionRequest proto decoded as a python dictionary.

        # example
        input_array_dict = {
                           "input_tensor_name1": numpy array,
                           "input_tensor_name2": numpy array
                            }

        Returns:
            A python dictionary with key (typically output name) and value as numpy array of predictions

        # example
        output = {
                   "output_tensor_name1": numpy array,
                   "output_tensor_name2": numpy array
                  }
        """
        print(input_array_dict)
        return ({"output_array1": np.array([100, 200]).astype(np.float32),
                 "output_array2": np.array(["foo".encode(),"bar".encode()]).astype(object),  # you can get and pass strings encoded as bytes also
                 })

    def get_model_info(self, list_of_model_info_dict):
        """This method which is responsible for the call GetModelInfo()

        Arguments:
            list_of_model_info_dict (list/tuple): A list containing model_info_dicts

        Note:
            model_info_dict contains the following keys:

            {
                "name": "model name as string"
                "version": "version as string"
                "status": "status string"
                "misc": "string with miscellaneous info"
            }

        Returns:
            list_of_model_info_dict (dict): containing the model and server info. This is similar to the function input
        """
        return [{"name": "first_model", "version": 1, "status": "up"},
                {"name": "second_model", "version": 2, "status": "up", "misc": "Other miscellaneous details"}]