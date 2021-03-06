#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from math import *
from superpose3d import Superpose3D

def test_superpose3d():
    X=[[0,0,0],[0,0,1],[0,1,1],[1,1,1]]
    x=[[0,0,0],[0,1,0],[0,1,-1],[1,1,-1]]  # (=X after rotation around the Z axis)
    result = Superpose3D(X,x)
    assert(abs(result[0]) < 1.0e-6)

    Xshifted = [ [X[i][0],X[i][1]+100, X[i][2]] for i in range(0,len(X))]
    xscaled  = [ [2*x[i][0],2*x[i][1],    2*x[i][2]] for i in range(0,len(x))]
    xscshift = [ [2*x[i][0],2*x[i][1]+200,2*x[i][2]] for i in range(0,len(x))]

    # Now try again using the translated, rescaled coordinates:

    result = Superpose3D(X, xscshift, None, True)

    # Does the RMSD returned in result[0] match the RMSD calculated manually?
    R = np.matrix(result[1])              # rotation matrix
    T = np.matrix(result[2]).transpose()  # translation vector (3x1 matrix)
    c = result[3]                         # scalar
    _x = np.matrix(xscshift).transpose()
    _xprime = c*R*_x + T
    xprime = np.array(_xprime.transpose()) # convert to length 3 numpy array

    print('1st (frozen) point cloud:\n'+str(X))
    print('2nd (mobile) point cloud:\n'+str(xscshift))
    print('2nd (mobile) point cloud after scale(c), rotation(R), translation(T):\n' +
          str(xprime))
    print('rmsd = '+str(result[0]))
    print('scale (c) = '+str(result[3]))
    print('rotation (R) = \n'+str(result[1]))
    print('translation (T) = '+str(result[2]))
    print('transformation used: x_i\' = Sum_over_j c*R_ij*x_j + T_i')

    RMSD = 0.0
    for i in range(0, len(X)):
        RMSD += ((X[i][0] - xprime[i][0])**2 +
                 (X[i][1] - xprime[i][1])**2 +
                 (X[i][2] - xprime[i][2])**2)

    RMSD = sqrt(RMSD / len(X))
    assert(abs(RMSD - result[0]) < 1.0e-6)


def main():
    test_superpose3d()


if __name__ == '__main__':
    main()
