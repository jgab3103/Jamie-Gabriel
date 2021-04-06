import numpy as np
from datetime import datetime
import itertools
import re
import sys
from sage.all import *

# should be with line as should type restrictions
def get_slope_of_projective_line(projective_line):
    normalised_vector = projective_line / projective_line[2]
    slope = -normalised_vector[1]
    return(slope)


# In[3]:


def set_up_if_condition(if_data = [],
                        then_data = []):
    condition_dict = {}
    condition_dict['if'] = if_data[0]
    for i in range(len(then_data)):
        condition_dict["then_" + str(i)] = then_data[i]

    return(condition_dict)




def get_distance_between_2_points(point_1, point_2):
    '''
    Returns a symbolic expression of the distance between 2 tpPoints

            Parameters:
                    components (list): list of 2 elements of tpPoint

            Returns:
                    expression (sage expression): expression of components in a perpendicular relationship
    '''
    point_1 = point_1[1:] / point_1[0]
    point_2 = point_2[1:] / point_2[0]
    sum = 0
    for i in range(len(point_1)):
        sum = sum + (point_1[i] - point_2[i]) ** 2

    return(sqrt(sum.full_simplify()))
