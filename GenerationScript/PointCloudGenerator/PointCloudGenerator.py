import random 
import numpy as np
import math
import csv

radius = 15
random_delta_position = 1.0
#Quaternion, from -1 to 1
random_rotation = [1.0, 1.0, 1.0, 1.0]
random_scale = [0.25, 2.0]
maxSavedPoints = 20000;
animations_number = 10
animation_speed_brackets = [0.25, 1.75]

"""  
Generating Cloud i need to limit space for generation. generation_interations defines how many FULL orbs will be generated to fill cube of edge size equal to
generation_interations*radius
"""

generation_maxDistance = 500
generation_limit_Cube = [generation_maxDistance, generation_maxDistance, generation_maxDistance, generation_maxDistance]

#width = x, depth = y, height = z  =>  its unreal engine standard 
class Transform:
    #x,y,z,w
    rotation = [0.0, 0.0, 0.0, 0.0]
    
    position = [0.0, 0.0, 0.0]
    scale = [0.0, 0.0, 0.0]
    
    def __init__(self, pos: list, rot: list, sc: list):
        self.position=pos
        self.rotation = rot
        self.scale = sc
        
    def get_data_as_list(self):
        returnlist = []
        returnlist.extend(self.position)
        returnlist.extend(self.rotation)
        returnlist.extend((self.scale))
        return returnlist
        

class PointProps:
    transform = Transform([0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0])
    animationId = 0
    animationSpeed = 1.0
    
    def __init__(self, transf: Transform, animID: int, animSpeed: float):
        self.transform = transf
        self.animationId = animID
        self.animationSpeed = animSpeed
    
    def get_data_as_list(self):
        returnlist = []
        returnlist.extend(self.transform.get_data_as_list())
        returnlist.append(self.animationId)
        returnlist.append((self.animationSpeed))
        return returnlist
    
class Cloud:
    Points = []
    Radius = 0.0
    def __init__(self):
        print("Robie generacje")
        Cloud.__GenerateCloud(self)
        print("done")
        
        
    
    def generate_points_of_orb(orb_radius: float):
        #perimeter of "circle" on orb
        number_of_points = 0
        perimeter = 2*math.pi*orb_radius
        points_on_height = math.floor(perimeter/radius)
        #print("Points on Height: "+ str(points_on_height))
        delta_rad = 2*math.pi/(points_on_height)
        points = list()
        #i means iteration on height, +1 becouse we have to count mirrored first point
        for i in range(math.floor(points_on_height/2)+1):
            
            height = math.cos(delta_rad*i)*orb_radius
            sub_radius = math.sin(delta_rad*i)*orb_radius
            if(abs(sub_radius) > math.pow(10.0, -6.0)):
                sub_perimeter = 2*math.pi*sub_radius 
                points_on_sub_perimeter = math.floor(sub_perimeter/radius)
                sub_delta_rad =  2*math.pi/points_on_sub_perimeter
                #print("Points on "+str(i)+" cicrcle: "+ str(points_on_sub_perimeter))
                for k in range(points_on_height):
                    width = sub_radius*math.sin(k*sub_delta_rad)
                    depth = sub_radius*math.cos(k*sub_delta_rad)
                    points.append([width, depth, height])
                    number_of_points += 1
            else:
                width = 0.0
                depth = 0.0
                #print("Points on "+str(i)+" cicrcle: 1")
                points.append([width, depth, height])
                number_of_points += 1
                      
        """
        print("\n __________________________________\n")
        #print(points)
        p0 = points[4500]
        count = 0
        for i in points:
            dst = math.sqrt( math.pow(p0[0] - i[0],2) +math.pow(p0[1] - i[1],2)+math.pow(p0[2] - i[2],2))
            
            if(dst <= 7.4):
                print(i, dst)
                count +=1
        print(count)
        """ 
        return points, number_of_points
    
    def __GenerateCloud(self):
        iterationRadious = radius
        saved_in_current_iteration = []
        saved_points = 0
        while True:
            saved_points_in_iteration = 0
            gen_points, num_points = Cloud.generate_points_of_orb(iterationRadious)
            saved_in_current_iteration.clear()
            for i in gen_points:
                if(Cloud.is_point_in_cube(i)):
                    pos = [i[0]+random.uniform(-random_delta_position, random_delta_position), i[1]+random.uniform(-random_delta_position, random_delta_position),i[2]+random.uniform(-random_delta_position, random_delta_position)]
                    temporaryPoitProps = PointProps(Transform(pos, self._genearte_rotation(), self._generate_scale()), self._generate_animationIndex(), self._generate_animation_speed())
                    saved_in_current_iteration.append(temporaryPoitProps)
                    saved_points_in_iteration +=1
            
            iterationRadious += radius
            saved_points +=saved_points_in_iteration
            self.Points.extend(saved_in_current_iteration)
            self.Radius = iterationRadious
            if(saved_points_in_iteration==0 or maxSavedPoints <=saved_points or generation_limit_Cube[0]*math.sqrt(2) < iterationRadious):
                break
            print("Progress; " + str(100*iterationRadious/(math.sqrt(2)*generation_limit_Cube[0])) + " iteration radius: " + str(iterationRadious))
            print(saved_points)
                
                
                
    def is_point_in_cube(point: [float, float, float]):
        return (point[0] >= -generation_limit_Cube[0]) and (point[0] <= generation_limit_Cube[0]) and (point[1] >= -generation_limit_Cube[1]) and (point[1] <= generation_limit_Cube[1]) & (point[2] >= -generation_limit_Cube[2]) and (point[2] <= generation_limit_Cube[2])
    
    def _genearte_rotation(self):
        return [random.uniform(-random_rotation[0], random_rotation[0]), random.uniform(-random_rotation[1], random_rotation[1]),random.uniform(-random_rotation[2], random_rotation[2]),random.uniform(-random_rotation[3], random_rotation[3])]      
    def _generate_scale(self):
        return [random.uniform(random_scale[0], random_scale[1]),random.uniform(random_scale[0], random_scale[1]),random.uniform(random_scale[0], random_scale[1])]
    def _generate_animationIndex(self):
        return random.randint(0,animations_number)
    def _generate_animation_speed(self):
        return random.uniform(animation_speed_brackets[0], animation_speed_brackets[1])
    
    def get_pointCloud(self):
        return self.Points
    def get_Radius(self):
        return self.Radius
    

pointsGenerator = Cloud()
generatedPoints = pointsGenerator.get_pointCloud()
radius = pointsGenerator.get_Radius()
row = ["lp", "positionX", "positionY", "positionZ", "quatRotX","quatRotY","quatRotZ","quatRotW","scaleX","scaleY","scaleZ","animID","animationTime", str(radius)]
index = 1
with open('points.csv', 'w', newline='', encoding='UTF8') as f:
    write = csv.writer(f)
    write.writerow(row)
    for i in generatedPoints:
        temp = i.get_data_as_list()
        temp.insert(0, index)
        write.writerow(temp)
        index+=1