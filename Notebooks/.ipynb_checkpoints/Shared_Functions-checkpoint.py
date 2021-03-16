# There are some better functions in Sympy and Sage to do this, but we want to keep things as simple as possible for te moment
def calculate_cross_product(v1, v2):
    return(v1[0] * v2[1] - v1[1]*v2[0])



def calculate_signed_area(points, origin_is_one_of_points = True):
    if origin_is_one_of_points:
        area = points[1][0] * points[2][1] - points[1][1] * points[2][0]
    else:
        area = points[0][0] * points[1][1] - points[0][1] * points[1][0]
    return((area/2).factor())




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