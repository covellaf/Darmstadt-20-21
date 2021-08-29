# =============================================================================
# Created By  : Francesca Covella
# Created Date: March - May 2021
# =============================================================================


"""
structure

every element of the dictonary is a parameter set which has as values a list of
dictionaries, each configuring a plot pertaining to that parameter set.


template

dictionary = { 
                'PARAMETER SET NAME #1': [ {
                                      'title': "  ",
                                      'style': 'seaborn-dark',
                                      'ys': [COLUMN 1, ...],
                                      'line_styles': ["-", ...],
                                      'line_widths': [1, ... ],
                                      'line_colors': [COLOR 1, ...],
                                      'markers': [".", ...],
                                      'v_label': " "       
                                    }, 
                                    {...}
                                    ],
                  ..., 
                  'PARAMETER SET NAME #n': [ {
                                      'title': "  ",
                                      'style': 'seaborn-dark',
                                      'ys': [COLUMN 1, ...],
                                      'line_styles': ["-", ...],
                                      'line_widths': [1, ... ],
                                      'line_colors': [COLOR 1, ...],
                                      'markers': [".", ...],
                                      'v_label': " "       
                                    }, 
                                    {...}
                                    ]                   
  }
"""


file_plots = {
    'HK_FSS': [
        {
            'title': "DCA RGA",
            'style': 'seaborn-darkgrid',
            'ys': [1, 2],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': " "
        }, 
        {
            'title': "FSS Alpha and Beta",
            'style': 'seaborn-darkgrid',
            'ys': [3, 4, 5, 6],
            'line_styles': ["-", "-", "--", "--"],
            'line_widths': [1, 1, 1.5, 1.5],
            'line_colors': ["red", "blue", "pink", "yellow"],
            'markers': [".", ".", "", ""],
            'v_label': "Alpha, Beta [rad]"
        }, 
        {
            'title': "FSS Alpha and Beta Error",
            'style': 'seaborn-darkgrid',
            'ys': [7, 8],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': "Error [rad]"
        } 
    ],
        
    'HK_IMUZ': [
        {
            'title': "IMU Accumulated Omega Z",
            'style': 'seaborn-darkgrid',
            'ys': [4, 6, 8],
            'line_styles': ["-", "-", "--"],
            'line_widths': [1, 1, 1],
            'line_colors': ["green", "orange", "orange"],
            'markers': [".", ".", ""],
            'v_label': "Angle [rad]"
            
        }, 
        {
            'title': "IMU Omega Z",
            'style': 'seaborn-dark',
            'ys': [3, 5, 7],
            'line_styles': ["-", "-", "--"],
            'line_widths': [1, 1, 1],
            'line_colors': ["green", "orange", "orange"],
            'markers': [".", ".", ""],
            'v_label': "Rate [rad/s]"
        } 
    ],

    'HK_CTRL': [
        {
            'title': "Control errors",
            'style': 'seaborn-darkgrid',
            'ys': [3, 4, 5],
            'line_styles': ["-", "-", "-"],
            'line_widths': [1, 1, 1],
            'line_colors': ["red", "blue", "orange"],
            'markers': [".", ".", "."],
            'v_label': "Error [rad]"
            
        }, 
        {
            'title': "DCA RGA",
            'style': 'seaborn-dark',
            'ys': [6, 7, 8],
            'line_styles': ["-", "-", "-"],
            'line_widths': [1, 1, 1],
            'line_colors': ["red", "blue", "orange"],
            'markers': [".", ".", "."],
            'v_label': "Momentum [Nms]"
        } 
    ],

    'HK_STR': [
        {
            'title': "STR Coordinates",
            'style': 'seaborn-darkgrid',
            'ys': [3, 4, 5, 6],
            'line_styles': ["-", "-", "-", "-"],
            'line_widths': [1, 1, 1.5, 1.5],
            'line_colors': ["blue", "green", "orange", "yellow"],
            'markers': [".", ".", "", ""],
            'v_label': "Coordinates [um/7]"
            
        }, 
        {
            'title': "STR errors",
            'style': 'seaborn-darkgrid',
            'ys': [7, 8],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["blue", "green"],
            'markers': [".", "."],
            'v_label': "Errors [um/7]"
        } 
    ],

    'ATT_IMU_RW': [
        {
            'title': "Wheel Speeds",
            'style': 'seaborn-darkgrid',
            'ys': [3, 4, 5, 6],
            'line_styles': ["-", "-", "-", "-"],
            'line_widths': [1, 1, 1, 1],
            'line_colors': ["blue", "red", "pink", "orange"],
            'markers': [".", ".", ".", "."],
            'v_label': "Speed [rpm]"
            
        }, 
        {
            'title': "IMU Angles",
            'style': 'seaborn-darkgrid',
            'ys': [1, 2],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "green"],
            'markers': [".", "."],
            'v_label': "Angle [arcsecs]"
        } 
    ],

    'ATT_TRQ_YPS': [
        {
            'title': "Wheel Torques",
            'style': 'seaborn-darkgrid',
            'ys': [1, 2, 3, 4],
            'line_styles': ["-", "-", "-", "-"],
            'line_widths': [1, 1, 1, 1],
            'line_colors': ["blue", "red", "purple", "orange"],
            'markers': [".", ".", ".", "."],
            'v_label': "Torques [Nm]"
            
        }

    ],

    'RTU2_IMU': [
        {
            'title': "TM Rates",
            'style': 'seaborn-dark',
            'ys': [1, 2, 3],
            'line_styles': ["-", "-", "-"],
            'line_widths': [1, 1, 1],
            'line_colors': ["red", "blue", "green"],
            'markers': [".", ".", "."],
            'v_label': "Rates [arcsecs/s]"
            
        }
    ], 
    
    'CTL_FSS': [
        {
            'title': "CTRL PKT DCA and RGA",
            'style': 'seaborn-darkgrid',
            'ys': [1, 2],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': " "
        }, 
        {
            'title': "CTRL PKT FSS Alpha and Beta Demand",
            'style': 'seaborn-dark',
            'ys': [3, 4],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': "Alpha, Beta [rad]"
        }, 
        {
            'title': "CTRL PKT FSS Alpha and Beta Error",
            'style': 'seaborn-darkgrid',
            'ys': [5, 6],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': "Error [rad] "
        } 
    ],

# CTL_IMUZ plot (to complete)
    'CTL_IMUZ': [
        {
            'title': "CTRL PKT IMU Acc. Omega Z",
            'style': 'seaborn-darkgrid',
            'ys': [1, 2],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': "[rad]"
            
        }, 
        {
            'title': "DCA RGA",
            'style': 'seaborn-darkgrid',
            'ys': [1, 2],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': " "
        } 
    ], 
    
    'CTL_CTRL': [
        {
            'title': "CTRL PKT Control Errors",
            'style': 'seaborn-darkgrid',
            'ys': [3, 4, 5],
            'line_styles': ["-", "-", "-"],
            'line_widths': [1, 1, 1],
            'line_colors': ["red", "blue", "orange"],
            'markers': [".", ".", "."],
            'v_label': "Error [rad]"
            
        }
    ],
    
    'CTL_STR': [
        {
            'title': "CTRL PKT STR Coordinates",
            'style': 'seaborn-darkgrid',
            'ys': [3, 4, 5, 6],
            'line_styles': ["--", "--", "-", "-"],
            'line_widths': [1.5, 1.5, 1, 1],
            'line_colors': ["orange", "orange", "blue", "green"],
            'markers': [None, None, ".", "."],
            'v_label': "Coordinates [um/7]"
            
        }
    ], 

    'CTL_DEBUG_FLOAT': [],

    'CTL_DEBUG_RAW': [],

    'CTL_ROLL_XY': [
        {
            'title': "Controller State: Roll Xn, Yn",
            'style': 'seaborn-darkgrid',
            'ys': [1, 3],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': "Roll Xn, Roll Yn"
            
        }, 
        {
            'title': "Controller State: Roll Xdot",
            'style': 'seaborn-darkgrid',
            'ys': [5],
            'line_styles': ["-"],
            'line_widths': [1],
            'line_colors': ["blue"],
            'markers': ["."],
            'v_label': " "
        } 
    ], 

    'CTL_ROLL_ITM': [
        {
            'title': "Controller State: Roll Y-integrator",
            'style': 'seaborn-darkgrid',
            'ys': [1],
            'line_styles': ["-"],
            'line_widths': [1],
            'line_colors': ["blue"],
            'markers': ["."],
            'v_label': " "
            
        }, 
        {
            'title': "Controller State: Roll Tn, Mn",
            'style': 'seaborn-darkgrid',
            'ys': [3, 5],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["blue", "orange"],
            'markers': [None, "."],
            'v_label': " "
        } 
    ], 

    'CTL_PITCH_XY': [
        {
            'title': "Controller State: Pitch Xn, Yn",
            'style': 'seaborn-dark',
            'ys': [1, 3],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': "Pitch Xn, Pitch Yn"
            
        }, 
        {
            'title': "Controller State: Pitch Xdot",
            'style': 'seaborn-darkgrid',
            'ys': [5],
            'line_styles': ["-"],
            'line_widths': [1],
            'line_colors': ["blue"],
            'markers': ["."],
            'v_label': " "
        } 
    ],

    'CTL_PITCH_ITM': [
        {
            'title': "Controller State: Pitch Y-integrator",
            'style': 'seaborn-darkgrid',
            'ys': [1],
            'line_styles': ["-"],
            'line_widths': [1],
            'line_colors': ["blue"],
            'markers': ["."],
            'v_label': " "
            
        }, 
        {
            'title': "Controller State: Pitch Tn, Mn",
            'style': 'seaborn-darkgrid',
            'ys': [3, 5],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["blue", "orange"],
            'markers': [None, "."],
            'v_label': " "
        } 
    ],

    'CTL_YAW_XY': [
        {
            'title': "Controller State: Yaw Xn, Yn",
            'style': 'seaborn-darkgrid',
            'ys': [1, 3],
            'line_styles': ["-", "-"],
            'line_widths': [1, 1],
            'line_colors': ["red", "blue"],
            'markers': [".", "."],
            'v_label': "Yaw Xn, Yaw Yn"
            
        }, 
        {
            'title': "Controller State: Yaw Xdot",
            'style': 'seaborn-darkgrid',
            'ys': [5],
            'line_styles': ["-"],
            'line_widths': [1],
            'line_colors': ["blue"],
            'markers': ["."],
            'v_label': " "
        } 
    ],

    'CTL_YAW_ITM': [
        {
            'title': "Controller State: Yaw Y-integrator",
            'style': 'seaborn-darkgrid',
            'ys': [1],
            'line_styles': ["-"],
            'line_widths': [1],
            'line_colors': ["blue"],
            'markers': ["."],
            'v_label': " "
            
        }, 
        {
            'title': "Controller State: Yaw Tn, Mn",
            'style': 'seaborn-darkgrid',
            'ys': [3, 4, 5, 6],
            'line_styles': ["-", "-", "-", "-"],
            'line_widths': [1, 1, 1, 1],
            'line_colors': ["blue", "orange", "black", "pink"],
            'markers': [".", ".", ".", "."],
            'v_label': " "
        } 
    ]


   
}

######################################################
# default colors
# red: roll
# blue: pitch
# green: yaw

# if you add a new set make sure to update the file id list on TMPrint_client
# file id
# HK_FSS     ---> 3 plots
# HK_IMUZ    ---> 2 plots
# HK_CTRL    ---> 2 plots
# HK_STR     ---> 2 plots
# ATT_IMU_RW ---> 2 plots
# ATT_TRQ_YPS ---> 1 plot
# RTU2_IMU   ---> 1 plot
# CTL_FSS  ---> 2 plots
# CTL_IMUZ ---> 2 plots
# CTL_CTRL ---> 1 plot
# CTL_STR ---> 1 plot
# CTL_DEBUG_FLOAT
# CTL_DEBUG_RAW
# CTL_ROLL_XY  ---> 2 plots
# CTL_ROLL_ITM ---> 2 plots
# CTL_PITCH_XY
# CTL_PITCH_ITM
# CTL_YAW_XY
# CTL_YAW_ITM
#######################################################
