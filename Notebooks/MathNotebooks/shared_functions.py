import numpy as np
import sympy as sp

def compute_cross_product_from_two_points(points_list):
    c = points_list[0][0] * points_list[1][1] - points_list[0][1] * points_list[1][0]
    return(c)

def compute_signed_area_from_two_points(points_list):
    c = compute_cross_product_from_two_points(points_list)
    signed_area = c / 2
    return(signed_area)

def compute_signed_area_using_meisters_formula(points_list, is_cyclic):

    total_signed_area = 0
    for each_point in range(len(points_list) - 1):
        signed_area = compute_signed_area_from_two_points([points_list[each_point], points_list[each_point + 1]])
        total_signed_area = total_signed_area + signed_area
    
    if is_cyclic:
        final_signed_area = compute_signed_area_from_two_points([points_list[-1], points_list[0]])
        total_signed_area = total_signed_area + final_signed_area
        
    return(total_signed_area)


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