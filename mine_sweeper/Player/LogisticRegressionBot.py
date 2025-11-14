## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## Modified By:
## @author Simon Díaz Monroy (simondiaz@javeriana.edu.co)
## @author Katheryn Sofia Guasca Chavarro (katheryn.guascar@javeriana.edu.co)
## =========================================================================

import os
import random

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
  brain = None
  m_RevealedValues = None
  feature_names = None

  '''
  '''
  def __init__( self, args ):
    self.brain = self.train_model()
    self.m_Plays = []
    self.m_RevealedValues = {}
  # end def
  
  '''
  '''
  def train_model(self, path_x="../game_x.csv", path_y="../game_y.csv"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    x_path = os.path.abspath(os.path.join(base_dir, path_x))
    y_path = os.path.abspath(os.path.join(base_dir, path_y))
    X = pd.read_csv(x_path)
    self.feature_names = list(X.columns)
    y = pd.read_csv(y_path)["mina_encontrada"]
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
      # Primera jugada: escoger una casilla aleatoria
      return ( random.randrange( w ), random.randrange( h ) )
    # end if

    # Choose a play usando el modelo
    if len( self.m_Plays ) > 0:
      filtered = [ cell for cell in self.m_Plays if not self.m_Marks[ cell[ 0 ] ][ cell[ 1 ] ] ]
      if len( filtered ) > 0:
        return self._choose_from_candidates( filtered )
      else:
        self.m_Plays = []
    # end if

    candidates = self._collect_frontier_cells( )
    if len( candidates ) > 0:
      return self._choose_from_candidates( list( candidates ) )
    # Si no hay frontera conocida, volver a elegir al azar
    return self._random_unknown_cell( )
  # end def

  '''
  '''
  def report( self, i, j, n ):
    self.m_Marks[ i ][ j ] = True
    self.m_RevealedValues[ ( i, j ) ] = n
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
  
  @staticmethod
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

  def _collect_frontier_cells( self ):
    frontier = set()
    for ( i, j ) in self.m_RevealedValues.keys( ):
      for cell in self.neighbors( self.m_Width, self.m_Height, i, j ):
        if not self.m_Marks[ cell[ 0 ] ][ cell[ 1 ] ]:
          frontier.add( cell )
        # end if
      # end for
    # end for
    return frontier
  # end def

  def _choose_from_candidates( self, candidates ):
    best_cell = None
    best_prob = None
    for cell in candidates:
      features = self._build_neightbor_vector( cell[ 0 ], cell[ 1 ] )
      features_df = pd.DataFrame( [ features ], columns = self.feature_names )
      prob = self.brain.predict_proba( features_df )[ 0 ][ 1 ]
      if best_prob is None or prob < best_prob:
        best_prob = prob
        best_cell = cell
      # end if
    # end for
    if best_cell is not None:
      try:
        self.m_Plays.remove( best_cell )
      except ValueError:
        pass
      # end try
      return best_cell
    # end if
    return self._random_unknown_cell( )
  # end def

  def _build_neightbor_vector( self, i, j ):
    features = []
    for x in range( i - 1, i + 2 ):
      for y in range( j - 1, j + 2 ):
        if x == i and y == j:
          continue
        if x >= 0 and x < self.m_Width and y >= 0 and y < self.m_Height:
          if ( x, y ) in self.m_RevealedValues:
            features.append( self.m_RevealedValues[ ( x, y ) ] )
          else:
            features.append( 9 )
          #end if
        else:
          features.append( -1 )
        # end if
      # end for
    # end for
    return features
  # end def

  def _random_unknown_cell( self ):
    unknown = []
    for i in range( self.m_Width ):
      for j in range( self.m_Height ):
        if not self.m_Marks[ i ][ j ]:
          unknown.append( ( i, j ) )
        # end if
      # end for
    # end for
    if len( unknown ) == 0:
      return ( 0, 0 )
    return random.choice( unknown )
  # end def

# end class

## eof - HumanWithZeroFilling.py
