"""
data, header=read('C:\\Users\\lil18\\Downloads\\DTIBrain.nrrd',index_order='F')
header:
OrderedDict([('type', 'float'),
             ('dimension', 4),
             ('space', 'right-anterior-superior'),
             ('sizes', array([  9, 144, 144,  85])),
             ('space directions', array([[    nan,     nan,     nan],
                     [-1.6667,  0.    ,  0.    ],
                     [ 0.    , -1.6667,  0.    ],
                     [ 0.    ,  0.    , -1.7   ]])),
             ('kinds', ['3D-matrix', 'domain', 'domain', 'domain']),
             ('endian', 'little'),
             ('encoding', 'gzip'),
             ('space origin', array([119.169, 119.169,  71.4  ])),
             ('measurement frame', array([[-1.,  0.,  0.],
                     [ 0., -1.,  0.],
                     [ 0.,  0., -1.]]))])
data.shape: (for index_order = F)
(9, 144, 144, 85)
data.shape: (for index_order = C)
(85, 144, 144, 9)
header['sizes']:
array([  9, 144, 144,  85])
data[30][75][75]=[ 8.2701148e-04, -2.2946764e-05,  3.9356088e-05, -2.2946764e-05,
        8.8675204e-04, -7.6865479e-05,  3.9356088e-05, -7.6865479e-05,
        8.4528158e-04] (for index_order = C)
"""