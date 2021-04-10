from numpy import imag


def get_lengths(pos1, pos2, screen_width, screen_height):
  w_length = abs(pos2[0] - pos1[0])
  h_length = abs(pos2[1] - pos1[1])
  length = max(w_length, h_length)
  screen_resolution = screen_width/screen_height
  if w_length > h_length:
    h_length = length / screen_resolution
  else:
    w_length = length * screen_resolution
  return (w_length, h_length)


def get_quadrat(pos1, pos2):
  length = max(
    abs(pos2[0] - pos1[0]),
    abs(pos2[1] - pos1[1])
  )
  return [
    (pos1[0] - length, pos1[1] - length),
    (pos1[0] + length, pos1[1] - length),
    (pos1[0] + length, pos1[1] + length),
    (pos1[0] - length, pos1[1] + length),
  ]


def get_rect(pos1, pos2, screen_width, screen_height):
  (w_length, h_length) = get_lengths(pos1, pos2, screen_width, screen_height)

  vertical = 1
  horizontal = 1
  topLeft = (0, 0)
  topRight = (0, 0)
  bottomRight = (0, 0)
  bottomLeft = (0, 0)

  if (pos2[0] - pos1[0]) < 0:
    vertical = -1
  if (pos2[1] - pos1[1]) < 0:
    horizontal = -1
  if horizontal > 0 and vertical > 0:
    topLeft = pos1
    topRight = (pos1[0] + w_length, pos1[1])
    bottomRight = (pos1[0], pos1[1] + h_length)
    bottomLeft = (pos1[0] + w_length, pos1[1] + h_length)
  elif horizontal < 0 and vertical > 0:
    topLeft = (pos1[0] + w_length, pos1[1] - h_length)
    topRight = (pos1[0], pos1[1] - h_length)
    bottomRight = (pos1[0] + w_length, pos1[1])
    bottomLeft = pos1
  elif horizontal > 0 and vertical < 0:
    topLeft = pos1
    topRight = (pos1[0] - w_length, pos1[1])
    bottomRight = (pos1[0], pos1[1] + h_length)
    bottomLeft = (pos1[0] - w_length, pos1[1] + h_length)
  elif horizontal < 0 and vertical < 0:
    topLeft = (pos1[0], pos1[1] - h_length)
    topRight = (pos1[0] - w_length, pos1[1] - h_length)
    bottomRight = pos1
    bottomLeft = (pos1[0] - w_length, pos1[1])

  corners = [
    topLeft,
    topRight,
    bottomLeft,
    bottomRight
  ]

  return corners


def get_new_values_quadrat(w_values, h_values, pos1, pos2, screen_width, screen_height):
  rect = get_quadrat(pos1, pos2)
  length = max(
    abs(pos2[0] - pos1[0]),
    abs(pos2[1] - pos1[1])
  )
  print('length:', length)
  (x_min, x_max) = w_values
  (y_min, y_max) = h_values
  factor = length / screen_width
  realpart = complex_transform(pos1[0], screen_width, x_max, x_min)
  imaginarypart = complex_transform(pos1[1], screen_height, y_max, y_min)
  print('x:', x_min, realpart, x_max)
  print('y:', y_min, imaginarypart, y_max)
  w_values[0] = interpolate(realpart, x_min, set_interpolation(factor))
  w_values[1] = interpolate(realpart, x_max, set_interpolation(factor))
  h_values[0] = interpolate(imaginarypart, y_min, set_interpolation(factor))
  h_values[1] = interpolate(imaginarypart, y_max, set_interpolation(factor))
  return (w_values, h_values)


def complex_transform(position, size, max, min):
  return min + (position * ((max - min) / size))


def interpolate(start, end, interpolation):
  return start + ((end - start) * interpolation)


def set_interpolation(factor):
  return 1.0/factor if factor > 1.0 else 1.0 * factor
