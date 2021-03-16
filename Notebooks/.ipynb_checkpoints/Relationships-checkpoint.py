# IMPLICATION -----------------------------------------------------------------------
import numpy as np
from datetime import datetime
import itertools
import re
import sys
from sage.all import *
import Utilities as ut

# Verifications -----------------------------------------------------------------
def evaluate_distinct_relationship(components = [],
                                   relationship_expectation = True):
    
    #     # for lines means no solutions
#     # ax + by = c, ax + by = k
#     # k != c

    if type(components[0]) != type(components[1]):
        print("CANNOT BE COMPARED")
        return

    # if they are distinct
    if components[0].construction != components[1].construction:
        return(True)
    else:
        return(False)


def create_relationship_implications(components):
    pass



# Relationships --------------------------------------------------------------
def create_perpendicularity_relationship(components = [],
                                         relationship_type_to_be_created = True):

    l1_slope = ut.get_slope_of_projective_line(components[0])
    l2_slope = - 1 / ut.get_slope_of_projective_line(components[1])
    return(l1_slope == l2_slope)



def create_parallel_relationship(components = [],
                                relationship_type_needed = True):
    
    implications = []

    m = matrix([components[0][1:], components[1][1:]])
    
    if relationship_type_needed == True:
        d = matrix([components[0][1:], components[1][1:]]).det() == 0
        imp1 = [[m[0][0] == 0],[m[1][1] != 0,m[0][1] != 0, m[1][0] == 0]]
        imp2 = [[m[0][0] != 0],[m[1][1] == 0,m[0][1] == 0, m[1][0] != 0]]

        implications.extend([imp1, imp2])
        
    else:
        d = matrix([components[0][1:], components[1][1:]]).det() != 0
        imp1 = [[m[0][1] == 0],[m[0][0] != 0, m[1][1] != 0]]
        imp2 = [[m[1][0] == 0],[m[0][0] != 0, m[1][1] != 0]]
        imp3 = [[m[0][0] == 0],[m[0][1] != 0, m[1][0] != 0]]
        imp4 = [[m[1][1] == 0],[m[0][1] != 0, m[1][0] != 0]]
        implications.extend([imp1, imp2, imp3, imp4])
        

    


    d_as_string = str(d)


    return([d, implications])




def create_incidence_relationship(components = [],
                                  relationship_type_to_be_created = True):

    result = components[0].dot_product(components[1]) == 0
    return(result)

