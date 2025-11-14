## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

"""
"""
class Player:

  '''
  '''
  m_Plays = None
  
  '''
  '''
  
  def __init__( self, args ):
    pass
  # end def

  '''
  '''
  def choose_cell( self, w, h, n ):
    c = ''
    while len( c ) != 2:
      c = input( "Choose a cell: " ).lower( )
    # end while
    return ( int( c[ 1 ] ), ord( c[ 0 ] ) - ord( 'a' ) )
  # end def

  '''
  '''
  def report( self, i, j, n ):
    pass
  # end def

# end class

## eof - Human.py
