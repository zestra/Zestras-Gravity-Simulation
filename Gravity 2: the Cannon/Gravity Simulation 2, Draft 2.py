import pygame, pgzero, pgzrun
import math

BLACK = (0, 0, 0)
BLUE = (0, 155, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (128, 0, 0)

DARK_BLUE = (0, 100, 200)
BRIGHT_BLUE = (100, 255, 355)
PALE_BLUE = (0, 35, 135)

DARK_GREY = (50, 50, 50)
DARKER_GREY = (10, 10, 10)

WIDTH = 1920
HEIGHT = 1050

top_left_x = WIDTH / 2
top_left_y = HEIGHT / 2

##################################################################
# EDIT THESE VARIABLES TO CHANGE THE SCENARIO!!!
#####

# ANGLE
angle = 17

# ACCELERATION
a_y = 0.5  # positive means move down for vertical acceleration
a_x = 0

# VELOCITY
v_y = -20 * math.sin(math.radians(angle))  # negative means move down for vertical velocity
v_x = 20 * math.cos(math.radians(angle))

# POSITION
ball_y = 250  # positive means move down for vertical position
ball_x = -600

# OTHER
show_path = False
show_variables = False
show_options = False
##################################################################


# PRESERVED CONSTANTS

constant_a_y = a_y
constant_a_x = a_x

constant_v_y = v_y
constant_v_x = v_x

constant_ball_y = ball_y
constant_ball_x = ball_x

path_points = []  # Records the points of the ball's path

cannon = Actor("head", center=(-600 + top_left_x, 250 + top_left_y))


######
# SIMULATION FUNCTIONS
######


def add_point(x, y):  # Adds a point to our path point list
    global path_points
    path_points.append([images.ball_stamp, x, y])


def ball_update():  # Simulation
    global ball_y, ball_x
    global a_y, a_x
    global v_y, v_x

    # Gravity: Falling Balls simulator

    v_y += a_y

    if ball_y + v_y < 325:
        ball_y += v_y
    else:
        # Bounce Simulator

        ball_y = 325
        v_y *= -(2 / 3)

        v_x *= (2 / 3)

        if int(abs(v_y)) > 5:
            sounds.thud.play()

    ball_x += v_x

    if [images.ball_stamp, ball_x, ball_y] not in path_points:  # Record path points
        add_point(ball_x, ball_y)

    pass


def check():
    global a_y, a_x, v_y, v_x, ball_y, ball_x
    global angle
    global path_points
    global show_variables, show_path, show_options

    if keyboard.k_0:
        if show_options:
            show_options = False
        else:
            show_options = True

    if keyboard.k_1:  # Toggle View Path
        if show_path:
            show_path = False
        else:
            show_path = True

    if keyboard.k_2:  # Reset
        a_y = constant_a_y

        # VELOCITY
        v_y = -20 * math.sin(math.radians(angle))  # negative means move down for vertical velocity
        v_x = 20 * math.cos(math.radians(angle))

        ball_y = constant_ball_y
        ball_x = constant_ball_x

        path_points = []

    if keyboard.k_3:
        if show_variables:
            show_variables = False
        else:
            show_variables = True

    if keyboard.up:
        cannon.angle += 1
        angle += 1
    elif keyboard.down:
        cannon.angle -= 1
        angle -= 1


#######
# DISPLAY FUNCTIONS
#######


def draw():
    screen.clear()
    screen.fill(BLACK)

    if show_path:
        draw_points()
    draw_image(images.ball, ball_x, ball_y)

    cannon.draw()
    draw_image(images.body, -500, 320)

    display_main()
    display_options()
    display_variables()


def draw_points():
    for point in path_points:
        draw_image(point[0], point[1], point[2])


def display_main():
    draw_rect(575, -440, 480, 70, WHITE, None)
    show_text(f"VELOCITY (x: {int(v_x)}, y: {-int(v_y)})", 390, -450, 0, 0, BLACK, 45)
    draw_rect(575, -360, 480, 70, WHITE, None)
    show_text(f"POSITION (x: {int(ball_x)}, y: {-int(ball_y)})", 390, -375, 0, 0, BLACK, 45)

    draw_rect(0, -400, 750, 150, DARK_BLUE, None)
    show_text("GRAVITY SIMULATION 2", -275, -420, 0, 0, WHITE, 75)

    draw_rect(0, 0, 1900, 1025, None, BLUE)
    draw_rect(0, 800, 1920, 950, PALE_BLUE, None)

    # draw_rect(-550, -410, 250, 120, PALE_BLUE, None)
    # show_text("Toggle Path: Press B", -640, -450, 0, 0, WHITE, 25)
    # show_text("Reset: Press Space", -640, -420, 0, 0, WHITE, 25)
    # show_text("View Variables: Press V", -640, -390, 0, 0, WHITE, 25)

    draw_rect(-650, -400, 375, 130, DARK_BLUE, None)
    show_text("MENU", -742.5, -435, 0, 0, WHITE, 100)
    show_text("Press key 0", -690, -370, 0, 0, WHITE, 25)


def display_variables():
    if show_variables:
        draw_rect(0, 0, 700, 500, PALE_BLUE, None)
        draw_rect(0, -200, 700, 125, DARK_BLUE, None)
        show_text("VARIABLES", -145, -220, 0, 0, WHITE, 75)
        show_text(f"Acceleration along y-axis: a_y = {int(a_y)}", -280, -120, 0, 0, WHITE, 25)
        show_text(f"Acceleration along x-axis: a_x = {int(a_x)}", -280, -90, 0, 0, WHITE, 25)
        show_text(f"Velocity along y-axis: v_y = {-int(v_y)}", -280, -60, 0, 0, WHITE, 25)
        show_text(f"Velocity along x-axis: v_x = {int(v_x)}", -280, -30, 0, 0, WHITE, 25)
        show_text(f"Position along y-axis: ball_y = {int(ball_y)}", -280, 0, 0, 0, WHITE, 25)
        show_text(f"Position along x-axis: ball_x = {int(ball_x)}", -280, 30, 0, 0, WHITE, 25)
        show_text(f"Angle of cannon: cannon.angle = {int(cannon.angle)}", -280, 60, 0, 0, WHITE, 25)


def display_options():
    if show_options:
        draw_rect(-650, -80, 230, 500, PALE_BLUE, None)
        show_text("Toggle Path: Press 1", -740, -310, 0, 0, WHITE, 25)
        show_text("Reset: Press 2", -740, -280, 0, 0, WHITE, 25)
        show_text("View Variables: Press 3", -740, -250, 0, 0, WHITE, 25)
        show_text("Change Angle: Press \n"
                  "Up and Down", -740, -220, 0, 0, WHITE, 25)
        pass
    pass


def draw_image(image, x, y):
    screen.blit(image,
                (top_left_x + x - image.get_width(),
                 top_left_y + y - image.get_height()))


def draw_rect(x, y,
              width, height,
              colour=BLACK,
              outline=None):
    if outline is not None:
        BOX2 = Rect((top_left_x + x - int(width / 2) - 2, top_left_y + y - int(height / 2) - 2),
                    (width + 4, height + 4)
                    )
        screen.draw.rect(BOX2, outline)

    if colour is not None:
        BOX = Rect((top_left_x + x - int(width / 2), top_left_y + y - int(height / 2)),
                   (width, height)
                   )
        screen.draw.filled_rect(BOX, colour)


def show_text(text_to_show, x, y,
              offset_y=0, offset_x=0,
              colour=WHITE,
              size=75):
    screen.draw.text(text_to_show,
                     (top_left_x + x + offset_x, top_left_y + y + offset_y),
                     fontsize=size, color=colour)


#####
# RUN FUNCTIONS
#####

clock.schedule_interval(check, 0.075)
clock.schedule_interval(ball_update, 0.1)
pgzrun.go()
