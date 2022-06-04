import pygame, pgzero, pgzrun
import math
import time

# Initial set up

# | Screen

# colours
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

colors = [images.ball, images.ball2, images.ball3, images.ball4, images.ball5, images.ball6]
color_index = 0
color_ball = colors[color_index]

# size
WIDTH = 1920
HEIGHT = 1050

top_left_x = WIDTH / 2
top_left_y = HEIGHT / 2

# sprites
cannon = Actor("head", center=(-600 + top_left_x, 250 + top_left_y))

# MORE

show_options = False
show_info = False

comment = ""
timer_comment = 0

force = 20


######
# SIMULATION FUNCTIONS
######


class Ball:
    def __init__(self, name, image, angle, a_y, a_x, v_y, v_x, ball_y, ball_x):
        self.name = name
        self.image = image

        # ANGLE
        self.angle = angle + 20

        # ACCELERATION
        self.a_y = a_y
        self.a_x = a_x

        # VELOCITY
        self.v_y = v_y * math.sin(math.radians(self.angle))
        self.v_x = v_x * math.cos(math.radians(self.angle))

        # POSITION
        self.ball_y = ball_y
        self.ball_x = ball_x

        # PRESERVED CONSTANTS
        self.constant_angle = self.angle + 20

        self.constant_a_y = a_y
        self.constant_a_x = a_x

        self.constant_v_y = v_y
        self.constant_v_x = v_x

        self.constant_ball_y = ball_y
        self.constant_ball_x = ball_x

        # OTHER
        self.show_path = False
        self.show_variables = False

        self.freeze = False

        self.path_points = []  # Records the points of the ball's path

    def ball_update(self):  # Simulation
        # Gravity: Falling Balls simulator

        self.v_y += self.a_y

        if self.ball_y + self.v_y < 325:
            self.ball_y += self.v_y
        else:
            # Bounce Simulator

            self.ball_y = 325
            self.v_y *= -(2 / 3)

            self.v_x *= (2 / 3)

            # if int(abs(self.v_y)) > 5:
            #     sounds.thud.play()

        self.ball_x += self.v_x

        if [images.ball_stamp, self.ball_x, self.ball_y] not in self.path_points:  # Record path points
            self.add_point(self.ball_x, self.ball_y)

    def add_point(self, x, y):  # Adds a point to our path point list
        self.path_points.append([images.ball_stamp, x, y])

    def display_variables(self):
        if self.show_variables:
            draw_rect(0, 0, 700, 500, PALE_BLUE, None)
            draw_rect(0, -200, 700, 125, DARK_BLUE, None)
            show_text("VARIABLES", -145, -220, WHITE, 75)
            show_text(f"Acceleration along y-axis: a_y = {int(self.a_y)}", -280, -120, WHITE, 25)
            show_text(f"Acceleration along x-axis: a_x = {int(self.a_x)}", -280, -90, WHITE, 25)
            show_text(f"Velocity along y-axis: v_y = {-int(self.v_y)}", -280, -60, WHITE, 25)
            show_text(f"Velocity along x-axis: v_x = {int(self.v_x)}", -280, -30, WHITE, 25)
            show_text(f"Position along y-axis: ball_y = {int(self.ball_y)}", -280, 0, WHITE, 25)
            show_text(f"Position along x-axis: ball_x = {int(self.ball_x)}", -280, 30, WHITE, 25)
            show_text(f"Angle of Ball: angle = {int(self.angle + 20)}", -280, 60, WHITE, 25)

    def check_controls(self):
        global balls, index, active_ball

        if keyboard.k_1:  # Toggle View Path on screen
            if self.show_path:
                self.show_path = False
            else:
                self.show_path = True

        if keyboard.k_2:  # View Variables' Table on screen
            if self.show_variables:
                self.show_variables = False
            else:
                self.show_variables = True

        if keyboard.k_3:  # Replay Ball's Motion on screen
            self.angle = self.constant_angle

            self.a_y = self.constant_a_y
            self.a_x = self.constant_a_x

            self.v_y = self.constant_v_y * math.sin(math.radians(self.angle))
            self.v_x = self.constant_v_x * math.cos(math.radians(self.angle))

            self.ball_y = self.constant_ball_y
            self.ball_x = self.constant_ball_x

            self.path_points = []

        if keyboard.k_4:  # Freeze Ball in place
            if self.freeze:
                self.freeze = False
            else:
                self.freeze = True

        if keyboard.k_5:  # Delete Ball activity and records
            if len(balls) > 1:
                balls.remove(active_ball)
                index -= 1
                active_ball = balls[index]

        if keyboard.up:
            self.angle += 1
        elif keyboard.down:
            self.angle -= 1

    def draw_points(self):
        for point in self.path_points:
            draw_image(point[0], point[1], point[2])

    def draw(self):
        if self.show_path:
            self.draw_points()

        draw_image(self.image, self.ball_x, self.ball_y)
        show_text(self.name, self.ball_x, self.ball_y - 25, WHITE, 25)


#######
# DISPLAY FUNCTIONS
#######

balls = [Ball(f"ball {0}", color_ball, cannon.angle, 0.5, 0, -20, 20, 250, -600)]
active_ball = balls[0]
index = 0

color_index += 1
color_ball = colors[color_index]


def draw():
    screen.clear()
    screen.fill(BLACK)

    for ball in balls:
        ball.draw()
        if ball.freeze is False:
            ball.ball_update()

    cannon.draw()
    draw_image(images.body, -500, 320)

    display_main()
    display_options()
    display_info()

    for ball in balls:
        ball.display_variables()


def display_main():
    draw_rect(0, -400, 750, 150, DARK_BLUE, None)
    show_text("GRAVITY SIMULATION 2", -275, -420, WHITE, 75)
    draw_image(images.earth, -275, -312.5)

    draw_rect(0, 0, 1900, 1025, None, BLUE)
    draw_rect(0, 800, 1920, 950, PALE_BLUE, None)

    draw_rect(-650, -400, 375, 130, DARK_BLUE, None)
    show_text("MENU", -742.5, -435, WHITE, 100)
    show_text("Press key 0", -690, -370, WHITE, 25)

    draw_rect(650, -400, 375, 130, DARK_BLUE, None)
    show_text("INFO", 572.5, -435, WHITE, 100)
    show_text("Press key 9", 610, -370, WHITE, 25)

    if timer_comment != 0:
        show_text(comment, -375, -305, WHITE, 35)


def display_options():
    if show_options:
        draw_rect(-650, -80, 230, 500, PALE_BLUE, None)
        show_text("Toggle Path: Press 1", -740, -310, WHITE, 25)
        show_text("View Variables: Press 2", -740, -280, WHITE, 25)
        show_text("Replay: Press 3", -740, -250, WHITE, 25)
        show_text("Freeze Ball: Press 4", -740, -220, WHITE, 25)
        show_text("Delete Ball: Press 5", -740, -190, WHITE, 25)

        show_text("Change Angle: Press \n"
                  "Up and Down", -740, -120, WHITE, 25)
        show_text("Change Force: Press \n"
                  "6 and 7", -740, -70, WHITE, 25)
        show_text("Create Ball: Press \n"
                  "Space", -740, -20, WHITE, 25)
        show_text("Activate Ball: Press \n"
                  "Right and Left", -740, 30, WHITE, 25)


def display_info():
    if show_info:
        draw_rect(650, -80, 230, 500, PALE_BLUE, None)
        show_text("Activated Ball: " + active_ball.name, 560, -310, WHITE, 25)
        show_text(f"Num of Balls: {len(balls)}", 560, -280, WHITE, 25)

        show_text(f"Force Measure: {force}", 560, -210, WHITE, 25)
        show_text(f"Angle: {cannon.angle + 20}", 560, -180, WHITE, 25)


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
              colour=WHITE,
              size=75):
    screen.draw.text(text_to_show,
                     (top_left_x + x, top_left_y + y),
                     fontsize=size, color=colour)


def check():
    global show_options, show_info
    global index, active_ball
    global balls
    global force
    global comment, timer_comment
    global color_ball, color_index

    if keyboard.k_0:
        if show_options:
            show_options = False
        else:
            show_options = True

    if keyboard.k_9:
        if show_info:
            show_info = False
        else:
            show_info = True

    if keyboard.up:
        if (cannon.angle + 20) < 70:
            cannon.angle += 1
        else:
            comment = "Cannot turn angle more than 70 degrees. \n" \
                      "Your Friendly Commenter \n" \
                      ";)"
            timer_comment = 1

    elif keyboard.down:
        if (cannon.angle + 20) > 5:
            cannon.angle -= 1
        else:
            comment = "Cannot turn angle less than 5 degrees. \n" \
                      "Your Friendly Commenter \n" \
                      ";)"
            timer_comment = 1

    if keyboard.k_7:
        if force < 50:
            force += 1
    elif keyboard.k_6:
        if force > 20:
            force -= 1

    if keyboard.right:
        clock.unschedule(active_ball.check_controls)

        active_ball.show_variables = False

        if index == len(balls) - 1:
            index = 0
        else:
            index += 1

        active_ball = balls[index]
        clock.schedule_interval(active_ball.check_controls, 0.075)

    elif keyboard.left:
        clock.unschedule(active_ball.check_controls)

        active_ball.show_variables = False

        if index == 0:
            index = len(balls) - 1
        else:
            index -= 1
        active_ball = balls[index]

        clock.schedule_interval(active_ball.check_controls, 0.075)

    if keyboard.SPACE:
        if len(balls) < 15:
            clock.unschedule(active_ball.check_controls)

            balls.append(Ball(f"ball {len(balls)}", color_ball, cannon.angle, 0.5, 0, -force, force, 250, -600))
            active_ball = balls[len(balls) - 1]

            color_index += 1
            if color_index == len(colors):
                color_index = 0
            color_ball = colors[color_index]

            clock.schedule_interval(active_ball.check_controls, 0.075)
        else:
            comment = " Cannot contain more than 15 balls at a time." \
                      "\n To make some space, delete some of the balls by pressing key 5." \
                      "\n Your Friendly Commenter" \
                      "\n ;)"
            timer_comment = 1

    if timer_comment != 0:
        timer_comment += 1
        if timer_comment == 35:
            timer_comment = 0


#####
# RUN FUNCTIONS
#####

comment = "Welcome to Gravity Simulation 2nd!"
timer_comment = 1

for ball in balls:
    if ball.name == active_ball.name:
        clock.schedule_interval(ball.check_controls, 0.075)

    clock.schedule_interval(ball.ball_update, 0.1)

clock.schedule_interval(check, 0.1)

pgzrun.go()
