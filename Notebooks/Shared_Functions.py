import numpy as np
import sympy as sp

def compute_vector_from_2_points(points_list):
    v = np.array([points_list[1][0] - points_list[0][0], points_list[1][1] - points_list[0][1]])
    return(v)
             
def compute_cross_product_from_two_vectors(vector_list):
    c = vector_list[0][0] * vector_list[1][1] - vector_list[0][1] * vector_list[1][0]
    return(c)

def compute_signed_area_of_triangle_from_two_vectors(vector_list):
    c = compute_cross_product_from_two_vectors(vector_list)
    signed_area = c / 2
    return(signed_area)



# and recall that for colinearity, 
# cross product = 0
def test_for_collinearity(points):
    
    current_slope = (points[1][1] - points[0][1]) / (points[1][0] - points[0][0])
    points_are_collinear = False
    
    for i in range(len(points)):
        
        if len(points[i:]) <= 1:
            return(points_are_collinear)
        else:
            
            p2 = points[i + 1]
            p1 = points[i]
            slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
            points_are_collinear = slope == current_slope
            

   
    
# iterate and determine slope