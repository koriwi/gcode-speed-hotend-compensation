#!/usr/bin/python3
from gcodeparser import GcodeParser
import math


def get_accel_dist(target_vel, cur_vel, accel):
    return (target_vel*target_vel-cur_vel *
            cur_vel)/(2*accel)


def get_accel_time_from_dist(cur_vel, dist, accel):
    discriminant = cur_vel*cur_vel - 2*accel*dist*-1
    discriminant = max(0, discriminant)
    return (-cur_vel+math.sqrt(discriminant))/acceleration


file1 = open('benchy.gcode', 'r')
file2 = open("result.gcode", 'w+')
gcode = file1.read()
raw_lines = file1.readlines()

count = 0
acceleration = 1000
current_velocity = 5
max_velocity = 30
current_x = 0
current_y = 0
layer_time = 0
layer_distance = 0
current_line_number = 0
complete_time = 0
target_temp = 263
max_speed_normal_temp = 120
compensation = 3.5

for line in GcodeParser(gcode).lines:
    count += 1
    if line.command_str == 'M204':
        acceleration = line.params['S']
    if line.command_str == 'M104':
        target_temp = line.params['S']
    if line.command_str == 'G1' or line.command_str == 'G0':
        if line.params.__contains__('F'):
            max_velocity = line.params['F'] / 60

        # distance spend accelerating

        if line.params.__contains__('X'):
            accel_dist = get_accel_dist(
                max_velocity, current_velocity, acceleration)
            move_distance = math.sqrt(
                pow(line.params['X']-current_x, 2) + pow(line.params['Y']-current_y, 2))
            if move_distance < accel_dist * 2:
                accel_time = get_accel_time_from_dist(
                    current_velocity, move_distance/2, acceleration)
            else:

                accel_time = get_accel_time_from_dist(
                    current_velocity, accel_dist, acceleration)
            layer_time += accel_time*2
            current_x = line.params['X']
            current_y = line.params['Y']
            move_time = max((move_distance-accel_dist*2)/max_velocity, 0)
            layer_time += move_time
            layer_distance += move_distance
        if line.params.__contains__('Z') and layer_time > 3.75:
            avg_vel = layer_distance / layer_time
            file2.write('; layer_avg_vel {}\n'.format(avg_vel))
            file2.write('M104  S{}\n'.format(target_temp +
                                             max(avg_vel-max_speed_normal_temp, 0)/compensation))
            complete_time += layer_time
            layer_time = 0
            layer_distance = 0
            current_line_number = count
    file2.write(line.gcode_str+'\n')


print(complete_time)
