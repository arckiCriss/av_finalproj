import copy
import random
import pygame, math
from pygame.locals import *
from sys import exit
import numpy as np

pygame.init()

car = pygame.image.load('car.png')
car_bg = pygame.image.load('car_gb.png')
bs = pygame.image.load('bs.png')
connected_bs = pygame.image.load('connected_bs.png')
bg = pygame.image.load('map.PNG')
font = pygame.font.SysFont('calibri', bold=True, size=20)
w, h = bs.get_size()

TURN_SPEED = 5
ACCELERATION = 1
MAX_SPEED = 2
# BG = (0, 0, 0)
MAX_Y = 1095
MAX_X = 1968

screen = pygame.display.set_mode((MAX_X, MAX_Y), 0, 32)
pygame.display.set_caption("Simulator")
pygame.mixer.init()
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
speed = direction = 0

endpoint_x = 1700
# position = [100, 230]
position = [100, 650]

list_bs = []

list_cars = []
speed_cars = 0
log_cars = []
list_gb = []
printed_cars=[]
while True:
    clock.tick(60)
    for event in pygame.event.get():

        if event.type == QUIT:
            exit()


        if event.type == MOUSEBUTTONDOWN:
            bs_x, bs_y = event.pos
            bs_x = bs_x - h / 2
            bs_y = bs_y - w / 2
            list_bs.append([int(bs_x), int(bs_y)])

        if not hasattr(event, 'key'):
            continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT:
            k_right = down * TURN_SPEED
        elif event.key == K_LEFT:
            k_left = down * TURN_SPEED
        elif event.key == K_UP:
            k_up = down * ACCELERATION
        elif event.key == K_DOWN:
            k_down = down * ACCELERATION

        if event.type == KEYUP and event.key == K_c:
            ini_postion = copy.deepcopy(position)
            random_seed = random.randint(1, 10)
            list_cars.append([[random_seed, 0], ini_postion])
            log_cars.append([])

    # if k_up > 0 and abs(speed - k_up) <= MAX_SPEED:
    #     speed -= k_up
    # if k_down > 0 and abs(speed + k_down) <= MAX_SPEED:
    #     speed += k_down
    #
    # direction -= (k_right - k_left)
    # x, y = position
    # rad = direction * math.pi / 180
    # x += speed * math.sin(rad)
    # y += speed * math.cos(rad)
    # if y < 0:
    #     y = 0
    # elif y > MAX_Y:
    #     y = MAX_Y
    # if x < 0:
    #     x = 0
    # elif x > MAX_X:
    #     x = MAX_X
    # position = (int(x), int(y))
    # rotated = pygame.transform.rotate(car, direction)
    # rect = rotated.get_rect()
    # rect.center = position

    #bg draw
    screen.blit(bg, (0, 0))

    #bs draw
    for i in range(len(list_bs)):
        screen.blit(bs, (list_bs[i][0], list_bs[i][1]))
        surface = font.render(str(i), False, (255, 255, 255))
        screen.blit(surface, (list_bs[i][0] + w / 2 - 5, list_bs[i][1] + h / 2 + 30))

    # cur bs draw
    cur_bs = 'None'
    cur_min_ds = 9999;
    for i in range(len(list_bs)):
        if len(list_cars) > 0:
            for j in range(len(list_cars)):
                p1 = np.array([list_cars[j][1][0], list_cars[j][1][1]])
                p2 = np.array([list_bs[i][0] + w / 2, list_bs[i][1] + h / 2])
                p3 = p2 - p1
                p4 = math.hypot(p3[0], p3[1])
                if p4 < w / 2 and p4 < cur_min_ds:
                    if (j % 2) == 0:
                        cur_min_ds = p4
                        cur_bs = str(i)
                        screen.blit(connected_bs, (list_bs[i][0], list_bs[i][1]))
                        log_cars[j].append(i)
                    else:
                        if i in list_gb:
                            cur_min_ds = p4
                            cur_bs = str(i)
                            screen.blit(connected_bs, (list_bs[i][0], list_bs[i][1]))
                            log_cars[j].append(i)

    # # cur bs draw
    # cur_bs_ind = font.render('Current Base Station: No. ' + cur_bs, False, (255, 0, 0))
    # screen.blit(cur_bs_ind, (10, 10))

    # car draw
    # screen.blit(rotated, rect)
    if len(list_cars) > 0:
       for i in range(len(list_cars)):
           if (i%2)==0:
               screen.blit(car, (list_cars[i][1][0],list_cars[i][1][1]))
           else:
               screen.blit(car_bg, (list_cars[i][1][0], list_cars[i][1][1]))

           if list_cars[i][1][0] < endpoint_x:
                list_cars[i][1][0] += list_cars[i][0][0]
           else:
                list_cars[i][0][1] = 1 # run over


    # show log
    if len(log_cars) > 0:
        for i in range(len(log_cars)):
            car_bs_ind = font.render('No. ' + str(i) +' car\'s '+ 'with speed '+ str(list_cars[i][0][0]) +', log:', False, (255, 0, 0))
            screen.blit(car_bs_ind, (10 , 10 + i * 30))
            for j in range(len(log_cars[i])):
                car_bs_ind_info = font.render(str(log_cars[i][j]), False, (255, 0, 0))
                screen.blit(car_bs_ind_info, (255 + j * 10, 10 + i * 30))

    #show global best need more precise calc
    if(len(list_bs))>0:
        for i in range(len(list_bs)):
            if list_bs[i][1] + w / 2 - position[1] <= 0 and i not in list_gb:
                list_gb.append(i)

    if(len(list_gb))>0:
        gb_ind_info_ind = font.render('Global best path: ', False, (255, 0, 0))
        screen.blit(gb_ind_info_ind, (10, 1000))
        for i in range(len(list_gb)):
            gb_ind_info = font.render(str(list_gb[i]), False, (255, 0, 0))
            screen.blit(gb_ind_info, (180 + i * 30, 1000))

    if len(log_cars) > 0:
        for i in range(len(log_cars)):
            if list_cars[i][0][1] == 1 and i not in printed_cars:
                list_remove_dup  = list(set(log_cars[i]))
                print("No. " + str(i) + ' car\'s handover time:')
                for j in range(len(list_remove_dup)):
                    print(str(250+random.randint(-50,50))+'ms for BS ' + str(list_remove_dup[j]))
                print('time cost for whole route: ' +str(68000/list_cars[i][0][0]) + 'ms')
                printed_cars.append(i)




    pygame.display.flip()
