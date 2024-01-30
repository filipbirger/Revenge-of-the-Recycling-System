```python
import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.124.3' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.13 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.13
bin2_color = [0,1,0]
bin3_offset = 0.13
bin3_color = [0,0,1]
bin4_offset = 0.13
bin4_color = [1,1,1]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import random
#function that determines if a new dispensed material is the same kind as the materials on the q_bot
def group(container_info):#Wahhaj
    global i_d
    i_d=container_info[2]    #i_d is a variable containing the bin destination info
    i_d_array.append(i_d)
    if i_d !=i_d_array[0]:
        print("Container Doesnt Belong On Qbot")
        return True          # if the materials are not the same, returns True
    
  
# function that determines if the maximum mass has been loaded   
def mass(container_info):#Wahhaj
    mass=container_info[1]   # mass is a variable that takes on the mass of a material
    mass= int(mass)          
    mass_array.append(mass) 
    total_mass=sum(mass_array)
    if total_mass>90:
        print("Maximum Weight On QBot")
        return True          # if the mass has reached 90g, returns True

#function that determines if a maximum of 3 items are loaded on q_bot
#number_of_items_on_q_bot is a variable that takes on type of material and appends to a list 
def number_of_items_on_q_bot(container_info):#Wahhaj
    number_of_items_on_q_bot=container_info[0]
    number_of_items_on_q_bot.strip()
    number_of_items_on_q_bot_array.append(number_of_items_on_q_bot)
    number_of_items_on_q_bot_items=len(number_of_items_on_q_bot_array)
    if number_of_items_on_q_bot_items>int(3):
        print("Maximum Number Of Items On QBot")
        return True          # if the length of the list is longer than 3, returns True

# dispenses a random container until conditions are met
def dispense_container():#Filip                       
    global mass_array        # initializing lists used in previous functions, global used because called in functions later
    mass_array=[]            
    global number_of_items_on_q_bot_array
    number_of_items_on_q_bot_array=[]
    global counter_load
    counter_load=0           # initializing a counter 
    while True:              # infinite loop that runs until the conditions are met 
        value = random.randint(1,6) # randomly chooses a number from 1-6
        container_info=table.dispense_container(value, True)
        time.sleep(3)
        if group(container_info)==True:
            break            
        elif mass(container_info)==True or number_of_items_on_q_bot(container_info)==True:
            break     
        else:
            q_arm_load_container()
            counter_load+=1  # counts the times a material is dispensed
    print("Qbot Going To",(i_d_array[0]))  
    

def q_arm_load_container():#Filip 
                             
    arm.move_arm(0.66, 0.0, 0.28) #arm moves to the location of the dispensed
    time.sleep(2)                        
    arm.control_gripper(43)        #gripper holds the container
    time.sleep(2)
    #arm moves verticly above q_bot and loads container, this changes based on the counter_load,
    #places on a different location on the q_bot
    if counter_load==0:
        arm.move_arm(0,0,0.585)
        time.sleep(3)
        arm.move_arm(0, -0.595, 0.585)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        arm.home()
    elif counter_load==1:
        arm.move_arm(0,0,0.585)
        time.sleep(3)
        arm.move_arm(0, -0.55, 0.585)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        arm.home()
    elif counter_load==2:
        arm.move_arm(0,0,0.585)
        time.sleep(3)
        arm.move_arm(0, -0.54, 0.585)
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        arm.home()
    print("contianer Loaded")

def Transfer_Container():#Filip 
    bot.activate_color_sensor()
    if i_d_array[0] == "Bin01":                 #determines which bin to go to 
        color_destination_bin = [1, 0, 0]
    elif i_d_array[0] == "Bin02":
        color_destination_bin = [0, 1, 0]
    elif i_d_array[0] == "Bin03":
        color_destination_bin = [0, 0, 1]
    elif i_d_array[0] == "Bin04":
        color_destination_bin = [1, 1, 1]
    while True:                                 #loop for line following

        #individual detecting for left and right side
        color_sensor_read = (bot.read_color_sensor()[0])
        left_detect=int(bot.line_following_sensors()[0])
        right_detect=int(bot.line_following_sensors()[1])
        x=float(bot.position()[0])
        y=float(bot.position()[1])
        z=float(bot.position()[2])
        # coordinates of bins
        if 1<x<1.1 and 0.6<y<0.8 and 0.0005<z<0.0009 and color_sensor_read == color_destination_bin:
            break
            bot.rotate(5)
        elif -0.1<x<0.1 and 0.6<y<0.8 and 0.0005<z<0.0009 and color_sensor_read == color_destination_bin:
            break 
        elif -0.05<x<0.05 and -0.8<y<-0.6 and 0.0005<z<0.0009 and color_sensor_read == color_destination_bin:
            break 
        elif 1<x<1.1 and -0.8<y<-0.6 and 0.0005<z<0.0009 and color_sensor_read == color_destination_bin:
            break
        # if the bins are not found, q_bot line follows
        elif left_detect==1 and right_detect==1:
            bot.set_wheel_speed([0.1,0.1])
        elif left_detect==0 and right_detect==0:
            bot.set_wheel_speed([-0.05,-0.05])
        elif left_detect==0 and right_detect==1:
            bot.set_wheel_speed([0.05,0.025])
        elif left_detect==1 and right_detect==0:
            bot.set_wheel_speed([0.025,0.05])
    # if bin is found, stop
    bot.set_wheel_speed([0,0])

    
def dump():#Wahhaj
    #turns on linear actuator
    bot.activate_linear_actuator()
    bot.dump()
    time.sleep(2)

 
def return_home():#Wahhaj
    #loop for line following
    while True:
        #individual detecting for left and right side
        left_detect=int(bot.line_following_sensors()[0])
        right_detect=int(bot.line_following_sensors()[1])
        x=float(bot.position()[0])
        y=float(bot.position()[1])
        z=float(bot.position()[2])

        #location of home
        if 1.4<x<1.6 and -0.01<y<0.01:
            break 
        elif left_detect==1 and right_detect==1:
            bot.set_wheel_speed([0.1,0.1])
        elif left_detect==0 and right_detect==0:
            bot.set_wheel_speed([-0.1,-0.1])
        elif left_detect==0 and right_detect==1:
            bot.set_wheel_speed([0.05,0.015])
        elif left_detect==1 and right_detect==0:
            bot.set_wheel_speed([0.015,0.05])
    bot.set_wheel_speed([0,0])

    #if the materials have been disposed, removes them from the i_d list 
    #Filip 
    if counter_load == 1: 
        i_d_array.pop(0)
        if len(i_d_array)==2:    # the nested ifs are for a special case where the counter_load is n-1 instead of n
            i_d_array.pop(0)
    if counter_load == 0:
        i_d_array.pop(0)
    if counter_load == 2:
        i_d_array.pop(0)
        i_d_array.pop(0)
        if len(i_d_array)==2:
            i_d_array.pop(0)
    if counter_load == 3:
        i_d_array.pop(0)
        i_d_array.pop(0)
        i_d_array.pop(0)
        if len(i_d_array)==2:
            i_d_array.pop(0)
    print("returned HOME")

# function that call on all other functions and completes the recycling 
def recycle_material():#Filip 
    global i_d_array
    i_d_array = []
    while True:                  # infinite loop that continuously recycles 
        if len(i_d_array)==0:    # This is only used for the first cycle
            dispense_container()
        else:
            q_arm_load_container()
            dispense_container()
        Transfer_Container()
        dump()
        return_home()
```
