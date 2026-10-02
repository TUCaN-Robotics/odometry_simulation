import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

step_size = 1  # cm

# Robot parameters
wheel_diameter = 9 # cm
wheelbase = 5  # cm
encoder_resolution  = 1000 # pulses per revolution
right_wheel_angular_velocity = 0
left_wheel_angular_velocity =0

# Initial position and orientation of the robot
x, y, theta = 0.0, 0.0, 0.0
poses = [(x, y, theta)]  # Store the robot's path

# User input for square size
square_size = random.randrange(80, 200)

# Function to move the robot forward
def move_forward(distance):
    global x, y, theta
    steps = int(distance / step_size)
    for _ in range(steps):
        dx = step_size * math.cos(theta)
        dy = step_size * math.sin(theta)
        x += dx
        y += dy
        poses.append((x, y, theta))

# Function to turn the robot 90 degrees to the left
def turn_left(angle_rad):
    global theta
    steps = int(abs(angle_rad) / math.radians(5))  # 5° per step
    dtheta = angle_rad / steps
    for _ in range(steps):
        theta += dtheta
        poses.append((x, y, theta))  # Turning in place, position stays the same

# Drive the robot in a square path
for _ in range(4):
    move_forward(square_size)  # Move forward by the size of the square
    turn_left(math.radians(90))  # Turn 90 degrees after each side

# --- Animation Setup ---
fig, ax = plt.subplots()
ax.set_aspect('equal')
margin = square_size * 0.5
ax.set_xlim(-margin, square_size + margin)
ax.set_ylim(-margin, square_size + margin)
ax.set_yticklabels([])
ax.set_xticklabels([])
line, = ax.plot([], [], 'b-', linewidth=0)
dot, = ax.plot([], [], 'ro', markersize=8)

# Initialize the plot
def init():
    line.set_data([], [])
    dot.set_data([], [])
    return line, dot

# Update the plot for each frame
def update(frame):
    if frame == 0:
        # At the first frame, just plot the initial position
        x_data, y_data, theta_data  = [poses[0][0]], [poses[0][1]], [poses[0][2]]
    else:
        x_data, y_data, theta_data = zip(*poses[:frame+1])  # Plot all positions up to the current frame
    line.set_data(x_data, y_data)
    dot.set_data([x_data[-1]], [y_data[-1]])  # Make sure these are sequences
    print (f"\r {x_data[-1]:3.2f}  {y_data[-1]:3.2f}  {math.degrees(theta_data[-1]):3.2f}", end='')
    return line, dot

# Set up the animation
ani = animation.FuncAnimation(
    fig, update,
    frames=len(poses),
    init_func=init,
    interval=30,
    blit=True,
    repeat=False
)

plt.title("Robot Following Square Path Using Odometry")
plt.xlabel("X Position (cm)")
plt.ylabel("Y Position (cm)")
plt.grid(False)
plt.show()
