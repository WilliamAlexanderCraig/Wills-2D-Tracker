#William Craig's 2d Tracker
#Made for IB DP Maths SL IA in Python and PyGame

#importing needed modules and packages
import pygame
import math #if only it were that easy :( 
import random
import keyboard

#initialising pygame
pygame.display.init()
pygame.font.init()

#setting the width and height of the window
display_width = 1000   
display_height = 750

#configuring the display
display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Wills 2d Tracker")

#colour definitions as RGB values
white = (255,255,255)
black = (0,0,0)
grey = (100,100,100)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (255,200,200)
purple = (167, 66, 244)
orange = (255, 178, 0)

#object varables 
standard_object_size = 10
double_object_distance = 50

#some variables for animating the camera *DONT WORRY ABOUT THES
cam_fov_step = 3
cam_rot_step = 3
cam_move_step = 3


#FUNCTION STACK 
#function that makes an object at x, y with colour col when called 
def print_controls_title():
    #print the text
    draw_text("Wills 2D Tracker", (0,0), 50)
    draw_text("Controls:", (0,display_height-120),20)
    draw_text("R and T to change object rotation", (0,display_height-100), 20)
    draw_text("Z and X activate cameras", (0,display_height-80),20)
    draw_text("U and I change Radius", (0,display_height-60),20)
    draw_text("N and M change FOV", (0,display_height-40),20)
    draw_text("J and K change Rotation", (0,display_height-20),20)

def make_single_object (x, y, col):
    pygame.draw.circle(display, col, (int(x), int(y)), standard_object_size)




#making the needed object for drawing text on screen
def text_objects(text,font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()

#drawing the text on screen
def draw_text(text, pos, size):
    text_font = pygame.font.SysFont('Arial', size, False, False)
    Text_Surface, Text_Rect = text_objects(text, text_font)
    Text_Rect = pos
    display.blit(Text_Surface,Text_Rect)

#CLASS STACK
#class of camera
class camera:
    #function which is called at initialisation
    def __init__(self, cam_name, cam_x, cam_y, cam_degree_fov, cam_degree_rot, cam_activated, radius):
        self.this_cam_name = cam_name
        self.this_cam_x = cam_x
        self.this_cam_y = cam_y
        self.this_cam_degree_fov = cam_degree_fov
        self.this_cam_degree_rot = cam_degree_rot
        self.this_cam_activated = cam_activated
        self.this_cam_radius = radius

    #function that draws the entire camera and deals with controls
    def draw(self):
        draw_text(self.this_cam_name, (self.this_cam_x,self.this_cam_y), 20)
        
        #use the PARAMETRIC EQUATION TO FIND THE POINT ON A CIRCLE ****VERY IMPORTANT*** GOOGLE IT 
        #drawing the camera
        if (self.this_cam_activated):
            pygame.draw.circle(display, green, (int(self.this_cam_x),int(self.this_cam_y)), standard_object_size)
        else:  
            pygame.draw.circle(display, grey, (int(self.this_cam_x),int(self.this_cam_y)), standard_object_size)
        
        #limiting the fov to 180 degrees
        if (self.this_cam_degree_fov > 180):
            self.this_cam_degree_fov = 180

        #controls
        if(self.this_cam_activated):
            draw_text("Activated: " + self.this_cam_name, (0,50), 20)

            #change the radius
            if (keyboard.is_pressed('u')):
                self.this_cam_radius += 3
            if (keyboard.is_pressed('i')):
                self.this_cam_radius -= 3

            #changing the fov
            #if the "n" key on the keyboard is pressed
            if(keyboard.is_pressed('n')):
                #then make the fov wider
                self.this_cam_degree_fov += cam_fov_step 
        
            #if the 'm' key on the keyboard is pressed
            if(keyboard.is_pressed('m')):
                #then make the fov narrower
                self.this_cam_degree_fov -= cam_fov_step

            #changing the rotation
            #if the "n" key on the keyboard is pressed
            if(keyboard.is_pressed('j')):
                #then make the fov wider
                self.this_cam_degree_rot += cam_rot_step
        
            #if the 'm' key on the keyboard is pressed
            if(keyboard.is_pressed('k')):
                #then make the fov narrower
                self.this_cam_degree_rot -= cam_rot_step

            #changing the x and y
            if(keyboard.is_pressed('w')):
                self.this_cam_y-= cam_move_step
            if(keyboard.is_pressed('s')):
                self.this_cam_y += cam_move_step
            if(keyboard.is_pressed('a')):
                self.this_cam_x -= cam_move_step
            if(keyboard.is_pressed('d')):
                self.this_cam_x += cam_move_step

        #drawing the fov lines
        #the equation of a circle is r = sqrt((x-a)^2 + (y-b)^s)
        #the equation of a point on the circle is (x,y) = (a+r*cos(t), b+r*sin(t)) where t is the rotation in rads
        ray_lengths = 1000
        #convert degree_rot to rad_rot
        rad_rot = (self.this_cam_degree_rot*math.pi)/180
        #calculating the point that the camera is looking at
        #camera_direction = (x + ray_lengths* math.cos(rad_rot), y + ray_lengths* math.sin(rad_rot))
        #drawing the center line of the camera
        #pygame.draw.line(display, red, (x,y), camera_direction, 2)
        
        #drawing the fov lines
        #convert degree_fov to rads
        rad_fov = (self.this_cam_degree_fov*math.pi)/180 
        #calculating the negative point 
        negative_fov_direction = (self.this_cam_x + ray_lengths* math.cos(rad_rot-(rad_fov/2)), self.this_cam_y + ray_lengths* math.sin(rad_rot-(rad_fov/2)))
        #drawing the negative point
        pygame.draw.line(display, green, (self.this_cam_x,self.this_cam_y), negative_fov_direction, 2)
        #calculating the positive point 
        positive_fov_direction = (self.this_cam_x + ray_lengths* math.cos(rad_rot+(rad_fov/2)), self.this_cam_y + ray_lengths* math.sin(rad_rot+(rad_fov/2)))
        #drawing the positive point
        pygame.draw.line(display, green, (self.this_cam_x,self.this_cam_y), positive_fov_direction, 2)
        
        #drawing the pink triangle for estimating distance
        points = [(self.this_cam_x,self.this_cam_y),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot-(rad_fov/2)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot-(rad_fov/2))), 
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot-(rad_fov/4)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot-(rad_fov/4))),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot)),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot+(rad_fov/4)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot+(rad_fov/4))),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot+(rad_fov/2)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot+(rad_fov/2)))
        ]
        pygame.draw.lines(display, pink, True, points, 2)

        #drawing a line between every object and the camera (the colourful ones)
        for d_object in double_objects:
            cam_pos = (self.this_cam_x, self.this_cam_y)
            object_1_pos = (d_object.object_1_x, d_object.object_1_y)
            object_2_pos = (d_object.object_2_x, d_object.object_2_y)
            pygame.draw.line(display, d_object.this_object_col1, object_1_pos, cam_pos, 2)
            pygame.draw.line(display, d_object.this_object_col2, object_2_pos, cam_pos, 2)

        
        

class double_object:
    #function that is called when initalised 
    def __init__(self, object_name, object_x, object_y, object_degree_rot, object_col1, object_col2):
        self.this_object_name = object_name
        self.this_object_x = object_x
        self.this_object_y = object_y
        self.this_object_degree_rot = object_degree_rot
        self.this_object_col1 = object_col1
        self.this_object_col2 = object_col2
        
        #the equation of a point on the circle is (x,y) = (a+r*cos(t), b+r*sin(t)) where t is the rotation in rads
        self.rad_rot = (self.this_object_degree_rot*math.pi)/180
        self.object_1_x = self.this_object_x + double_object_distance/2*math.cos(self.rad_rot)
        self.object_1_y = self.this_object_y + double_object_distance/2*math.sin(self.rad_rot)
        self.object_2_x = self.this_object_x + double_object_distance/2*math.cos(self.rad_rot + math.pi)
        self.object_2_y = self.this_object_y + double_object_distance/2*math.sin(self.rad_rot + math.pi)
        draw_text(self.this_object_name,(self.this_object_x,self.this_object_y),20)
        
        #function that makes a double object at x,y with colour col and rotation rot
    
    #function that draws the double object
    def draw_double_object(self):

        #the equation of a point on the circle is (x,y) = (a+r*cos(t), b+r*sin(t)) where t is the rotation in rads
        self.rad_rot = (self.this_object_degree_rot*math.pi)/180
        self.object_1_x = self.this_object_x + double_object_distance/2*math.cos(self.rad_rot)
        self.object_1_y = self.this_object_y + double_object_distance/2*math.sin(self.rad_rot)
        self.object_2_x = self.this_object_x + double_object_distance/2*math.cos(self.rad_rot + math.pi)
        self.object_2_y = self.this_object_y + double_object_distance/2*math.sin(self.rad_rot + math.pi)
        draw_text(self.this_object_name,(self.this_object_x,self.this_object_y),20)
        #internal variables to the function
        #controls
        if (keyboard.is_pressed('r')):
            self.this_object_degree_rot += 3
        if (keyboard.is_pressed('t')):
            self.this_object_degree_rot -= 3
        
        #drawing the double object
        pygame.draw.line(display,white,(int(self.object_1_x),int(self.object_1_y)),(int(self.object_2_x),int(self.object_2_y)), 2)
        pygame.draw.circle(display, self.this_object_col1, (int(self.object_1_x),int(self.object_1_y)), int(standard_object_size))
        pygame.draw.circle(display, self.this_object_col2, (int(self.object_2_x),int(self.object_2_y)), int(standard_object_size))

    

#INSTANCE STACK
#creating the cameras
cal_cam = camera("Callum Griffiths", display_width/3, display_height/2, 90, 0, False, 100)
jack_cam = camera("Jack Banfeild", 2*display_width/3, display_height/2, 90 , 0, True, 100)

#creating the double object
kobey_object = double_object("Kobey Rafferty", display_width/2, display_height/2, 90, blue, red)
dan_object = double_object("Daniel Buchhorn", display_width/2, display_height/3, 0, purple, orange)
double_objects = [kobey_object, dan_object]

#main running loop
running = True
while running:
    
    #fill the background with white
    display.fill(black)
       
    #switching activated object
    if (keyboard.is_pressed('z')):
        jack_cam.this_cam_activated = True
        cal_cam.this_cam_activated = False
    if (keyboard.is_pressed('x')):
        jack_cam.this_cam_activated = False
        cal_cam.this_cam_activated = True

    #drawing the camreas
    jack_cam.draw()
    cal_cam.draw()
    

    #drawing the objects
    kobey_object.draw_double_object()
    dan_object.draw_double_object()
    
    
    
    
    #input and event loop
    for event in pygame.event.get():

        #quitting loop
        if event.type == pygame.QUIT:
            running = False

    

    #update the display and wait a lil bit *do this last in the loop*
    print_controls_title()
    pygame.display.update()
    pygame.time.delay(10)


#quitting the application
pygame.quit()
