import numpy as np

class Fillzone:
  ''' Clase que define un juego de fillzone, tiene su estado y sus acciones para modificar este.'''
  def __init__(self, n, k):
    self.state = np.random.randint(0, k, size=(n, n), dtype='u4')

  # se me ocurre algo asi recursivo pero me parece que estoy paveando, ademas debe ser re costoso
  def change(self, x, y, number):
    old = self.state[x][y]
    if x > 0 and self.state[x-1, y] == old:
      change(self, x-1, y, number)

  # aca esta el temita, debe estar en internet, pero hay que escribir el algo que cambie todos los adyacentes
  def process(self, number):
    '''Modifica el estado acorde al numero que se ingreso'''
    change(self, 0, 0, number)



game = Fillzone(14, 6)
print(game.state)