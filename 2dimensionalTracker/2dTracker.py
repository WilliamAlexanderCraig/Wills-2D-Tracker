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
#region
white = (255,255,255)
black = (0,0,0)
grey = (100,100,100)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
pink = (255,200,200)
purple = (167, 66, 244)
orange = (255, 178, 0)
cyan = (0, 201, 188)
light_green = (0,255,0)
light_red = (255, 0, 0)
light_blue = (0,0,255)
yellow = (244, 241, 66)
#endregion

#images
#region
wills_2d_tracker_img = pygame.image.load("wills_2d_tracker.png")
menu_img = pygame.image.load("menu_image.png")
start_button_img = pygame.image.load("start_button.png")
quit_button_img = pygame.image.load("quit_button.png")
more_information_button_img = pygame.image.load("more_information_button.png")
how_it_works_img = pygame.image.load("how_it_works_button.png")
start_button_hover_img = pygame.image.load("start_button_hover.png")
quit_button_hover_img = pygame.image.load("quit_button_hover.png")
more_information_button_hover_img = pygame.image.load("more_information_button_hover.png")
how_it_works_hover_img = pygame.image.load("how_it_works_button_hover.png")
#endregion

#object varables 
standard_object_size = 10
double_object_distance = 50

#some variables for animating the camera *DONT WORRY ABOUT THES
cam_fov_step = 5
cam_rot_step = 5
cam_move_step = 5


#FUNCTION STACK 

def print_menu_images():
    display.blit(wills_2d_tracker_img, (0,0))
    display.blit(menu_img, (100, 200))

#function that makes an object at x, y with colour col when called 
def print_controls_title():
    #print the text
    draw_text("Wills 2D Tracker", (0,0), 50)
    draw_text("Controls:", (0,display_height-120),20)
    draw_text("R and T to change object rotation", (0,display_height-100), 20)
    draw_text("Z and X activate cameras", (0,display_height-80),20)
    #draw_text("U and I change Radius", (0,display_height-60),20)
    draw_text("N and M change FOV", (0,display_height-40),20)
    draw_text("J and K change Rotation", (0,display_height-20),20)

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
    
#finding the distance between two objects in the most convoluted way possible because fuck it
def find_distance(pos_1_x, pos_1_y, pos_2_x, pos_2_y):
    #points = [(x1,y1), (x2,y2), (x2-x1, y2-y1)]
    #pygame.draw.lines(display, yellow, True, points, 2)
    dist = math.sqrt( (pos_1_x-pos_2_x)**2 + (pos_1_y-pos_2_y)**2 )
    return dist

#CLASS STACK
#class of camera
class camera:
    #function which is called at initialisation
    def __init__(self, cam_name, cam_x, cam_y, cam_degree_fov, cam_degree_rot, cam_activated, radius):
        #funky shit
        self.this_cam_name = cam_name
        self.this_cam_x = cam_x
        self.this_cam_y = cam_y
        self.this_cam_degree_fov = cam_degree_fov
        self.this_cam_degree_rot = cam_degree_rot
        self.this_cam_activated = cam_activated
        self.this_cam_radius = radius
        

    #function that draws the entire camera and deals with controls
    def draw(self):
        #convert degree_rot to rads
        rad_rot = (self.this_cam_degree_rot*math.pi)/180
        #convert degree_fov to rads
        rad_fov = (self.this_cam_degree_fov*math.pi)/180 

        draw_text(self.this_cam_name, (self.this_cam_x,self.this_cam_y), 20)
        
        #fov lines degrees
        negative_fov_line_degree_rot = self.this_cam_degree_rot - (self.this_cam_degree_fov/2)
        positive_fov_line_degree_rot = self.this_cam_degree_rot + (self.this_cam_degree_fov/2)
        
        #use the PARAMETRIC EQUATION TO FIND THE POINT ON A CIRCLE ****VERY IMPORTANT*** GOOGLE IT 
        #drawing the camera
        if (self.this_cam_activated):
            draw_text("Camera position: " + str(self.this_cam_x) + " , " + str(self.this_cam_y), (0,70), 20)
            draw_text("Fov: " + str(self.this_cam_degree_fov) + " Rot: " + str(self.this_cam_degree_rot), (0,90), 20)
            draw_text("PosFovRotDeg: " + str(positive_fov_line_degree_rot) + " NegFovRotDeg: " + str(negative_fov_line_degree_rot), (0, 110), 20)
            pygame.draw.circle(display, green, (int(self.this_cam_x),int(self.this_cam_y)), standard_object_size)
        else:  
            pygame.draw.circle(display, grey, (int(self.this_cam_x),int(self.this_cam_y)), standard_object_size)
        

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

            #Limiting variables TODO FIX THE LIMITIN
            
            if (self.this_cam_degree_fov > 180):
                self.this_cam_degree_fov = 180
            if (self.this_cam_degree_fov < 0):
                self.this_cam_degree_fov = 0
            
            if (self.this_cam_degree_rot > 360):
                self.this_cam_degree_rot = 0
            if (self.this_cam_degree_rot < 0):
                self.this_cam_degree_rot = 359
            
            if (self.this_cam_x >display_width):
                self.this_cam_x = display_width
            if (self.this_cam_y > display_height):
                self.this_cam_y = display_height
            if (self.this_cam_x < 0):
                self.this_cam_x = 0
            if (self.this_cam_y < 0):
                self.this_cam_y = 0
            

        #drawing the fov lines
        ray_lengths = 1000
        #calculating the negative point 
        negative_fov_direction = (self.this_cam_x + ray_lengths* math.cos(rad_rot-(rad_fov/2)), self.this_cam_y + ray_lengths* math.sin(rad_rot-(rad_fov/2)))
        #drawing the negative point
        pygame.draw.line(display, green, (self.this_cam_x, self.this_cam_y), negative_fov_direction, 2)
        #calculating the positive point 
        positive_fov_direction = (self.this_cam_x + ray_lengths* math.cos(rad_rot+(rad_fov/2)), (self.this_cam_y + ray_lengths* math.sin(rad_rot+(rad_fov/2))))
        #drawing the positive point
        pygame.draw.line(display, green, (self.this_cam_x, self.this_cam_y), positive_fov_direction, 2)
        
        #drawing the pink arc for estimating distance
        '''
        points = [(self.this_cam_x,self.this_cam_y),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot-(rad_fov/2)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot-(rad_fov/2))), 
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot-(rad_fov/4)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot-(rad_fov/4))),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot)),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot+(rad_fov/4)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot+(rad_fov/4))),
        (self.this_cam_x + self.this_cam_radius* math.cos(rad_rot+(rad_fov/2)), self.this_cam_y + self.this_cam_radius* math.sin(rad_rot+(rad_fov/2)))
        ]
        pygame.draw.lines(display, orange, True, points, 2)
        '''
        #drawing the camera view background
        pygame.draw.rect(display, grey, pygame.Rect(display_width-500, 0,500, 50))

        #drawing a line between every object and the camera (the colourful ones) (this has nothing to do with the calculation about finding the distance, only for graphics
        for d_object in double_objects:
            #get the positions
            cam_pos = (self.this_cam_x, self.this_cam_y)
            object_1_pos = (d_object.object_1_pos[0], d_object.object_1_pos[1])
            object_2_pos = (d_object.object_2_pos[0], d_object.object_2_pos[1])

            #object 1
            #case 1 cam is top and left of object
            if (self.this_cam_activated and object_1_pos[0] > cam_pos[0] and object_1_pos[1] > cam_pos[1]):
                a = object_1_pos[0] - cam_pos[0]
                b = object_1_pos[1] - cam_pos[1]
                c = find_distance(object_1_pos[0], object_1_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.asin(b/c)/math.pi)
                
                
                if (negative_fov_line_degree_rot < theta < positive_fov_line_degree_rot):
                    
                    if (d_object == alice_object):
                        pygame.draw.line(display, d_object.this_col1, object_1_pos, cam_pos, 2)
                        draw_text("Theta: " + str(theta), (0,150), 20)
                    self.draw_camera_view(theta, d_object.this_col1)
            
            #case 2 cam is top and right of object
            if (self.this_cam_activated and object_1_pos[0] < cam_pos[0] and object_1_pos[1] > cam_pos[1]):
                
                a = cam_pos[0] - object_1_pos[0]
                b = object_1_pos[1] - cam_pos[1]
                c = find_distance(object_1_pos[0], object_1_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.asin(b/c)/math.pi)
                
                if (negative_fov_line_degree_rot < 180 - theta < positive_fov_line_degree_rot):
                    pygame.draw.line(display, d_object.this_col1, object_1_pos, cam_pos, 2)
                    if (d_object == alice_object):
                        draw_text("Theta: " + str(theta), (0,150), 20)
                    self.draw_camera_view(theta, d_object.this_col1)

            #case 3 cam is bottom and right of object
            if (self.this_cam_activated and object_1_pos[0] < cam_pos[0] and object_1_pos[1] < cam_pos[1]):
                
                a = cam_pos[0] - object_1_pos[0]
                b = cam_pos[1] - object_1_pos[1]
                c = find_distance(object_1_pos[0], object_1_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.acos(b/c)/math.pi)
                
                if (negative_fov_line_degree_rot < 270 - theta < positive_fov_line_degree_rot):
                    pygame.draw.line(display, d_object.this_col1, object_1_pos, cam_pos, 2)
                    if (d_object == alice_object):
                        draw_text("Theta: " + str(theta), (0,150), 20)
                    self.draw_camera_view(theta, d_object.this_col1)
            
            #case 4 cam is bottom and left of object
            if (self.this_cam_activated and object_1_pos[0] > cam_pos[0] and object_1_pos[1] < cam_pos[1]):
                
                a = cam_pos[0] - object_1_pos[0]
                b = cam_pos[1] - object_1_pos[1]
                c = find_distance(object_1_pos[0], object_1_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.acos(b/c)/math.pi)
                
                if (negative_fov_line_degree_rot < 270 + theta < positive_fov_line_degree_rot):
                    pygame.draw.line(display, d_object.this_col1, object_1_pos, cam_pos, 2)
                    if (d_object == alice_object):
                        draw_text("Theta: " + str(theta), (0,150), 20)
                    self.draw_camera_view(theta, d_object.this_col1)


            #object 2
            #case 1 cam is top and left of object
            if (self.this_cam_activated and object_2_pos[0] > cam_pos[0] and object_2_pos[1] > cam_pos[1]):
                a = object_2_pos[0] - cam_pos[0]
                b = object_2_pos[1] - cam_pos[1]
                c = find_distance(object_2_pos[0], object_2_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.asin(b/c)/math.pi)
                
                
                if (negative_fov_line_degree_rot < theta < positive_fov_line_degree_rot):
                    pygame.draw.line(display, d_object.this_col2, object_2_pos, cam_pos, 2)
            
            #case 2 cam is top and right of object
            if (self.this_cam_activated and object_2_pos[0] < cam_pos[0] and object_2_pos[1] > cam_pos[1]):
                
                a = cam_pos[0] - object_2_pos[0]
                b = object_2_pos[1] - cam_pos[1]
                c = find_distance(object_2_pos[0], object_2_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.asin(b/c)/math.pi)
                
                if (negative_fov_line_degree_rot < 180 - theta < positive_fov_line_degree_rot):
                    pygame.draw.line(display, d_object.this_col2, object_2_pos, cam_pos, 2)

            #case 3 cam is bottom and right of object
            if (self.this_cam_activated and object_2_pos[0] < cam_pos[0] and object_2_pos[1] < cam_pos[1]):
                
                a = cam_pos[0] - object_2_pos[0]
                b = cam_pos[1] - object_2_pos[1]
                c = find_distance(object_2_pos[0], object_2_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.acos(b/c)/math.pi)
                
                if (negative_fov_line_degree_rot < 270 - theta < positive_fov_line_degree_rot):
                    pygame.draw.line(display, d_object.this_col2, object_2_pos, cam_pos, 2)
            
            #case 4 cam is bottom and left of object
            if (self.this_cam_activated and object_2_pos[0] > cam_pos[0] and object_2_pos[1] < cam_pos[1]):
                
                a = cam_pos[0] - object_2_pos[0]
                b = cam_pos[1] - object_2_pos[1]
                c = find_distance(object_2_pos[0], object_2_pos[1], cam_pos[0], cam_pos[1])

                theta = 180 * (math.acos(b/c)/math.pi)
                
                if (negative_fov_line_degree_rot < 270 + theta < positive_fov_line_degree_rot):
                    pygame.draw.line(display, d_object.this_col2, object_2_pos, cam_pos, 2)
            
    def draw_camera_view(self, angle, col):
        #self.this_angle = angle
        #fov lines degrees
        negative_fov_line_degree_rot = self.this_cam_degree_rot - (self.this_cam_degree_fov/2)
        positive_fov_line_degree_rot = self.this_cam_degree_rot + (self.this_cam_degree_fov/2)
        arc_x_value = 150

        pygame.draw.line(display, col, (display_width - 500 + arc_x_value, 0), (display_width - 500 + arc_x_value, 50), 5)


        



class double_object:
    #function that is called when initalised 
    def __init__(self, object_name, object_pos, object_degree_rot, col1, col2):
        self.this_object_name = object_name
        self.this_object_pos = object_pos
        self.this_object_degree_rot = object_degree_rot
        self.this_col1 = col1
        self.this_col2 = col2
        #the equation of a point on the circle is (x,y) = (a+r*cos(t), b+r*sin(t)) where t is the rotation in rads
        self.rad_rot = (self.this_object_degree_rot*math.pi)/180

        #setting the position of the single objects
        self.object_1_pos =  (self.this_object_pos[0] + double_object_distance/2*(math.cos(self.rad_rot)), self.this_object_pos[1] + double_object_distance/2*(math.sin(self.rad_rot)))
        self.object_2_pos = (self.this_object_pos[0] + double_object_distance/2*(math.cos(self.rad_rot + math.pi)), self.this_object_pos[1] + double_object_distance/2*(math.sin(self.rad_rot + math.pi)))
        
        draw_text(self.this_object_name, self.this_object_pos,20)
        
    
    #function that draws the double object
    def draw_double_object(self):
        draw_text(self.this_object_name, self.this_object_pos,20)
        #internal variables to the function
        #controls
        if (keyboard.is_pressed('r')):
            self.this_object_degree_rot += 3
        if (keyboard.is_pressed('t')):
            self.this_object_degree_rot -= 3
        #setting the position of the single objects
        self.object_1_pos =  (self.this_object_pos[0] + double_object_distance/2*(math.cos(self.rad_rot)), self.this_object_pos[1] + double_object_distance/2*(math.sin(self.rad_rot)))
        self.object_2_pos = (self.this_object_pos[0] + double_object_distance/2*(math.cos(self.rad_rot + math.pi)), self.this_object_pos[1] + double_object_distance/2*(math.sin(self.rad_rot + math.pi)))
        
        #drawing the double object
        pygame.draw.line(display,white, self.object_1_pos, self.object_2_pos, 2)
        pygame.draw.circle(display, self.this_col1, (int(self.object_1_pos[0]),int(self.object_1_pos[1])), int(standard_object_size))
        pygame.draw.circle(display, self.this_col2, (int(self.object_2_pos[0]),int(self.object_2_pos[1])), int(standard_object_size))
        
class button:
    def __init__(self, pos, size, col_normal, col_hover, text):
        self.this_button_pos = pos
        self.this_button_size = size
        self.this_button_col_normal = col_normal
        self.this_button_col_hover = col_hover
        self.this_button_text = text
    
    def draw_button (self, is_image, image, image_pressed):
        mouse = pygame.mouse.get_pos()

        if (not is_image):
            if (self.this_button_pos[0] < mouse[0] < self.this_button_pos[0] + self.this_button_size[0] and self.this_button_pos[1] < mouse[1] < self.this_button_pos[1] + self.this_button_size[1]):
                pygame.draw.rect(display, self.this_button_col_hover, pygame.Rect(self.this_button_pos[0],self.this_button_pos[1],self.this_button_size[0], self.this_button_size[1]))
                draw_text (self.this_button_text, self.this_button_pos, self.this_button_size[1])
            else: 
                pygame.draw.rect(display, self.this_button_col_normal, pygame.Rect(self.this_button_pos[0],self.this_button_pos[1],self.this_button_size[0], self.this_button_size[1]))
                draw_text (self.this_button_text, self.this_button_pos, self.this_button_size[1])
        if (is_image):
            if (self.this_button_pos[0] < mouse[0] < self.this_button_pos[0] + self.this_button_size[0] and self.this_button_pos[1] < mouse[1] < self.this_button_pos[1] + self.this_button_size[1]):
                display.blit(image_pressed, self.this_button_pos)
            else:
                display.blit(image, self.this_button_pos)


    def check_for_click(self):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        if (click[0] == 1 and self.this_button_pos[0] < mouse[0] < self.this_button_pos[0] + self.this_button_size[0] and self.this_button_pos[1] < mouse[1] < self.this_button_pos[1] + self.this_button_size[1]):           
            return True
        else:
            return False

#INSTANCE STACK
#creating the cameras
cal_cam = camera("Callum Griffiths", display_width/3, display_height/2, 90, 0, False, 100)
jack_cam = camera("Jack Banfeild", 2*display_width/3, display_height/2, 90, 180, True, 100)

#creating the double object
kobey_object = double_object("Kobey Rafferty", (display_width/2, display_height/2), 90, blue, red)
dan_object = double_object("Daniel Buchhorn", (display_width/2, display_height/3), 0, purple, pink)
alice_object = double_object("Alice Hood", (display_width/2, 2* display_height/3), 30, cyan, white)
double_objects = [kobey_object, dan_object, alice_object]

#creating button
start_button = button((3*display_width/4, display_height/4), (200,100), green, grey, "Start")
more_information_button = button((3*display_width/4, (display_height/4) + 100), (200,100), blue, grey, "More Information")
how_it_works = button ((3*display_width/4, (display_height/4) + 200), (200,100),yellow, grey, "How it Works")
quit_button = button ((3*display_width/4, (display_height/4) + 300), (200,100), red, grey, "Quit")

## LOOP STACK

#loop switcher
menu = True
running = False
#menu loop 
while menu:
    
    #fill the background with white
    display.fill(blue)
    
    #drawing the button
    start_button.draw_button(True, start_button_img, start_button_hover_img)
    if (start_button.check_for_click()):
        menu = False
        running = True
    more_information_button.draw_button(True, more_information_button_img, more_information_button_hover_img)

    how_it_works.draw_button(True, how_it_works_img, how_it_works_hover_img)
    
    
    quit_button.draw_button(True, quit_button_img, quit_button_hover_img)
    if (quit_button.check_for_click()):
        menu = False
        running = False

     #input and event loop
    for event in pygame.event.get():

        #quitting loop
        if event.type == pygame.QUIT:
            menu = False

    #update the display and wait a lil bit *do this last in the loop*
    print_menu_images()
    pygame.display.update()
    pygame.time.delay(10)

#main running loop
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
    alice_object.draw_double_object()

    #testing 
    jack_cam.draw_camera_view(0, blue)
    


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
