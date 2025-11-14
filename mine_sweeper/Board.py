## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## Modified By:
## @author Simon Díaz Monroy (simondiaz@javeriana.edu.co)
## @author Katheryn Sofia Guasca Chavarro (ksofia.guasca@javeriana.edu.co)
## =========================================================================

import random
import csv
import os

class Board:

  m_Patches       = None
  m_Mines         = None
  m_NumberOfMines = 0
  m_Explosion     = False

  def __init__( self, w, h, n, record_play_data = True ):
    self.m_Patches = [ [ False for j in range( h ) ] for i in range( w ) ]
    self.m_Mines = [ [ 0 for j in range( h ) ] for i in range( w ) ]
    self.m_NumberOfMines = n
    self.m_Explosion = False
    self.m_PlayHistory = []
    self.m_PlayDataWritten = False
    self.m_RecordPlayData = record_play_data
    self.m_PlayCount = 0

    # Randomly choose mine locations
    t = [ i for i in range( w * h ) ]
    random.shuffle( t )
    for i in t[ 0: n ]:
      self.m_Mines[ int( i / w ) ][ i % w ] = 9
    # end for

    # Fill the remaining cells with the count of neighboring mines
    for i in range( len( self.m_Mines ) ):
      for j in range( len( self.m_Mines[ i ] ) ):
        if self.m_Mines[ i ][ j ] == 0:
          for k in range( i - 1, i + 2 ):
            if k >= 0 and k < len( self.m_Mines ):
              for l in range( j - 1, j + 2 ):
                if l >= 0 and l < len( self.m_Mines[ i ] ):
                  if self.m_Mines[ k ][ l ] == 9:
                    self.m_Mines[ i ][ j ] += 1
                  # end if
                # end if
              # end for
            # end if
          # end for
        # end if
      # end for
    # end for

  # end def

  def __str__( self ):
    s = '    '
    for k in range( len( self.m_Mines ) ):
      s += '+---'
    s += '+\n    '
    for k in range( len( self.m_Mines ) ):
      s += '| ' + str( k ) + ' '
    s += '|\n'
    for j in range( len( self.m_Mines[ 0 ] ) ):
      for k in range( len( self.m_Mines ) + 1 ):
        s += '+---'
      s += '+\n'
      s += '| ' + chr( ord( 'A' ) + j ) + ' '
      for i in range( len( self.m_Mines ) ):
        s += '| '
        if self.m_Patches[ i ][ j ]:
          if self.m_Mines[ i ][ j ] < 9:
            s += str( self.m_Mines[ i ][ j ] )
          else:
            s += 'X'
        else:
          s += ' '
        s += ' '
      s += '|\n'
    for k in range( len( self.m_Mines ) + 1 ):
      s += '+---'
    s += '+\n'
    return s
  # end def

  def __repr__( self ):
    return self.__str__( )
  # end def

  def width( self ):
    return len( self.m_Mines )
  # end def

  def number_of_mines( self ):
    return self.m_NumberOfMines
  # end def

  def height( self ):
    if len( self.m_Mines ) > 0:
      return len( self.m_Mines[ 0 ] )
    else:
      return 0
  # end def

  def have_won( self ):
    c = 0
    for i in range( len( self.m_Mines ) ):
      for j in range( len( self.m_Mines[ i ] ) ):
        if not self.m_Patches[ i ][ j ]:
          c += 1
    return c == self.m_NumberOfMines
  # end def

  def have_lose( self ):
    return self.m_Explosion
  # end def

  def have_finished( self ):
    return self.have_won( ) or self.have_lose( )
  # end def

  def click( self, i, j ):
    if not self.m_Explosion:
      if i < 0 or j < 0 or i >= self.width( ) or j >= self.height( ):
        return 0
      else:
        self.m_PlayCount += 1
        new_reveal = False
        if not self.m_Patches[ i ][ j ]:
          self.m_Patches[ i ][ j ] = True
          new_reveal = True
        if new_reveal:
          self._record_play( i, j )
        if self.m_Mines[ i ][ j ] == 9:
          self.m_Explosion = True
          self.m_Patches = [ [ True for j in range( self.height( ) ) ] for i in range( self.width( ) ) ]
        if self.have_finished( ):
          self.save_play_data( )
        return self.m_Mines[ i ][ j ]
    else:
      self.m_PlayCount += 1
      return self.m_Mines[ i ][ j ]
  # end def
  
  def _record_play( self, i, j ):
    value = self.m_Mines[ i ][ j ]
    neighbors = self._collect_neighbors( i, j )
    self.m_PlayHistory.append( ( i, j, value, neighbors ) )
  # end def

  def _collect_neighbors( self, i, j ):
    neighbors = []
    for x in range( i - 1, i + 2 ):
      for y in range( j - 1, j + 2 ):
        if x == i and y == j:
          continue
        if x >= 0 and x < self.width( ) and y >= 0 and y < self.height( ):
          neighbors.append( self.m_Mines[ x ][ y ] )
        else:
          neighbors.append( 9 )
    return neighbors
  # end def

  def save_play_data(self):
    if not self.m_RecordPlayData or len(self.m_PlayHistory) == 0:
      return

    filename_x = f'game_x.csv'
    filename_y = f'game_y.csv'

    # Check if files already exist to avoid writing duplicated headers
    file_exists_x = os.path.exists(filename_x)
    file_exists_y = os.path.exists(filename_y)

    # Save X (neighbor configurations)
    with open(filename_x, 'a', newline='') as fx:
      writer_x = csv.writer(fx)
      if not file_exists_x:
        writer_x.writerow([f"n{i}" for i in range(1, 9)])
      for play in self.m_PlayHistory:
        neighbors = play[3]
        writer_x.writerow(neighbors)

    # Save Y (whether a mine was found)
    with open(filename_y, 'a', newline='') as fy:
      writer_y = csv.writer(fy)
      if not file_exists_y:
        writer_y.writerow(["mina_encontrada"])
      for play in self.m_PlayHistory:
        valor = play[2]
        y = 1 if valor == 9 else 0
        writer_y.writerow([y])

    self.m_PlayDataWritten = True
  # end def

  def play_count( self ):
    return self.m_PlayCount
  # end def

# end class

## eof - Board.py
