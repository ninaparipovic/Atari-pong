# Nina Paripovic
# 1 October 2018
# Lab assignment 1
# based on the smiley.pg program from lecture 6
# moves the Atari Pong paddles, keeping them within the graphics window
# If the ' ' key is pressed while the game is not in action, the ball begins moving and the game starts
# If the 'a' key is pressed, the left paddle moves upwards, unless it is already at the top of the screen
# If the 'z' key is pressed, the left paddle moves downwards, unless it is already at the bottom of the screen
# If the 'k' key is pressed, the right paddle moves upwards, unless it is already at the top of the screen
# If the 'm' key is pressed, the right paddle moves downwards, unless it is already at the bottom of the screen
# if the ball hits the top wall, bottom wall, or the paddles, the ball rebounds
# if the ball hits the left or right wall i.e. goes out of bounds, the ball stops and the player is instructed how to
# start a new game
# if the 'q' key is pressed, the graphics window closes



from cs1lib import *

# global constant variables
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
PADDLE_WIDTH = 20      # width of the paddles
PADDLE_LENGTH = 80     # length of the paddles
PADDLE_SPEED = 10   # rate at which the location of the paddles move
V_X = 5             # rate at which the ball moves in the horizontal direction
V_Y = 5             # rate at which the ball moves in the vertical direction
BALL_DIAMETER = 15
BALL_RADIUS = BALL_DIAMETER / 2
HORIZONTAL_WALL_X_LEFT = WINDOW_WIDTH - WINDOW_WIDTH        # x location of left of horizontal wall
HORIZONTAL_WALL_X_RIGHT = WINDOW_WIDTH                      # x location of right of horizontal wall
HORIZONTAL_WALL_Y_TOP = WINDOW_HEIGHT - WINDOW_HEIGHT       # y location of top of vertical wall
HORIZONTAL_WALL_Y_BOTTOM = WINDOW_HEIGHT                    # y location of bottom of vertical wall
WINDOW_CENTER_X = WINDOW_WIDTH // 2                         # x location of the center of the window
WINDOW_CENTER_Y = WINDOW_HEIGHT // 2                        # x location of the center of the window


# initializing state variables
paddle_left_x = WINDOW_WIDTH - WINDOW_WIDTH         # x location of top left corner of left paddle
paddle_left_y = WINDOW_HEIGHT - WINDOW_HEIGHT       # y location of top left corner of left paddle
paddle_right_x = WINDOW_WIDTH - PADDLE_WIDTH        # x location of top left corner of right paddle
paddle_right_y = WINDOW_HEIGHT - PADDLE_LENGTH      # y location of top left corner of right paddle

# initializing the ball location to the center of the screen
ball_center_x = WINDOW_CENTER_X                     # x location of ball centre
ball_center_y = WINDOW_CENTER_Y                     # y location of ball centre

# defining end points of horizontal and vertical segments on the ball
x_left_ball = ball_center_x - BALL_RADIUS           # x location of the left of the horizontal segment on the ball
x_right_ball = ball_center_x + BALL_RADIUS          # x location of the right of the horizontal segment on the ball
y_top_ball = ball_center_y - BALL_RADIUS            # y location of the top of the vertical segment on the ball
y_bottom_ball = ball_center_y + BALL_RADIUS         # y location of the bottom of the vertical segment on the ball

# initializing the ball velocities
v_x = 0
v_y = 0


# each button is initially not pressed
pressed_a = False
pressed_z = False
pressed_k = False
pressed_m = False
pressed_q = False
pressed_space = False

# function that draws the ball
def draw_ball(ball_center_x, ball_center_y):
    disable_stroke()                # no outline
    set_fill_color(0.25, 0, 0.5)    # purple fill of the ball
    draw_circle(ball_center_x, ball_center_y, BALL_DIAMETER)


# function that draws the bars
def draw_paddles(paddle_left_x, paddle_left_y, paddle_right_x, paddle_right_y, PADDLE_WIDTH, PADDLE_LENGTH):
    disable_stroke()          # no outline
    set_fill_color(1, 0, 1)   # magenta fill
    draw_rectangle(paddle_left_x, paddle_left_y, PADDLE_WIDTH, PADDLE_LENGTH)       # left paddle drawn
    draw_rectangle(paddle_right_x, paddle_right_y, PADDLE_WIDTH, PADDLE_LENGTH)     # right paddle drawn


# recording whether or not a key has been pressed
# a key controlling the left bar and a key controlling the right bar can be simultaneously pressed,
# allowing simultaneous movement
def key_down(key):
    global pressed_a, pressed_z, pressed_k, pressed_m, pressed_space, pressed_q, game_is_running

    if key == 'a':
        pressed_a = True
    elif key == 'z':
        pressed_z = True
    if key == 'k':
        pressed_k = True
    elif key == 'm':
        pressed_m = True
    if key == 'q':
        pressed_q = True
    if key == ' ' and not game_is_running:          # the game will start running when the space bar key is pressed,
        game_is_running = True                      # however, the space bar will only be able to get the game running
        pressed_space = True                        # if it is pressed while the game is currently not running


# recording whether or not a key has been released
def key_up (key):
    global pressed_a, pressed_z, pressed_k, pressed_m, pressed_space, game_is_running

    if key == 'a':
        pressed_a = False
    elif key == 'z':
        pressed_z = False
    if key == 'k':
        pressed_k = False
    elif key == 'm':
        pressed_m = False


# general function which determines whether the horizontal/vertical line segment of the ball is colliding with the
# vertical/horizontal wall/paddles
def segment_intersection(x_segment_left, x_segment_right, x_segment_middle, y_segment_middle, y_segment_top,
                         y_segment_bottom):
    return (x_segment_left <= x_segment_middle <= x_segment_right) and (y_segment_top <= y_segment_middle
                                                                        <= y_segment_bottom)


# determining whether the ball is hitting the horizontal top wall by using the general intersection formula
def hit_horizontal_wall_top():
    global ball_center_x, ball_center_y
    return segment_intersection(HORIZONTAL_WALL_X_LEFT, HORIZONTAL_WALL_X_RIGHT, ball_center_x, HORIZONTAL_WALL_Y_TOP,
                                ball_center_y - BALL_RADIUS, ball_center_y + BALL_RADIUS)


# determining whether the ball is hitting the horizontal bottom wall by using the general intersection formula
def hit_horizontal_wall_bottom():
    global ball_center_x, ball_center_y
    return segment_intersection(HORIZONTAL_WALL_X_LEFT, HORIZONTAL_WALL_X_RIGHT, ball_center_x,
                                HORIZONTAL_WALL_Y_BOTTOM, ball_center_y - BALL_RADIUS, ball_center_y + BALL_RADIUS)


# determining whether the ball is hitting the left paddle by using the general intersection formula
def hit_left_paddle():
    global ball_center_x, ball_center_y, BALL_RADIUS, paddle_left_x, paddle_left_y, PADDLE_LENGTH, PADDLE_WIDTH
    return segment_intersection(ball_center_x - BALL_RADIUS, ball_center_x + BALL_RADIUS, paddle_left_x + PADDLE_WIDTH,
                                ball_center_y, paddle_left_y, paddle_left_y + PADDLE_LENGTH)


# determining whether the ball is hitting the right paddle by using the general intersection formula
def hit_right_paddle():
    global ball_center_x, ball_center_y, BALL_RADIUS, paddle_left_x, paddle_left_y, PADDLE_LENGTH, PADDLE_WIDTH
    return segment_intersection(ball_center_x - BALL_RADIUS, ball_center_x + BALL_RADIUS, paddle_right_x, ball_center_y,
                                paddle_right_y, paddle_right_y + PADDLE_LENGTH)


# determining whether the ball is hitting the left wall by using the general intersection formula
def hit_left_wall():
    global ball_center_x, ball_center_y, BALL_RADIUS, HORIZONTAL_WALL_Y_TOP, HORIZONTAL_WALL_Y_BOTTOM
    return segment_intersection(ball_center_x - BALL_RADIUS, ball_center_x + BALL_RADIUS, HORIZONTAL_WALL_X_LEFT,
                                ball_center_y, HORIZONTAL_WALL_Y_TOP, HORIZONTAL_WALL_Y_BOTTOM)


# determining whether the ball is hitting the right wall by using the general intersection formula
def hit_right_wall():
    global ball_center_x, ball_center_y, BALL_RADIUS
    return segment_intersection(ball_center_x - BALL_RADIUS, ball_center_x + BALL_RADIUS, HORIZONTAL_WALL_X_RIGHT,
                                ball_center_y, HORIZONTAL_WALL_Y_TOP, HORIZONTAL_WALL_Y_BOTTOM)


# setting the velocity of the ball to zero when the game ends
def end_game():
    global v_x, v_y, game_is_running
    v_x = 0
    v_y = 0
    game_is_running = False


# setting the initial state of the game to false
game_is_running = False


# rendering a frame of the animation
def graphics():
    global paddle_left_x, paddle_left_y, paddle_right_x, paddle_right_y, ball_center_x, ball_center_y, V_Y, V_X,\
            pressed_space, v_x, v_y, WINDOW_CENTER_X, WINDOW_CENTER_Y
    clear()                     # clearing the graphics screen
    set_clear_color(0, 1, 1)    # cyan background color

    # drawing the paddles and the ball
    draw_paddles(paddle_left_x, paddle_left_y, paddle_right_x, paddle_right_y, PADDLE_WIDTH, PADDLE_LENGTH)
    draw_ball(ball_center_x, ball_center_y)

    # changing the direction of the vertical component of the velocity if the top or bottom wall is hit
    if hit_horizontal_wall_top():
        v_y = -v_y
    if hit_horizontal_wall_bottom():
        v_y = -v_y

    # changing the direction of the horizontal component of the velocity if the left or right paddle is hit
    # the ball moves more than the ball radius away from the bar when it makes contact in order to fix the
    # jittery motion of the ball
    if hit_left_paddle():
        v_x = -v_x
        ball_center_x = ball_center_x + BALL_RADIUS*1.2
    if hit_right_paddle():
        v_x = -v_x
        ball_center_x = ball_center_x - BALL_RADIUS*1.2

    # allowing the window to close if the key 'q' is pressed
    if pressed_q:
        cs1_quit()

    # updating the position of the ball if the game is running
    if game_is_running:
        ball_center_y += v_y
        ball_center_x += v_x

    # once the space key is pressed while the game is not running, it is set to false and the game is restarted by
    # setting the current ball velocity to the constant velocity and by returning it to the center of the screen.
    # The paddles are also returned to the start positions.
    if pressed_space:
        pressed_space = False
        v_x = V_X
        v_y = V_Y
        ball_center_x = WINDOW_CENTER_X
        ball_center_y = WINDOW_CENTER_Y
        paddle_left_x = WINDOW_WIDTH - WINDOW_WIDTH
        paddle_left_y = WINDOW_HEIGHT - WINDOW_HEIGHT
        paddle_right_x = WINDOW_WIDTH - PADDLE_WIDTH
        paddle_right_y = WINDOW_HEIGHT - PADDLE_LENGTH

    # if the a key is pressed, the left paddle is moved upwards
    if pressed_a:
        if paddle_left_y > 0:
            paddle_left_y -= PADDLE_SPEED

    # if the z key is pressed, the left paddle is moved downwards
    elif pressed_z:
        if paddle_left_y < (WINDOW_HEIGHT - 80):
            paddle_left_y += PADDLE_SPEED

    # if the k key is pressed, the right paddle is moved upwards
    if pressed_k:
        if paddle_right_y > 0:
            paddle_right_y -= PADDLE_SPEED

    # if the m key is pressed, the right paddle is moved downwards
    elif pressed_m:
        if paddle_right_y < (WINDOW_HEIGHT - 80):
            paddle_right_y += PADDLE_SPEED

    # the game ends when the ball hits either the left or the right wall
    if hit_left_wall() or hit_right_wall():
        end_game()

    # the starting instructions appears on the screen while the game is not in progress
    if not game_is_running:
        enable_stroke()
        draw_text('Press space to start a new game', 100, 100)


start_graphics(graphics, title='Atari Pong', width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
               framerate=50, key_press=key_down, key_release=key_up)