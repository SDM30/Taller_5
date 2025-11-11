## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import numpy, pandas, sys

# Read coefficients
coeffs_fs = open( sys.argv[ 1 ] )
coeffs = [ float( v ) for v in coeffs_fs.read( ).split( ) ]
coeffs_fs.close( )

# Build model
W = numpy.matrix( coeffs[ 1 : ] ).reshape( -1, 1 ) * -1.0 # Pesos del modelo
b = numpy.array( [ coeffs[ 0 ] ] ).reshape( 1, ) # Sesgos

# Test model
X = pandas.read_csv( sys.argv[ 2 ], sep = ',', header = None ).to_numpy( )
zp = 1.0 / ( 1.0 + numpy.exp( ( X @ W ) + b ) )
yp = 1.0 - ( zp < 0.5 ).astype( float )

print( zp.T )
print( yp.T )

## eof - test_model.py
