## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## Modified By:
## @author Simon Díaz Monroy (simondiaz@javeriana.edu.co)
## @author Katheryn Sofia Guasca Chavarro (katheryn.guascar@javeriana.edu.co)
## =========================================================================

import pandas as pd
from sklearn.linear_model import LogisticRegression

"""
"""
class Player:

  '''
  '''
  m_Marks = None
  m_Plays = []
  m_Width = 0
  m_Height = 0
  m_NumberOfMines = 0

  '''
  '''
  def __init__( self, args ):
    self.train_model()
    pass
  # end def
  
  '''
  '''
  def train_model(path_x="../game_x.csv", path_y="../game_y.csv"):
    X = pd.read_csv(path_x)
    y = pd.read_csv(path_y)["mina_encontrada"]
    model = LogisticRegression(max_iter=500)
    model.fit(X, y)
    return model

  '''
  '''
  
  def choose_cell( self, w, h, n ):

    # Init game state
    if self.m_Marks is None:
      self.m_Marks = [ [ False for j in range( h ) ] for i in range( w ) ]
      self.m_Width = w
      self.m_Height = h
      self.m_NumberOfMines = n
    # end if

    # Choose a play
    if len( self.m_Plays ) > 0:
      o = self.m_Plays[ -1 ]
      self.m_Plays.pop( )
      return o
    else:
      c = ''
      while len( c ) != 2:
        c = input( "Choose a cell: " ).lower( )
      # end while
      return ( int( c[ 1 ] ), ord( c[ 0 ] ) - ord( 'a' ) )
    # end if
  # end def

  '''
  '''
  def report( self, i, j, n ):
    self.m_Marks[ i ][ j ] = True
    if n == 0:
      for k in range( -1, 2 ):
        for l in range( -1, 2 ):
          ni = i + k
          nj = j + l
          if ni >= 0 and ni < self.m_Width and nj >= 0 and nj < self.m_Height:
            if self.m_Marks[ ni ][ nj ] == False:
              self.m_Plays += [ ( ni, nj ) ]
            # end if
          # end if
        # end for
      # end for
    # end if
  # end def
  
  def neighbors(w, h, i, j):
    """
    Genera todos los vecinos (8 casillas adjacentes) de (i,j) dentro del tablero.
    - Doble for sobre el rango [i-1, i+1] x [j-1, j+1]
    Retorna: lista de (x, y)
    """
    neighbors_list = []
    # Ciclo externo: x en {i-1, i, i+1}
    for x in range(i - 1, i + 2):
        # Ciclo interno: y en {j-1, j, j+1}
        for y in range(j - 1, j + 2):
            if (x, y) != (i, j) and 0 <= x < w and 0 <= y < h:
                neighbors_list.append((x, y))
            #end if
        #end for
    # end for
    return neighbors_list

  # end def

# end class

## eof - HumanWithZeroFilling.py
