# TYPES EACH HAVE DEFINITIONS WHICH INFORM APIs for INTERACTION

import numpy as np
from datetime import datetime
import itertools
import re
import sys
from sage.all import *

class tpPoint():
    
    def __init__(self, components = "",
                 label = ""):
        
        self.components = components
        self.label = label
        self.description = 'point'
        self.construction = None
        self.point_in_cartesian_form = None
        self.point_in_projective_form = None
        self.create_point()
        
    def convert_point_to_projective_point(self, point_list):
        initial_list = point_list
        lcden = denominator(sum(initial_list))
        normalised_list = [lcden * x for x in initial_list]
        normalised_list.insert(0, lcden)
        return(vector(normalised_list))

    
    def create_point(self):
        self.construction = vector(self.components)
        self.point_in_projective_form = self.convert_point_to_projective_point(self.components)
        

    def __repr__(self):
        return(str(self.point_in_projective_form))
    
    
class tpLine():
    
    #TO DO - need a line as n-proportion
    
    def __init__(self, components = "",
                 label = "",
                 parameters = "",
                 from_points = False):
        
        self.description = 'line'
        self.components = components
        self.label = label
        self.construction = None
        self.line_as_equation = None
        self.line_as_parametised_relationship = None
        self.from_points = from_points
        self.parameters = parameters
        self.create_line()


        
    def create_paramaterised_construction(self):
        self.parametised_construction = self.construction.dot_product(vector(self.parameters))
        

    def create_line(self):

        if self.from_points == True:
            point_list = self.components
            
            p1 = point_list[0]
            p2 = point_list[1]
            t1 = p1[1]* p2[2] - p1[2] * p2[1]
            t2 = p1[2]* p2[0] - p1[0] * p2[2]
            t3 = p1[0]* p2[1] - p1[1] * p2[0]
            
            self.construction = vector([t1,t2,t3])
            
            v = vector([1,1,1])
            
            self.line_as_parametised_relationship = self.construction.dot_product(v) == 0  
            
            
        else:

            l = vector(self.components)

            self.construction = l
            self.line_as_parametised_relationship = self.construction.dot_product(vector(self.parameters)) == 0     
            
        
        self.line_as_equation = self.construction[1] + self.construction[2] == -self.construction[0]


    def __repr__(self):
        return(str(self.construction))
        
        
class tpTriangle():
    ''' expects three points and will provide a matrix construction. if not available it will be just a a single vector'''
    
    def __init__(self, components = "", compose_from_points = True, label = ""):
        
        self.components = components
        self.label = label
        self.description = 'triangle'
        self.construction = None
        self.compose_from_points = compose_from_points
        self.create_triangle()

    
    def create_triangle(self):

        self.construction = matrix([self.components[0].point_in_projective_form, 
                                    self.components[1].point_in_projective_form, 
                                    self.components[2].point_in_projective_form])
        
    def __repr__(self):
        return(str(self.construction))
    
    
class tpSubstitution():
    def __init__(self, existing_components = [],
                       substitution = {},
                       label = ""):
        self.components = components
        self.label = label
        self.construction = None
        self.line_as_equation = None
        self.from_points = from_points
        self.create_substitution()


    def create_substitution(self):
        pass

    def __repr__(self):
        return(str(self.construction))
    
    
