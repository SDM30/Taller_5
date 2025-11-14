## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

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
    pass
  # end def

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

# end class

## eof - HumanWithZeroFilling.py
