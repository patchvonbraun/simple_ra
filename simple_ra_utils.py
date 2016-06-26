#
# Configuration management for Simple RA
#
# Marcus Leech, Science Radio Laboratories, Inc.
#
import os
import signal
import numpy
import math
import sys
import time
doephem=True
doserial=True
try:
    import ephem
except:
    print "PyEphem import failed.  You'll be missing LMST an other logging functionality"
    doephem=False

try:
    import serial
except:
    print "serial import failed.  You'll be missing calibration functionality"
    doserial=False
    
from gnuradio import gr

fixup_spline = [0.83,0.830215,0.830431,0.830647,0.831084,0.831304,0.831525,0.831747,
0.83197,0.832193,0.832418,0.832644,0.832871,0.833099,0.833328,0.833558,
0.833789,0.834021,0.834253,0.834487,0.834722,0.834958,0.835195,0.835433,
0.835672,0.835912,0.836153,0.836395,0.836638,0.836882,0.837127,0.837373,
0.83762,0.837868,0.838117,0.838367,0.838618,0.83887,0.839123,0.839377,
0.839632,0.839888,0.840145,0.840403,0.840662,0.840922,0.841183,0.841445,
0.841708,0.841972,0.842237,0.842503,0.842771,0.843039,0.843308,0.843578,
0.843849,0.844121,0.844394,0.844668,0.844943,0.84522,0.845497,0.845775,
0.846054,0.846334,0.846615,0.846898,0.847181,0.847465,0.84775,0.848036,
0.848323,0.848612,0.848901,0.849191,0.849482,0.849775,0.850068,0.850362,
0.850657,0.850953,0.851251,0.851549,0.851848,0.852148,0.852448,0.85275,
0.853053,0.853356,0.85366,0.853965,0.854271,0.854578,0.854885,0.855193,
0.855502,0.855812,0.856122,0.856433,0.856745,0.857058,0.857371,0.857684,
0.857999,0.858314,0.858629,0.858945,0.859262,0.859579,0.859897,0.860215,
0.860534,0.860853,0.861173,0.861493,0.861814,0.862135,0.862456,0.862778,
0.8631,0.863423,0.863746,0.864069,0.864393,0.864717,0.865041,0.865365,
0.86569,0.866015,0.86634,0.866665,0.866991,0.867317,0.867643,0.867969,
0.868295,0.868621,0.868948,0.869274,0.869601,0.869928,0.870254,0.870581,
0.870908,0.871235,0.871561,0.871888,0.872215,0.872541,0.872868,0.873194,
0.873521,0.873847,0.874173,0.874499,0.874825,0.87515,0.875476,0.875801,
0.876126,0.876451,0.876775,0.8771,0.877424,0.877748,0.878072,0.878395,
0.878719,0.879042,0.879365,0.879688,0.880011,0.880333,0.880655,0.880977,
0.881299,0.881621,0.881942,0.882263,0.882584,0.882905,0.883226,0.883546,
0.883866,0.884186,0.884506,0.884826,0.885145,0.885464,0.885783,0.886102,
0.88642,0.886738,0.887057,0.887374,0.887692,0.888009,0.888327,0.888644,
0.88896,0.889277,0.889593,0.889909,0.890225,0.890541,0.890856,0.891172,
0.891487,0.891801,0.892116,0.89243,0.892744,0.893058,0.893372,0.893685,
0.893999,0.894312,0.894624,0.894937,0.895249,0.895561,0.895873,0.896184,
0.896496,0.896807,0.897118,0.897428,0.897739,0.898049,0.898359,0.898669,
0.898978,0.899287,0.899596,0.899905,0.900214,0.900522,0.90083,0.901138,
0.901445,0.901753,0.90206,0.902368,0.902675,0.902982,0.903289,0.903596,
0.903903,0.90421,0.904517,0.904823,0.90513,0.905437,0.905745,0.906052,
0.906359,0.906666,0.906974,0.907282,0.90759,0.907898,0.908206,0.908515,
0.908823,0.909132,0.909442,0.909751,0.910061,0.910372,0.910682,0.910993,
0.911305,0.911617,0.911929,0.912242,0.912555,0.912868,0.913183,0.913497,
0.913812,0.914128,0.914444,0.914761,0.915079,0.915397,0.915716,0.916035,
0.916355,0.916676,0.916998,0.91732,0.917643,0.917967,0.918291,0.918617,
0.918943,0.91927,0.919598,0.919926,0.920256,0.920586,0.920918,0.92125,
0.921583,0.921918,0.922253,0.922589,0.922927,0.923265,0.923605,0.923945,
0.924287,0.92463,0.924973,0.925319,0.925665,0.926012,0.926361,0.92671,
0.927061,0.927413,0.927766,0.92812,0.928475,0.928831,0.929188,0.929546,
0.929905,0.930266,0.930627,0.930989,0.931353,0.931717,0.932082,0.932449,
0.932816,0.933184,0.933553,0.933924,0.934295,0.934667,0.93504,0.935413,
0.935788,0.936164,0.93654,0.936918,0.937296,0.937675,0.938055,0.938435,
0.938817,0.939199,0.939583,0.939967,0.940351,0.940737,0.941123,0.94151,
0.941898,0.942287,0.942676,0.943066,0.943457,0.943849,0.944241,0.944634,
0.945027,0.945422,0.945816,0.946212,0.946608,0.947005,0.947403,0.947801,
0.948199,0.948599,0.948999,0.949399,0.9498,0.950202,0.950604,0.951007,
0.95141,0.951814,0.952218,0.952623,0.953029,0.953435,0.953841,0.954248,
0.954655,0.955063,0.955471,0.95588,0.956289,0.956698,0.957107,0.957517,
0.957927,0.958337,0.958747,0.959158,0.959568,0.959978,0.960388,0.960798,
0.961208,0.961618,0.962027,0.962437,0.962845,0.963254,0.963662,0.964069,
0.964476,0.964883,0.965289,0.965694,0.966099,0.966502,0.966906,0.967308,
0.967709,0.96811,0.968509,0.968908,0.969305,0.969702,0.970097,0.970491,
0.970884,0.971276,0.971667,0.972056,0.972443,0.97283,0.973215,0.973598,
0.97398,0.97436,0.974738,0.975115,0.975491,0.975864,0.976235,0.976605,
0.976973,0.977339,0.977703,0.978065,0.978424,0.978782,0.979138,0.979491,
0.979842,0.980191,0.980537,0.980881,0.981223,0.981562,0.981899,0.982233,
0.982565,0.982894,0.98322,0.983543,0.983864,0.984182,0.984497,0.984809,
0.985119,0.985425,0.985728,0.986029,0.986326,0.98662,0.986912,0.9872,
0.987486,0.987768,0.988048,0.988324,0.988598,0.988868,0.989136,0.9894,
0.989662,0.989921,0.990176,0.990429,0.990678,0.990925,0.991169,0.991409,
0.991647,0.991881,0.992113,0.992342,0.992567,0.99279,0.993009,0.993226,
0.993439,0.99365,0.993857,0.994062,0.994263,0.994462,0.994657,0.994849,
0.995039,0.995225,0.995408,0.995588,0.995766,0.99594,0.996111,0.996279,
0.996444,0.996606,0.996765,0.996921,0.997074,0.997224,0.99737,0.997514,
0.997655,0.997792,0.997927,0.998058,0.998187,0.998312,0.998434,0.998553,
0.99867,0.998783,0.998893,0.999,0.999104,0.999204,0.999302,0.999397,
0.999488,0.999577,0.999662,0.999744,0.999824,0.9999,0.999973,1.00004,
1.00011,1.00017,1.00023,1.00029,1.00035,1.0004,1.00045,1.0005,
1.00054,1.00058,1.00062,1.00066,1.00069,1.00072,1.00075,1.00078,
1.0008,1.00083,1.00085,1.00087,1.00088,1.0009,1.00091,1.00092,
1.00093,1.00093,1.00094,1.00094,1.00094,1.00094,1.00094,1.00094,
1.00093,1.00093,1.00092,1.00091,1.0009,1.00089,1.00087,1.00086,
1.00085,1.00083,1.00081,1.0008,1.00078,1.00076,1.00074,1.00072,
1.0007,1.00067,1.00065,1.00063,1.0006,1.00058,1.00056,1.00053,
1.00051,1.00048,1.00045,1.00043,1.0004,1.00038,1.00035,1.00033,
1.0003,1.00028,1.00025,1.00023,1.0002,1.00018,1.00015,1.00013,
1.00011,1.00008,1.00006,1.00004,1.00002,1,0.999984,0.999967,
0.99995,0.999934,0.999918,0.999904,0.99989,0.999877,0.999864,0.999853,
0.999842,0.999831,0.999822,0.999813,0.999804,0.999797,0.99979,0.999783,
0.999777,0.999772,0.999767,0.999763,0.999759,0.999756,0.999754,0.999751,
0.99975,0.999749,0.999748,0.999748,0.999748,0.999748,0.999749,0.999751,
0.999753,0.999755,0.999757,0.99976,0.999763,0.999766,0.99977,0.999774,
0.999778,0.999783,0.999788,0.999793,0.999798,0.999804,0.999809,0.999815,
0.999821,0.999827,0.999833,0.99984,0.999846,0.999853,0.999859,0.999866,
0.999873,0.99988,0.999887,0.999894,0.9999,0.999907,0.999914,0.999921,
0.999928,0.999935,0.999941,0.999948,0.999954,0.99996,0.999967,0.999973,
0.999979,0.999984,0.99999,0.999995,1,1.00001,1.00001,1.00001,
1.00002,1.00002,1.00003,1.00003,1.00003,1.00004,1.00004,1.00004,
1.00005,1.00005,1.00005,1.00005,1.00005,1.00006,1.00006,1.00006,
1.00006,1.00006,1.00006,1.00006,1.00007,1.00007,1.00007,1.00007,
1.00007,1.00007,1.00007,1.00007,1.00007,1.00007,1.00007,1.00007,
1.00007,1.00006,1.00006,1.00006,1.00006,1.00006,1.00006,1.00006,
1.00006,1.00006,1.00006,1.00005,1.00005,1.00005,1.00005,1.00005,
1.00005,1.00004,1.00004,1.00004,1.00004,1.00004,1.00004,1.00003,
1.00003,1.00003,1.00003,1.00003,1.00002,1.00002,1.00002,1.00002,
1.00002,1.00002,1.00001,1.00001,1.00001,1.00001,1.00001,1.00001,
1,1,1,1,0.999998,0.999997,0.999996,0.999995,
0.999994,0.999993,0.999992,0.999991,0.99999,0.999989,0.999988,0.999988,
0.999987,0.999986,0.999986,0.999985,0.999985,0.999984,0.999984,0.999983,
0.999983,0.999983,0.999983,0.999982,0.999982,0.999982,0.999982,0.999982,
0.999982,0.999982,0.999982,0.999982,0.999982,0.999982,0.999982,0.999982,
0.999983,0.999983,0.999983,0.999983,0.999984,0.999984,0.999984,0.999985,
0.999985,0.999985,0.999986,0.999986,0.999987,0.999987,0.999987,0.999988,
0.999988,0.999989,0.999989,0.99999,0.99999,0.999991,0.999991,0.999992,
0.999992,0.999993,0.999993,0.999994,0.999994,0.999995,0.999995,0.999996,
0.999996,0.999996,0.999997,0.999997,0.999998,0.999998,0.999999,0.999999,
0.999999,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,0.999999,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,1,1,
1,1,1,1,1,1,0.999999,0.999999,
0.999999,0.999998,0.999998,0.999997,0.999997,0.999996,0.999996,0.999996,
0.999995,0.999995,0.999994,0.999994,0.999993,0.999993,0.999992,0.999992,
0.999991,0.999991,0.99999,0.99999,0.999989,0.999989,0.999988,0.999988,
0.999987,0.999987,0.999987,0.999986,0.999986,0.999985,0.999985,0.999985,
0.999984,0.999984,0.999984,0.999983,0.999983,0.999983,0.999983,0.999982,
0.999982,0.999982,0.999982,0.999982,0.999982,0.999982,0.999982,0.999982,
0.999982,0.999982,0.999982,0.999982,0.999983,0.999983,0.999983,0.999983,
0.999984,0.999984,0.999985,0.999985,0.999986,0.999986,0.999987,0.999988,
0.999988,0.999989,0.99999,0.999991,0.999992,0.999993,0.999994,0.999995,
0.999996,0.999997,0.999998,1,1,1,1,1.00001,
1.00001,1.00001,1.00001,1.00001,1.00001,1.00002,1.00002,1.00002,
1.00002,1.00002,1.00002,1.00003,1.00003,1.00003,1.00003,1.00003,
1.00004,1.00004,1.00004,1.00004,1.00004,1.00004,1.00005,1.00005,
1.00005,1.00005,1.00005,1.00005,1.00006,1.00006,1.00006,1.00006,
1.00006,1.00006,1.00006,1.00006,1.00006,1.00006,1.00007,1.00007,
1.00007,1.00007,1.00007,1.00007,1.00007,1.00007,1.00007,1.00007,
1.00007,1.00007,1.00007,1.00006,1.00006,1.00006,1.00006,1.00006,
1.00006,1.00006,1.00005,1.00005,1.00005,1.00005,1.00005,1.00004,
1.00004,1.00004,1.00003,1.00003,1.00003,1.00002,1.00002,1.00001,
1.00001,1.00001,1,0.999995,0.99999,0.999984,0.999979,0.999973,
0.999967,0.99996,0.999954,0.999948,0.999941,0.999935,0.999928,0.999921,
0.999914,0.999907,0.9999,0.999894,0.999887,0.99988,0.999873,0.999866,
0.999859,0.999853,0.999846,0.99984,0.999833,0.999827,0.999821,0.999815,
0.999809,0.999804,0.999798,0.999793,0.999788,0.999783,0.999778,0.999774,
0.99977,0.999766,0.999763,0.99976,0.999757,0.999755,0.999753,0.999751,
0.999749,0.999748,0.999748,0.999748,0.999748,0.999749,0.99975,0.999751,
0.999754,0.999756,0.999759,0.999763,0.999767,0.999772,0.999777,0.999783,
0.99979,0.999797,0.999804,0.999813,0.999822,0.999831,0.999842,0.999853,
0.999864,0.999877,0.99989,0.999904,0.999918,0.999934,0.99995,0.999967,
0.999984,1,1.00002,1.00004,1.00006,1.00008,1.00011,1.00013,
1.00015,1.00018,1.0002,1.00023,1.00025,1.00028,1.0003,1.00033,
1.00035,1.00038,1.0004,1.00043,1.00045,1.00048,1.00051,1.00053,
1.00056,1.00058,1.0006,1.00063,1.00065,1.00067,1.0007,1.00072,
1.00074,1.00076,1.00078,1.0008,1.00081,1.00083,1.00085,1.00086,
1.00087,1.00089,1.0009,1.00091,1.00092,1.00093,1.00093,1.00094,
1.00094,1.00094,1.00094,1.00094,1.00094,1.00093,1.00093,1.00092,
1.00091,1.0009,1.00088,1.00087,1.00085,1.00083,1.0008,1.00078,
1.00075,1.00072,1.00069,1.00066,1.00062,1.00058,1.00054,1.0005,
1.00045,1.0004,1.00035,1.00029,1.00023,1.00017,1.00011,1.00004,
0.999973,0.9999,0.999824,0.999744,0.999662,0.999577,0.999488,0.999397,
0.999302,0.999204,0.999104,0.999,0.998893,0.998783,0.99867,0.998553,
0.998434,0.998312,0.998187,0.998058,0.997927,0.997792,0.997655,0.997514,
0.99737,0.997224,0.997074,0.996921,0.996765,0.996606,0.996444,0.996279,
0.996111,0.99594,0.995766,0.995588,0.995408,0.995225,0.995039,0.994849,
0.994657,0.994462,0.994263,0.994062,0.993857,0.99365,0.993439,0.993226,
0.993009,0.99279,0.992567,0.992342,0.992113,0.991881,0.991647,0.991409,
0.991169,0.990925,0.990678,0.990429,0.990176,0.989921,0.989662,0.9894,
0.989136,0.988868,0.988598,0.988324,0.988048,0.987768,0.987486,0.9872,
0.986912,0.98662,0.986326,0.986029,0.985728,0.985425,0.985119,0.984809,
0.984497,0.984182,0.983864,0.983543,0.98322,0.982894,0.982565,0.982233,
0.981899,0.981562,0.981223,0.980881,0.980537,0.980191,0.979842,0.979491,
0.979138,0.978782,0.978424,0.978065,0.977703,0.977339,0.976973,0.976605,
0.976235,0.975864,0.975491,0.975115,0.974738,0.97436,0.97398,0.973598,
0.973215,0.97283,0.972443,0.972056,0.971667,0.971276,0.970884,0.970491,
0.970097,0.969702,0.969305,0.968908,0.968509,0.96811,0.967709,0.967308,
0.966906,0.966502,0.966099,0.965694,0.965289,0.964883,0.964476,0.964069,
0.963662,0.963254,0.962845,0.962437,0.962027,0.961618,0.961208,0.960798,
0.960388,0.959978,0.959568,0.959158,0.958747,0.958337,0.957927,0.957517,
0.957107,0.956698,0.956289,0.95588,0.955471,0.955063,0.954655,0.954248,
0.953841,0.953435,0.953029,0.952623,0.952218,0.951814,0.95141,0.951007,
0.950604,0.950202,0.9498,0.949399,0.948999,0.948599,0.948199,0.947801,
0.947403,0.947005,0.946608,0.946212,0.945816,0.945422,0.945027,0.944634,
0.944241,0.943849,0.943457,0.943066,0.942676,0.942287,0.941898,0.94151,
0.941123,0.940737,0.940351,0.939967,0.939583,0.939199,0.938817,0.938435,
0.938055,0.937675,0.937296,0.936918,0.93654,0.936164,0.935788,0.935413,
0.93504,0.934667,0.934295,0.933924,0.933553,0.933184,0.932816,0.932449,
0.932082,0.931717,0.931353,0.930989,0.930627,0.930266,0.929905,0.929546,
0.929188,0.928831,0.928475,0.92812,0.927766,0.927413,0.927061,0.92671,
0.926361,0.926012,0.925665,0.925319,0.924973,0.92463,0.924287,0.923945,
0.923605,0.923265,0.922927,0.922589,0.922253,0.921918,0.921583,0.92125,
0.920918,0.920586,0.920256,0.919926,0.919598,0.91927,0.918943,0.918617,
0.918291,0.917967,0.917643,0.91732,0.916998,0.916676,0.916355,0.916035,
0.915716,0.915397,0.915079,0.914761,0.914444,0.914128,0.913812,0.913497,
0.913183,0.912868,0.912555,0.912242,0.911929,0.911617,0.911305,0.910993,
0.910682,0.910372,0.910061,0.909751,0.909442,0.909132,0.908823,0.908515,
0.908206,0.907898,0.90759,0.907282,0.906974,0.906666,0.906359,0.906052,
0.905745,0.905437,0.90513,0.904823,0.904517,0.90421,0.903903,0.903596,
0.903289,0.902982,0.902675,0.902368,0.90206,0.901753,0.901445,0.901138,
0.90083,0.900522,0.900214,0.899905,0.899596,0.899287,0.898978,0.898669,
0.898359,0.898049,0.897739,0.897428,0.897118,0.896807,0.896496,0.896184,
0.895873,0.895561,0.895249,0.894937,0.894624,0.894312,0.893999,0.893685,
0.893372,0.893058,0.892744,0.89243,0.892116,0.891801,0.891487,0.891172,
0.890856,0.890541,0.890225,0.889909,0.889593,0.889277,0.88896,0.888644,
0.888327,0.888009,0.887692,0.887374,0.887057,0.886738,0.88642,0.886102,
0.885783,0.885464,0.885145,0.884826,0.884506,0.884186,0.883866,0.883546,
0.883226,0.882905,0.882584,0.882263,0.881942,0.881621,0.881299,0.880977,
0.880655,0.880333,0.880011,0.879688,0.879365,0.879042,0.878719,0.878395,
0.878072,0.877748,0.877424,0.8771,0.876775,0.876451,0.876126,0.875801,
0.875476,0.87515,0.874825,0.874499,0.874173,0.873847,0.873521,0.873194,
0.872868,0.872541,0.872215,0.871888,0.871561,0.871235,0.870908,0.870581,
0.870254,0.869928,0.869601,0.869274,0.868948,0.868621,0.868295,0.867969,
0.867643,0.867317,0.866991,0.866665,0.86634,0.866015,0.86569,0.865365,
0.865041,0.864717,0.864393,0.864069,0.863746,0.863423,0.8631,0.862778,
0.862456,0.862135,0.861814,0.861493,0.861173,0.860853,0.860534,0.860215,
0.859897,0.859579,0.859262,0.858945,0.858629,0.858314,0.857999,0.857684,
0.857371,0.857058,0.856745,0.856433,0.856122,0.855812,0.855502,0.855193,
0.854885,0.854578,0.854271,0.853965,0.85366,0.853356,0.853053,0.85275,
0.852448,0.852148,0.851848,0.851549,0.851251,0.850953,0.850657,0.850362,
0.850068,0.849775,0.849482,0.849191,0.848901,0.848612,0.848323,0.848036,
0.84775,0.847465,0.847181,0.846898,0.846615,0.846334,0.846054,0.845775,
0.845497,0.84522,0.844943,0.844668,0.844394,0.844121,0.843849,0.843578,
0.843308,0.843039,0.842771,0.842503,0.842237,0.841972,0.841708,0.841445,
0.841183,0.840922,0.840662,0.840403,0.840145,0.839888,0.839632,0.839377,
0.839123,0.83887,0.838618,0.838367,0.838117,0.837868,0.83762,0.837373,
0.837127,0.836882,0.836638,0.836395,0.836153,0.835912,0.835672,0.835433,
0.835195,0.834958,0.834722,0.834487,0.834253,0.834021,0.833789,0.833558,
0.833328,0.833099,0.832871,0.832644,0.832418,0.832193,0.83197,0.831747,
0.831525,0.831304,0.831084,0.830647,0.830431,0.830215,0.83]

notches1=[0]
notches2=[0]
notches3=[0]
convolved_notches=[complex(1.0,0.0)]
correction_estimate=[0]
num_estimates=0
fft_counter=5
correct_fn="??"
cur_tp_fn="none"
cur_sp_fn="none"
def writevars(varnames,vars,prefix):
    f=open(prefix+"/"+"variables.dump","w")
    for i in range(0,len(varnames)):
        f.write(varnames[i]+"="+str(float(vars[i]))+"\n")
    f.close()
    return 1
        

def sra_formatter(v):
    return "%12.1f" % float(v)
    

def bw_labels(clock,devid,devstr):
    labels = []
    if "rtl=" in devid or "rtl=" in devstr:
        return (["250k", "300k", "1M", "1.5M", "2M", "2.5M"])
    for i in range(1,11):
        mhz=i*1.0e6
        div=clock/mhz
        if div == int(div):
            label = str(i) + "M"
            labels.append(label)
    return (labels)

def bw_values(clock,devid,devstr):
    values = []
    if "rtl=" in devid or "rtl=" in devstr:
        return ([250e3, 300e3, 1.0e6, 1.5e6, 2.0e6, 2.5e6])
    for i in range(1,11):
        mhz=i*1.0e6
        div=clock/mhz
        if div == int(div):
            value = i*1.0e6
            values.append(value)
    return (values)
        
def cur_utc(val):
    ltp = time.gmtime()
    x = "%02d:%02d:%02d" % (ltp.tm_hour, ltp.tm_min, ltp.tm_sec)
    return (x)
    
def cur_sidereal(longitude,val):
    global doephem
    if doephem == False:
        return (("12:00:00","9999999999"))
    longstr = "%02d" % int(longitude)
    longstr = longstr + ":"
    longitude = abs(longitude)
    frac = longitude - int(longitude)
    frac *= 60
    mins = int(frac)
    longstr += "%02d" % mins
    longstr += ":00"
    x = ephem.Observer()
    x.date = ephem.now()
    x.long = longstr
    jdate = ephem.julian_date(x)
    tokens=str(x.sidereal_time()).split(":")
    hours=int(tokens[0])
    minutes=int(tokens[1])
    seconds=int(float(tokens[2]))
    sidt = "%02d:%02d:%02d" % (hours, minutes, seconds)
    return ((sidt,jdate))

def defnotch(notch,bw,cfreq):
    global convolved_notches
    foo = numpy.convolve(addnotch(notch,bw,cfreq,5.0e3,0),addnotch(notch,bw,cfreq,12.5e3,1))
    convolved_notches = (numpy.convolve(foo,
        addnotch(notch,bw,cfreq,10.0e3,2)))
    return 1
        
def getnotches(var):
    global convolved_notches
    
    return convolved_notches
        
def clear_notches(foo):
    global notches1
    global notches2
    global notches3
    global convolved_notches
    notches1 = [0]
    notches2 = [0]
    notches3 = [0]
    convolved_notches = [complex(1.0,0.0)]
    return 1

def addnotch(notch,bw,cfreq,raster,num):
    global notches1
    global notches2
    global notches3
    
    na = [notches1,notches2,notches3]
    
    lastnotch=notch
    filtsize=int(bw/raster)
    canonical_notch = int(notch/raster)*int(raster)
    
    i = 0
    
    removed = 0
    ns = na[num]
    for n in ns:
        if n == canonical_notch:
            ns.pop(i)
            removed = 1
        
        i = i + 1
    if removed == 0:
        ns.append(canonical_notch)
    na[num] = ns
    if num == 0:
        notches1 = ns
    elif num == 1:
        notches2 = ns
    elif num == 2:
        notches3 = ns
        
    l = compute_notches (na[num],filtsize,bw,cfreq)
    return (l)
    
    
def compute_notches(notchlist,flen,bw,freq):
    tmptaps=[complex(1.0,0.0)]*flen
    binwidth = bw / flen
    added=0
        
    #
    # Compute a multi-bin notch filter (a comb filter)
    #   based on the input notch list
    #
    for i in notchlist:
        diff = i - freq
        
        if ((i < (freq - bw/2)) or (i > (freq + bw/2))):
            continue
        
        idx = diff/binwidth
        idx = round(idx)
        
        if (idx < 0):
            #idx = -1 * idx
            idx = ((flen)-1) - idx
        
        #while (idx < 0):
            #idx = idx + 1
            
        tmptaps[int(idx)] = complex(0.0, 0.0)
        added = added + 1
        
    if (added <= 0):
        tmptaps = [complex(1.0,0.0)]
        
    return (numpy.fft.ifft(tmptaps))

def set_fftsize(fftsize):
    global correction_estimate
    global fft_counter
    global num_estimates
    
    correction_estimate = [0]*2048
    fft_counter = 5
    num_estimates = 0
    
    return True


def update_correction(fft):
    
    global correction_estimate
    global fft_counter
    global num_estimates
    
    smoothed_fft = [0.0]*len(fft)
    
    x = y = fft[0]
    
    for i in range(0,len(fft)):
        x = fft[i]
        y = (0.25*x) + (0.75)*y
        smoothed_fft[i] = y
    
    larray = [0.0]*len(fft)
    if fft_counter > 0:
        fft_counter -= 1
        return True

    minlvl = 999999.0;
    maxlvl = -0.99999999;
    
    if fft[0] < -90.0 and fft[len(fft)/2] < -90.0:
        return True

    
    for i in range(0,len(fft)):
        level = math.pow(10.0,smoothed_fft[i]/10.0)
        larray[i] = level
        if (level > maxlvl):
            maxlvl = level
        if (level < minlvl):
            minlvl = level
    
    halfway = (maxlvl - minlvl)/2
    halfway += minlvl
    
    for i in range(0,len(fft)):
        y = correction_estimate[i]
        x = larray[i]/halfway
        x = 1.0 / x
        y = (0.25 * x) + (0.75*y)
        correction_estimate[i] = y
    
    num_estimates = num_estimates + 1
    return True

#
# Log spectral data
#
# fft           - vector containing FFT magnitudes
# freq          - center frequency of observation
# decln         - declination of observation
# bw            - bandwidth of observation
# longitude     - geographic longitude at time of observation
# pref          - filename prefix for log files
# lrate         - logging rate
# ena           - enable logging
# ra            - RA of observation
#
def log_fft_data (fft, freq, decln, bw, longitude, pref, lrate, ena, ra, stype):
    if ena != True:
        return 0
    ltp = time.gmtime()
    if ((ltp.tm_sec % (lrate*6)) != 0):
        return False
    utc = cur_utc (1)
    sid,jdate = cur_sidereal (longitude, 1)
    fn = "%s/spec-%04d%02d%02d-%02d.dat" % (pref, ltp.tm_year, ltp.tm_mon, ltp.tm_mday, ltp.tm_hour)
    fp = open (fn, "a")
    paramstr = "PARAMS %12.5f %12.5f %12.5f %d %6.2f\n" % (freq, bw, decln, int(jdate), ra)
    fp.write (paramstr)
    headerstr = "%s.0 %s [\n" % (utc, sid)
    fp.write (headerstr)
    vstr = ""
    ctr = 0
    for i in range(len(fft)/2, len(fft)):
        dstr = "%5.2f " % (fft[i])
        vstr = vstr + dstr
        if ((ctr % 10) == 0):
            vstr = vstr + "\n"
            fp.write (vstr)
            vstr = ""
        ctr = ctr + 1
    for i in range(0, len(fft)/2):
        dstr = "%5.2f " % (fft[i])
        vstr = vstr + dstr
        if ((ctr % 10) == 0):
            vstr = vstr + "\n"
            fp.write (vstr)
            vstr = ""
        ctr = ctr + 1
    vstr = vstr + " ]\n"
    fp.write (vstr)
    fp.close ()
    return True

#
#
# Log pulsar profile
#
# profile          - a vector containing the profile
# freq             - center frequency of observation
# decln            - declination
# bw               - bandwidth of observation
# prate            - notional pulsar rate
# dm               - the DM used for dedispersion
# longitude        - our current geographic longitude
# pref             - filename prefix for log files
# lrate            - logging rate
# ena              - logging enabled
# ra               - RA of observation
#
def log_psr_data (profile, freq, decln, bw, prate, dm, longitude, pref, lrate, ena, ra):
    if ena != True:
        return 0
    ltp = time.gmtime()
    if ((ltp.tm_sec % (lrate*6)) != 0):
        return False
    utc = cur_utc (1)
    sid,jdate = cur_sidereal (longitude, 1)
    fn = "%s/psr-%04d%02d%02d-%02d.dat" % (pref, ltp.tm_year, ltp.tm_mon, ltp.tm_mday, ltp.tm_hour)
    fp = open (fn, "a")
    paramstr = "PARAMS %12.5f %12.5f %12.5f %d %7.3f %7.3f %6.2f\n" % (freq, bw, decln, int(jdate), prate, dm, ra)
    fp.write (paramstr)
    headerstr = "%s.0 %s [\n" % (utc, sid)
    fp.write (headerstr)
    vstr = ""
    ctr = 0
    for i in range(0,len(profile)):
        dstr = "%8.6f " % (profile[i])
        vstr = vstr + dstr
        if ((ctr % 10) == 0):
            vstr = vstr + "\n"
            fp.write (vstr)
            vstr = ""
        ctr = ctr + 1
    vstr = vstr + " ]\n"
    fp.write (vstr)
    fp.close ()
    return True

#
# Log total-power data
#
# tp          - total power value
# freq        - center frequency
# decln       - declination
# bw          - detector bandwidth
# longitude   - geographic longitude (for LMST calcs)
# pref        - filename prefix for log files
# lrate       - logging rate (logs every 'lrate' seconds)
# ra          - current RA
# ena         - logging enabled (True/False)
# expn        - experiment name
# cal_state   - current state of calibration source (if any):  1/0
#
gsecs = int(time.time())
def log_tp_data (tpr, tpi, freq, decln, bw, longitude, pref, lrate, ra, ena, expn, cal_state, stype,rda,rdb):
    global gsecs
    secs = int(time.time())
    if gsecs == secs:
        return False
    gsecs = secs
    ltp = time.gmtime()
    if ((ltp.tm_sec % lrate) != 0):
        return False
    if (ena != True):
        return False
    
    if (stype == "none"):
        return False
        
    if (stype == "both" or stype == "csv"):
        log_ref_tp_data (tpr, tpi,  longitude, pref, expn, cal_state, rda, rdb, freq)
    
    if (stype == "both" or stype == "traditional"):
        utc = cur_utc (tpr)
        sid,jdate = cur_sidereal (longitude, tpr)
        fn = "%s/tp-%04d%02d%02d-%02d.dat" % (pref, ltp.tm_year, ltp.tm_mon, ltp.tm_mday, ltp.tm_hour)
        logstr = "%s.0 %s %15.7f %15.7f %15.7f %15.7f\n" % (utc, sid, tpr, tpi, rda, rdb)
        fp = open (fn, "a")
        if ((ltp.tm_sec % 30) == 0):
            paramstr = "PARAMS %12.5f %12.5f %12.5f %d %6.2f %d\n" % (freq, bw, decln, int(jdate), ra, cal_state)
            fp.write (paramstr)
        fp.write (logstr)
     
        fp.close ()
    return True

#
# For CSV-file compatibility
#
def log_ref_tp_data (tpr, tpi, longitude, pref, expname, cal_state, rda, rdb, freq):
    ltp = time.gmtime()
    utc = cur_utc (tpr)
    sid,jdate = cur_sidereal (longitude, tpr)
    fn = "%s/CR%04d%02d%02d_%s.csv" % (pref, ltp.tm_year, ltp.tm_mon, ltp.tm_mday, expname)
    utc = utc.replace(":", ",")
    sid = sid.replace(":", ",")
    logstr = "%s,%s,%13.7f,%13.7f,%13.f,%13.7f,%d,%d\n" % (utc, sid, tpr, tpi, rda, rdb, cal_state, freq)
    fp = open (fn, "a")
    fp.write (logstr) 
    fp.close ()
    return True

cal_countdown = 3600
cal_ontime = 30
CAL_INIT_REQUIRED = 0
CAL_WAITING = 1
CAL_ON = 2
CAL_BADDEVICE = 3
CAL_MANUAL = 4
cal_state = CAL_INIT_REQUIRED

def calib_onoff_auto(depvar, devname, baudrate, initstring, onstring, offstring, lterm, every, seconds):
    global serh
    global cal_state
    global cal_countdown
    global cal_ontime
    global CAL_INIT_REQUIRED
    global CAL_WAITING
    global CAL_ON
    global CAL_BADDEVICE
    global CAL_MANUAL
    global doserial
    
    if (doserial == False):
        cal_state = CAL_BADDEVICE
    
    if (cal_state == CAL_BADDEVICE):
        return "BAD-DEVICE"
        
    if (len(devname) == 0 or devname == "none"):
        return "OFF"
    
    if (cal_state == CAL_MANUAL):
        return "MANUAL"

    if (cal_state == CAL_INIT_REQUIRED):
        # do pyserial stuff with devname
        cal_ontime = seconds
        cal_state = CAL_WAITING
        try:
            serh = serial.Serial (devname, baudrate, timeout=0)
        except:
            cal_state = CAL_BADDEVICE
            return "BAD-DEVICE"
            
        serh.write (initstring+lterm)
        serh.write (offstring+lterm)
        serh.read (100)
   
   
    # Drain input queue
    x = serh.read (100)
    
    if (cal_state == CAL_WAITING):
        t = int(time.time())
        if ((t % 3) == 0):
            # send offstring
            serh.write (offstring+lterm)
            x=serh.read(100)
        f = t % int(every)
        if f in [0,1,2,3,4]:
            cal_state = CAL_ON
            cal_ontime = seconds+1
            serh.write (onstring+lterm)
            x=serh.read (100)
    
    if (cal_state == CAL_ON):
        cal_ontime -= 1
        if ((cal_ontime % 5) == 0):
            # send onstring
            serh.write (onstring+lterm)
            x=serh.read(100)
        if (cal_ontime <= 0):
            # send offstring
            serh.write (offstring+lterm)
            x=serh.read(100)
            cal_state = CAL_WAITING
            
    if (cal_state == CAL_ON):   
        return "ON"
        
    return "OFF"

def calib_onoff_manual (control,devname,baudrate,onstring,offstring,lterm):
    global serh
    global cal_state
    global CAL_MANUAL
    global CAL_WAITING
    
    if (len(devname) == 0 or devname == "none"):
        return False

    if (cal_state == CAL_INIT_REQUIRED or cal_state == CAL_BADDEVICE):
        return False
    
    if (control == True):
        serh.write(onstring+lterm)
        x=serh.read (100)
        cal_state = CAL_MANUAL
        
    if (control == False):
        serh.write(offstring+lterm)
        x=serh.read(100)
        cal_state = CAL_WAITING
        
    return True

def get_num_estimates(probe):
    return num_estimates


def newfreq(freq):
    global num_estimates
    global correction_estimate
    global fft_counter
    
    num_estimates = 0
    fft_counter = 5
    l = len(correction_estimate)
    correction_estimate = [0]*l
    
    
def compute_correction(ena,filename):

    global correction_estimate
    global num_estimates
    global fft_counter
    global fixup_spline
    global correct_fn
    
    if ena != True:
        fft_counter = 5
        l = len(correction_estimate)
        correction_estimate = [0]*l
        num_estimates = 0
        return ([complex(1.0,0.0)])
    
    if correction_estimate[0] == 0 and correction_estimate[len(correction_estimate)/2] == 0:
        return ([complex(1.0,0.0)])
    
    try:
        t = numpy.fromfile(filename,dtype=float,count=-1,sep='\n')
        correction_estimate = t
        print "Correcting with pre-recorded correction data from", filename
        correct_fn = filename
    except:
        correct_fn = "??"
        pass

    numpy.savetxt ("sra_correction.dat",correction_estimate,fmt="%.9f")
    arry = correction_estimate
    if len(arry) < 256:
        return ([complex(1.0,0.0)])
    tmptaps = [complex(1.0,0.0)]*len(arry)
    ntaps = len(arry)

    tmp_spline = [0.0] * len(arry)
    if len(arry) == len(fixup_spline):
        tmp_spline = fixup_spline
    
    
    tndx = 0    
    #
    # Interpolate fixup spline if our FFT size is larger than the fixup spline size
    #
    if len(arry) > len(fixup_spline):
        d = int(len(arry)/len(fixup_spline))
        for i in range(0,len(arry)):
            tmp_spline[i] = fixup_spline[tndx]
            if i > 0 and (i % d == 0):
                tndx += 1
    
    #
    # Decimate the fixup spline if our FFT size is smaller than the fixup spline size
    #           
    if len(arry) < len(fixup_spline):
        d = int(len(fixup_spline)/len(arry))
        avg = 0.0
        tndx = 0
        for i in range(0,len(arry)):
            tmp_spline[i] = fixup_spline[tndx]
            tndx += d
        
    tndx = len(arry)/2
    for i in range(0,len(arry)):
        arry[i] *= tmp_spline[tndx]
        tndx += 1
        if (i == (len(arry)/2)-1):
            tndx = 0
    y = arry[0]     
    for i in range(0,len(arry)):
        y = (0.3 * arry[i]) + (0.7*y)
        tmptaps[i] = complex(y,0.0)
    
    tdtaps = numpy.fft.ifft(tmptaps)
    return (tdtaps)

def get_correct_fn (probe):
    global correct_fn
    return correct_fn
    
#
# For "real" FFT, so highest freq is srate/2
#
# Avoid the bottom 3%, which is where DC hangs out
#
# We return the frequency of the max bin
#
# Takes the FFT magnitude vector as input, the sample rate, and the highest frequency to search
#  (just set it to somehwere north of the sample rate to not limit the search)
#
def find_max_bin_freq (fft,srate,lim):
    start = int(len(fft)/30)
    maxbin = -200.0
    maxfreq = -1.0
    for i in range(start,len(fft)):
        freq = float(i)/float(len(fft))
        freq = freq * (srate/2.0)
        if (fft[i] > maxbin and freq < lim):
            maxbin = fft[i]
            maxfreq = freq
    
    return (maxfreq)

#
# Compute a de-dispersion filter
#  From Hankins, et al, 1975
#
# This code translated from dedisp_filter.c from Swinburne
#   pulsar software repository
#
def compute_dispfilter(dm,doppler,bw,centerfreq):
    npts = compute_disp_ntaps(dm,bw,centerfreq)
    tmp = numpy.zeros(npts, dtype=numpy.complex)
    M_PI = 3.14159265358
    DM = dm/2.41e-10
    #
    # Because astronomers are a crazy bunch, the "standard" calculation
    #   is in Mhz, rather than Hz
    #
    centerfreq = centerfreq / 1.0e6
    bw = bw / 1.0e6
    
    isign = int(bw / abs (bw))
    
    # Center frequency may be doppler shifted
    cfreq     = centerfreq / doppler

    # As well as the bandwidth..
    bandwidth = bw / doppler

    # Bandwidth divided among bins
    binwidth  = bandwidth / npts

    # Delay is an "extra" parameter, in usecs, and largely
    #  untested in the Swinburne code.
    delay = 0.0
    
    # This determines the coefficient of the frequency response curve
    # Linear in DM, but quadratic in center frequency
    coeff = -isign * 2.0*M_PI * DM / (cfreq*cfreq)
    
    # DC to nyquist/2
    n = 0
    for i in range(int(npts/2),npts):
        freq = (n + 0.5) * binwidth
        phi = coeff*freq*freq/(cfreq+freq) + (2.0*M_PI*freq*delay)
        tmp[i] = complex(math.cos(phi), math.sin(phi))
        n += 1

    # -nyquist/2 to DC
    n = int(npts/2)
    n *= -1
    for i in range(0,int(npts/2)):
        freq = (n + 0.5) * binwidth
        phi = coeff*freq*freq/(cfreq+freq) + (2.0*M_PI*freq*delay)
        tmp[i] = complex(math.cos(phi), math.sin(phi))
        n += 1
    
    
    return(numpy.fft.ifft(tmp))

#
# Compute minimum number of taps required in de-dispersion FFT filter
#
def compute_disp_ntaps(dm,bw,freq):
    NTLIMIT=65536*2
    #
    # Dt calculations are in Mhz, rather than Hz
    #    crazy astronomers....
    mbw = bw/1.0e6
    mfreq = freq/1.0e6

    f_lower = mfreq-(mbw/2)
    f_upper = mfreq+(mbw/2)

    # Compute smear time
    Dt = dm/2.41e-4 * (1.0/(f_lower*f_lower)-1.0/(f_upper*f_upper))

    # ntaps is now bandwidth*smeartime
    ntaps = bw*Dt
    if (ntaps < 32):
        ntaps = 32
    # special "flag" from command-line invoker to get around a bug
    #   in Gnu Radio involving the FFT filter implementation
    #   we can *never* increase the size of an FFT filter at runtime
    #   but can decrease it.  So there's a special "startup" flag (dm=1500.0)
    #   that causes us to return the NTLIMIT number of taps
    #
    if (dm >= 1500.0):
        ntaps = NTLIMIT
    if (ntaps > NTLIMIT):
        ntaps = NTLIMIT
    ntaps = int(math.log(ntaps) / math.log(2))
    ntaps = int(math.pow(2,ntaps+1))
    return(int(ntaps))

#
#
# Calculations for automated fringe-stopping
#
# We are called on a regular basis to produce a complex rotation value that is
#  applied to one leg of the interferometer, to reduce the fringe frequency to
#  close-to zero, thus allowing longer integration times.
#
def ha (ra,longit):
    #
    # First get current sidereal time as as HH:MM:SS string
    #
    lmst = cur_sidereal (longit, 0)
    lmst = lmst[0]
    parts = lmst.split(":")
    
    #
    # Re-express lmst (string) as a decimal hours
    #
    lmst = float(parts[0])
    lmst += float(parts[1]) / 60.0
    lmst += float(parts[2]) / 3600.0
    
    #
    # Now compute relative hour-angle between us, and the object in question (at some RA)
    #   When we're done, we have the relative hour-angle in radians
    #
    h = ra - lmst
    return (h)
#
# Phase accumulator
#
phase_accum = 0.0

#
# For time-delta calcs
#
last_time_phase = -99.0

#
# Earth rotation in radians/second
#
earth = math.radians(360.0 / 86400.0)

#
# Since part of the calculation only needs to be done when baseline or
#  frequency changes, we keep 'em global
gbaseline = 0.0
gfreq = 0.0
basefreqrot = 0.0

#
# Another part only changes when dec/latit changes
#
gdec = -99.0
glatit = -99.0
declatrot = 0.0

#
# The combination of the two
#
baserot = 0.0

#
# Speed of light, in case it wasn't obvious :)
#
C = 299792000.0

#
#
# Compute phase-rotation value based either on manual input, or automatic
#   fringe rotation
#
# pacer   - ignored, simply used as a "dummy" variable in the flow-graph to
#           make sure that we're called regularly.
# ra       - The RA in fractional hours
# dec      - The DEC in fractional degrees
# longit   - Our geographic longitude
# latit    - Our geographic latitude
# baseline - Baseline length, in meters
# ena      - Whether automagic or manual is in use
# manval   - The manual value
# freq     - The sky frequency
#
#
# These calculations assume a meridian-transit type setup, with a strictly east-west baseline
#
def fringe_stop (pacer, ra, dec, longit, latit, baseline, ena, manval, freq):
    global phase_accum
    global last_time_phase
    global earth
    global gbaseline
    global gfreq
    global basefreqrot
    global declatrot
    global gdec
    global glatit
    global baserot
 
    #
    # Just compute the fixed-value from the degrees input by the UI
    #
    if ena == False:
        radians = math.radians(manval)
        return (complex(math.cos(radians),math.sin(radians)),ha(ra,longit))

   
    #
    # Handle initialization of our time-delta calculator
    #
    if last_time_phase < 0:
        last_time_phase = time.time()

    #
    # Compute time delta compared to last-time
    #
    now = time.time()
    tdelt = now - last_time_phase
    
    #
    # Remember "now" for next time
    #
    last_time_phase = now
    
    changed = False
    
    #
    # If baseline or freq parameters have changed
    #
    if baseline != gbaseline or freq != gfreq:
        gbaseline = baseline
        gfreq = freq
        basefreqrot = (baseline * earth)/(C / freq)
        changed = True
    
    #
    # If dec or latit changes
    #
    if dec != gdec or latit != glatit:
        gdec = dec
        glatit = latit
        declatrot = math.cos(math.radians(dec))*math.cos(math.radians(latit))
        changed = True
    
    #
    # Update the combined "baserot"
    #
    if changed == True:
        baserot = basefreqrot * declatrot
        
    #
    # First get current sidereal time as as HH:MM:SS string
    #
    lmst = cur_sidereal (longit, 0)
    lmst = lmst[0]
    parts = lmst.split(":")
    
    #
    # Re-express lmst (string) as a decimal hours
    #
    lmst = float(parts[0])
    lmst += float(parts[1]) / 60.0
    lmst += float(parts[2]) / 3600.0
    
    #
    # Now compute relative hour-angle between us, and the object in question (at some RA)
    #   When we're done, we have the relative hour-angle in radians
    #
    h = ra - lmst
    h *= math.radians((360.0 / 24.0))
        
    #
    # Compute fringe rate in radians/hour
    #
    # h       - relative hour-angle, in radians between us and source
    #
    # Other parameters to the equation don't change with time, so they're
    #   efficiently pre-computed above, and re-computed when the input
    #   parameters change
    #
    F = baserot*math.sin(h)
    
    #
    # Because I get lost in the units, the above may be in radians/hour
    #   or radians/second so we can just adjust this scaling for the calculation below
    #
    scale = 1.0/3600.0
    
    #
    # Update the phase accumulator (stored in radians)
    # Handle phase-wrap gracefully
    # (although, the Python transcendentals handle this just fine themselves)
    #
    phase_accum += tdelt*(F * scale)
    if phase_accum > 2.0*math.pi:
        phase_accum -= (2.0*math.pi)
    
    #
    # We return a value that can be used by the phase rotator in the flow-graph
    #
    rval = complex(math.cos(phase_accum),math.sin(phase_accum))
    return (rval,math.degrees(h))
    
def beamwidth (aperture, freq):
    lamb = C /freq
    beam = 70 * lamb
    beam /= aperture
    return beam
    

def intuit_mode(d1,d2,dstr):
    if (dstr == "NONE" and "file=/dev/zero" in d2):
        return 0
    if (dstr == "NONE"):
        return 1
    if (dstr != "NONE"):
        if (" " in dstr and "rtl=" in dstr):
            return 1
        if ("nchan=2" in dstr):
            return 1
        if (" " in dstr and "uhd," in dstr):
            return 1
    return 0


def exit_cleanly(butval):
    p=os.getpid()
    if (butval == 1):
        x=os.kill(p,signal.SIGTERM)
