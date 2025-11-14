## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import random

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

    # Init game state
    if self.m_Plays is None:
      self.m_Plays = []
      for i in range( w ):
        for j in range( h ):
          self.m_Plays += [ ( i, j ) ]
        # end for
      # end for
    # end if

    # Choose a play
    random.shuffle( self.m_Plays )
    if len( self.m_Plays ) > 0:
      o = self.m_Plays[ -1 ]
      self.m_Plays.pop( )
      return o
    # end if
  # end def

  '''
  '''
  def report( self, i, j, n ):
    pass
  # end def

# end class

## eof - Random.py
