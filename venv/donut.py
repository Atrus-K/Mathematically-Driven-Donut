import os
from math import cos, sin
import pygame

White = (255, 255, 255)

Black = (0, 0, 0)

os.environ['SDL_VIDEO_CENTERED'] = '1'
Resolution = Width, Height = 1200, 1000
FPS = 60

pixel_width = 20
pixel_height = 20

x_pixel = 0
y_pixel = 0

screen_width = Width //pixel_width
screen_height = Height// pixel_height
screen_size = screen_width*screen_height

A, B = 0, 0 


theta_spacing = 7
phi_spacing = 2
chars = ".,-~:;=!*#$@"

R1 = 10
R2 = 20
K2 = 500
K1 = screen_height * K2 * 3 / (8 * (R1+ R2))
print(K1)







pygame.init()

screen = pygame.display.set_mode(Resolution)
clock = pygame.time.Clock()
#pygame.display.set_caption('Donut')
font = pygame.font.SysFont('Arial', 20, bold=True)

def text_display(char, x, y):
    text = font. render(str(char), True, White)
    text_rect = text.get_rect(center = (x,y))
    screen.blit(text, text_rect)




    

k = 0
paused = False
running = True
while running:
    clock.tick(FPS)
    pygame.display.set_caption("Donut")
    #pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))
    screen.fill(Black)

    output = [' '] * screen_size
    zBuffer = [0] * screen_size


    for theta in range(0, 628, theta_spacing):
        for phi in range(0, 628, phi_spacing):

            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi = cos(phi)
            sinphi = sin(phi)

            # x and y cooridnated before toration

            circle_x = R2 + R1 * costheta
            circle_y = R1 * sintheta
            
            #3d xyz coords after rotation
            # lè donut
            # addind rotational matricies
            x = circle_x * (cosB * cosphi + sinA * sinB * sinphi) - circle_y * cosA * sinB
            y = circle_x * (sinB * cosphi - sinA * cosB * sinphi) + circle_y * cosA * cosB
            z = K2 + cosA + circle_x * sinphi + circle_y * sinA
            z_reciprocal = 1 / z




            # x and y projection    
            x_proj = int(screen_width / 2 + K1 * z_reciprocal * x)
            y_proj = int(screen_height / 2 - K1 * z_reciprocal * y )


            position = x_proj + screen_width * y_proj

            # luminance calculation( L ranges from -sqrt2, to sqrt2 ) - essentially this is how " bright " or dark the characters ust be relative
            # to the viewer
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * ( cosA * sintheta- costheta * sinA * sinphi)
            

            if z_reciprocal > zBuffer[position]:
                zBuffer[position] = z_reciprocal # the larger the reciprocal the closeth the pixel is to the viewer and in turn the light source ans as such needs to be brighter
                luminance_index = int( L * 8 + 0.5) #this is done to get a lumonance index rance from 0 ==> 11 which matches the ascii characters we are using as pixels
                output[position] = chars[luminance_index if luminance_index > 0 else 0]

                








    



    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display(output[k], x_pixel, y_pixel)
            k+=1

        x_pixel = 0
    y_pixel = 0
    k = 0

    A += 0.15
    B += 0.035



    if not paused: 
        pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                paused = not paused
    


