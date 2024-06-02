import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in a Circle")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Clock object to control frame rate
clock = pygame.time.Clock()

# Circle properties
circle_center = (width // 2, height // 2)
circle_radius = 300

# Ball properties
ball_radius = 10
ball_pos = [circle_center[0] - circle_radius / 2, circle_center[1]]
ball_speed = [0.1, 0]  # Initial horizontal speed and zero vertical speed
ball_growth = 1.04  # Growth factor of the ball radius after each bounce
speed_increase_factor = 1.04  # Factor to increase speed after each bounce
gravity = 0.08  # Acceleration due to gravity

# Load the bounce sounds
notes = {
    "C3": pygame.mixer.Sound("C3.mp3"),
    "C#3": pygame.mixer.Sound("C#3.mp3"),
    "D3": pygame.mixer.Sound("D3.mp3"),
    "D#3": pygame.mixer.Sound("D#3.mp3"),
    "E3": pygame.mixer.Sound("E3.mp3"),
    "F3": pygame.mixer.Sound("F3.mp3"),
    "F#3": pygame.mixer.Sound("F#3.mp3"),
    "G3": pygame.mixer.Sound("G3.mp3"),
    "G#3": pygame.mixer.Sound("G#3.mp3"),
    "A3": pygame.mixer.Sound("A3.mp3"),
    "A#3": pygame.mixer.Sound("A#3.mp3"),
    "B3": pygame.mixer.Sound("B3.mp3"),
    "C4": pygame.mixer.Sound("C4.mp3"),
    "C#4": pygame.mixer.Sound("C#4.mp3"),
    "D4": pygame.mixer.Sound("D4.mp3"),
    "D#4": pygame.mixer.Sound("D#4.mp3"),
    "E4": pygame.mixer.Sound("E4.mp3"),
    "F4": pygame.mixer.Sound("F4.mp3"),
    "F#4": pygame.mixer.Sound("F#4.mp3"),
    "G4": pygame.mixer.Sound("G4.mp3"),
    "G#4": pygame.mixer.Sound("G#4.mp3"),
    "A4": pygame.mixer.Sound("A4.mp3"),
    "A#4": pygame.mixer.Sound("A#4.mp3"),
    "B4": pygame.mixer.Sound("B4.mp3")
    
}

# Define a sequence of note names, including third octave notes
note_sequence = [
    #"C4", "D#4", "F4", "F#4", "F4", "D#4", "C4", "A#3", "D#4", "C4", "G3", "C4"
    "F4", "D4", "A3", "D4", "F4", "D4", "A3", "D4", "F4", "C4", "A3", "C4", "F4", "C4", "A3", "C4", "E4", "C#4", "A3", "C#4", "E4", "C#4", "A3", "C#4"
    
]
note_index = 0

# Set number of mixer channels
pygame.mixer.set_num_channels(12)

# Create a list of channels
channels = [pygame.mixer.Channel(i) for i in range(12)]  # 12 channels for simultaneous playback

def handle_bounce(ball_pos, ball_radius, ball_speed, circle_center, circle_radius, ball_growth, speed_increase_factor):
    global note_index

    # Calculate distance from the center of the circle to the ball position
    dx = ball_pos[0] - circle_center[0]
    dy = ball_pos[1] - circle_center[1]
    distance = math.hypot(dx, dy)
    
    if distance + ball_radius > circle_radius:
        # Calculate normal vector at the point of contact
        nx = dx / distance
        ny = dy / distance
        
        # Reflect ball speed around the normal vector
        dot_product = ball_speed[0] * nx + ball_speed[1] * ny
        ball_speed[0] -= 2 * dot_product * nx
        ball_speed[1] -= 2 * dot_product * ny
        
        # Increase the ball's radius
        ball_radius *= ball_growth
        
        # Increase the ball's speed
        ball_speed[0] *= speed_increase_factor
        ball_speed[1] *= speed_increase_factor
        
        # Reposition the ball to be just outside the circle after the bounce
        overlap = (distance + ball_radius) - circle_radius
        ball_pos[0] -= overlap * nx
        ball_pos[1] -= overlap * ny
        
        # Play the next note in the sequence if it is not -1
        current_note = note_sequence[note_index]
        available_channel = channels[note_index % len(channels)]
        available_channel.play(notes[current_note])
        note_index = (note_index + 1) % len(note_sequence)  # Increment and wrap the note index

    return ball_radius

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply gravity
    ball_speed[1] += gravity

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Check for bounce and handle it
    ball_radius = handle_bounce(ball_pos, ball_radius, ball_speed, circle_center, circle_radius, ball_growth, speed_increase_factor)

    # Check if the ball's radius is twice the circle's radius
    if ball_radius >= 2 * circle_radius:
        running = False

    # Clear screen
    screen.fill(BLACK)

    # Draw the bounding circle
    pygame.draw.circle(screen, WHITE, circle_center, circle_radius, 2)

    # Draw the ball
    pygame.draw.circle(screen, BLUE, ball_pos, int(ball_radius))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
