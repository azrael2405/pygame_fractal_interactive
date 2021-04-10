import pygame
import time

from mandelbrot import mandelbrot
from pos_funcs import get_quadrat, get_new_values_quadrat


def create_mandelbrot(screen, screen_width, screen_height, w_values, h_values, resolution):
  next_pixelarray = mandelbrot(screen_width, screen_height, w_values, h_values, resolution)
  surf = next_pixelarray.surface
  del next_pixelarray
  surf_center = (
    (screen_width-surf.get_width())/2,
    (screen_height-surf.get_height())/2
  )
  screen.blit(surf, surf_center)
  pygame.display.flip()
  return surf


def main(screen_width, screen_height):
  pygame.init()
  screen = pygame.display.set_mode([screen_width, screen_height])

  running = True
  screen.fill((0,0,0))
  orig_h_values = [-2.25, 0.75]
  orig_w_values = [-1.5, 1.5]
  h_values = list(orig_h_values)
  w_values = list(orig_w_values)
  resolution = 1000

  step = 0.1
  mouse_state = 0
  mouse_pos1 = (0, 0)
  mandelbrot_surface = create_mandelbrot(screen, screen_width, screen_height, w_values, h_values, resolution)
  while running:
    # capture events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        
        if mouse_state == 0:
          mouse_state = 1
          mouse_pos1 = pygame.mouse.get_pos()
        elif mouse_state == 1:
          mouse_state = 0
          mouse_pos2 = pygame.mouse.get_pos()
          
          (w_values, h_values) = get_new_values_quadrat(
            w_values,
            h_values,
            mouse_pos1,
            mouse_pos2,
            screen_width,
            screen_height
          )


          # (w_length, h_length) = get_lengths(
          #   mouse_pos1,
          #   mouse_pos2,
          #   screen_width,
          #   screen_height
          # )
          # w_resolution = w_length / screen_width
          # h_resolution = h_length / screen_height

          # w_values = list(map(lambda x: x* w_resolution, w_values))
          # h_values = list(map(lambda x: x* h_resolution, h_values))
          
          mandelbrot_surface = create_mandelbrot(
            screen,
            screen_width,
            screen_height,
            w_values,
            h_values,
            resolution
          )
          mouse_pos1 = (0,0)
          mouse_pos2 = (0,0)
        print('mouse_state: {}'.format(mouse_state))
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False
        elif event.key == pygame.K_r:
          h_values = list(orig_h_values)
          w_values = list(orig_w_values)
        elif event.key == pygame.K_PLUS:
          step *= 10
          print('step factor = {}'.format(step))
        elif event.key == pygame.K_MINUS:
          step /= 10
          print('step factor = {}'.format(step))
        elif event.key == pygame.K_w:
          h_values = list(map(lambda x: x - step, h_values))
        elif event.key == pygame.K_a:
          w_values = list(map(lambda x: x - step, w_values))
        elif event.key == pygame.K_s:
          h_values = list(map(lambda x: x + step, h_values))
        elif event.key == pygame.K_d:
          w_values = list(map(lambda x: x + step, w_values))
        elif event.key == pygame.K_e:
          h_values = list(map(lambda x: x / 1.1, h_values))
          w_values = list(map(lambda x: x / 1.1, w_values))
        elif event.key == pygame.K_q:
          h_values = list(map(lambda x: x * 1.1, h_values))
          w_values = list(map(lambda x: x * 1.1, w_values))
        mandelbrot_surface = create_mandelbrot(screen, screen_width, screen_height, w_values, h_values, resolution)
          
    if mouse_state == 1:
      cur_mouse_pos = pygame.mouse.get_pos()
      
      mouse_screen = pygame.Surface((screen.get_size()))
      mouse_screen.set_alpha(100)
      
      corners = get_quadrat(
        mouse_pos1,
        cur_mouse_pos
      )
      
      
      

      pygame.draw.lines(
        mouse_screen,
        (255,255,255),
        True,
        corners,
        2
      )

      # pygame.draw.rect(
      #   screen,
      #   (255, 255, 255),
      #   (
      #     mouse_pos1[0],
      #     mouse_pos1[1],
      #     w_length,
      #     h_length
      #   )
      # )
      surf_center = (
        (screen_width - mouse_screen.get_width()) / 2,
        (screen_height - mouse_screen.get_height()) / 2
      )
      mandelbrot_center = (
        (screen_width - mandelbrot_surface.get_width()) / 2,
        (screen_height - mandelbrot_surface.get_height()) / 2
      )
      
      screen.blit(mandelbrot_surface, mandelbrot_center)
      screen.blit(mouse_screen, surf_center)
      pygame.display.update()
    # fill background white
    

    # draw circle
    # pygame.draw.circle(screen, color[curColor%3], (width/2, height/2), 75)

    # create surface and get rectangle
    # surf = pygame.Surface((50,50))
    # surf.fill(color[curColor])
    # rect = surf.get_rect()
    # surf_center = (
    #   (screen_width-surf.get_width())/2,
    #   (screen_height-surf.get_height())/2
    # )

    # screen.blit(surf, surf_center)

    # #flip display (updates whole screen)
    # pygame.display.flip()



if __name__ == '__main__':
  main(800, 600)