## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import importlib.util, sys
from Board import *

'''
'''
def ImportLibrary( module_name, filename ):
  spec = importlib.util.spec_from_file_location( module_name, filename )
  if spec is None:
    print( f'Error: Could not create module specification for {filename}' )
    return None
  # end if
  module = importlib.util.module_from_spec( spec )
  sys.modules[ module_name ] = module
  try:
    spec.loader.exec_module( module )
    return module
  except Exception as e:
    print( f'Error executing module {filename}: {e}' )
    del sys.modules[ module_name ]
  # end try
  return None
# end def

"""
"""
if __name__ == '__main__':

  if len( sys.argv ) < 5:
    print(
      "Usage: python3", sys.argv[ 0 ], "width height mines player [--record-data] <player arguments>"
      )
    sys.exit( 1 )
  # end if
  w = int( sys.argv[ 1 ] )
  h = int( sys.argv[ 2 ] )
  m = int( sys.argv[ 3 ] )
  player_fname = sys.argv[ 4 ]
  player_args = sys.argv[ 5 : ]

  record_play_data = False
  if '--record-data' in player_args:
    record_play_data = True
    player_args = [ arg for arg in player_args if arg != '--record-data' ]
  # end if

  # Load player
  player_lib = ImportLibrary( 'Player', player_fname )
  player = player_lib.Player( player_args )

  # Create board
  board = Board( w, h, m, record_play_data = record_play_data )

  # Play!
  while not board.have_finished( ):
    print( board )
    i, j = player.choose_cell( w, h, m )
    print( 'Cell =', i, j )
    n = board.click( i, j )
    player.report( i, j, n )
  # end while

  print( '====================================================' )
  print( board )
  if board.have_won( ):
    print( "You won!" )
  elif board.have_lose( ):
    print( "You lose :-(" )
  # end if
  print( f"Plays made: {board.play_count( )}" )
  print( '====================================================' )

# end if

## eof - MineSweeper.py
