# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:38:11 2019

@author: kg900332
"""

import numpy as np
from keras.preprocessing import image
test_image = image.load_img('C:/Users/kg900332.PROD/Downloads/aws-images/aws_new/image1.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
training_set.class_indices

if result[0][0] == 1:
    prediction = 'dog'
else:
    prediction = 'cat'