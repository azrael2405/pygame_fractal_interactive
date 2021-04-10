import numpy
from numba import njit
import pygame as pg


def mandelbrot(screen_width, screen_height, w_values, h_values, resolution):
  '''
  Generate mandelbrot set
  '''
  print('Generating Mandelbrot set for coordinates x0: {:.2f}, x1: {:.2f}, y0: {:.2f}, y1:{:.2f}'.format(
    w_values[0],
    w_values[1],
    h_values[0],
    h_values[1]
  ))
  result = pg.PixelArray(pg.Surface((screen_width, screen_height)))
  
  for row_index, Re in enumerate(numpy.linspace(h_values[0], h_values[1], num=screen_height)):
    for column_index, Im in enumerate(numpy.linspace(w_values[0], w_values[1], num=screen_width)):
      mb_value = generate_mandelbrot(Re, Im, resolution)
      color = pg.Color((0,0,0))
      hue = 360.0 * mb_value / resolution
      saturation = 100.0
      value = 100.0 if mb_value < resolution else 0.0
      color.hsva = (hue, saturation, value, 100.0)
      result[column_index, row_index] = color

  return result

@njit
def generate_mandelbrot(Re, Im, max_iter):
  c = complex(Re, Im)
  z = 0.0j

  for i in range(max_iter):
    z = z*z + c
    if (z.real**2 + z.imag**2) >= 4:
      return i
  return max_iter




