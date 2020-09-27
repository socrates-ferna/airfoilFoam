import pandas as pd
import numpy as np
import sympy as sy
import numpy.polynomial.polynomial as poly
import os
# Read txt file and drop first line
# Propongo el siguiente cambio para la lectura del perfil
airfoil_file = 'E423.txt'
airfoilpath = os.path.abspath(os.getcwd() + "/" + airfoil_file)
df = pd.read_csv(airfoilpath, sep=' ', header=None)
df = df.drop(df.index[[0]])
df = df.astype(float)
df.columns = ['x', 'y']
df = df.sort_values('x', ascending=True)
Prog = 1  # If 0 SU2 if 1 OpenFoam
O_F_Name = 'Airfoil'
#-----------------------------Rotation----------------------------------------#
deg = 0
X_Rt = 0.90
theta = deg*(np.pi/180)
for i in range(df.shape[0]):
    if df.iloc[i, 0] > X_Rt:
        origin = np.array([X_Rt, 0])
        Points = np.array([df.iloc[i, 0], df.iloc[i, 1]])
        Point_to_Rot = Points-origin
        Rotation_Matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta), np.cos(theta)]])
        Rotated = Rotation_Matrix.dot(Point_to_Rot)
        Rotated = Rotated+origin
        df.iloc[i, 0] = Rotated[0]
        df.iloc[i, 1] = Rotated[1]
#-----------------------------------------------------------------------------#

chord = 1
front = df[df['x'] < (0.2025*chord)]
backm = df[(df['x'] > (0.2025*chord)) & (df['x'] < (0.90*chord))]
backe = df[df['x'] > (0.90*chord)]

#####################################################################


def Avg_Cord():
    global a, i, avgxcord, avgycord
    x = (xcord[0+a] + xcord[1+a])/2
    y = (ycord[0+a] + ycord[1+a])/2
    a = a + 1
    i = i + 1
    avgxcord = np.append(avgxcord, x)
    avgycord = np.append(avgycord, y)


def Cont_Cord():
    global a, i
    a = a + 1
    i = i + 1


def Find_MCL_for_SEG(avgcordx, avgcordy, nofcoef):
    mcamberlcoeff = poly.polyfit(avgcordx, avgcordy, nofcoef)
    x = sy.Symbol('x')
    if nofcoef == 2:
        meancline = mcamberlcoeff[0]+mcamberlcoeff[1]*x+mcamberlcoeff[2]*x**2
    elif nofcoef == 3:
        meancline = mcamberlcoeff[0]+mcamberlcoeff[1]*x+mcamberlcoeff[2]*x**2+mcamberlcoeff[3]*x**3
    return meancline


######################################################################
xcord = front.iloc[:, 0].values
ycord = front.iloc[:, 1].values

elemxf = np.count_nonzero(xcord) - 1
i = 0
a = 0
avgxcord = np.array([])
avgycord = np.array([])

for i in range(elemxf):
    if (abs(ycord[0+a]))-(abs(ycord[1+a])) > 0.00001:
        Avg_Cord()
    else:
        Cont_Cord()

le_mcl = Find_MCL_for_SEG(avgxcord, avgycord, 3)
######################################################################
xcord = backm.iloc[:, 0].values
ycord = backm.iloc[:, 1].values

elemxf = np.count_nonzero(xcord) - 1
i = 0
a = 0
avgxcord = np.array([])
avgycord = np.array([])

for i in range(elemxf):
    if abs(((abs(ycord[0+a]))-(abs(ycord[1+a]))) > 0.03) and (((xcord[0+a] + xcord[1+a])/2) < 0.80):
        Avg_Cord()
    elif abs(((abs(ycord[0+a]))-(abs(ycord[1+a]))) > 0.02) and (((xcord[0+a] + xcord[1+a])/2) > 0.80) and (((xcord[0+a] + xcord[1+a])/2) < 0.90):
        Avg_Cord()
    else:
        Cont_Cord()

backm_mcl = Find_MCL_for_SEG(avgxcord, avgycord, 2)
######################################################################
xcord = backe.iloc[:, 0].values
ycord = backe.iloc[:, 1].values

elemxf = np.count_nonzero(xcord) - 1
i = 0
a = 0
avgxcord = np.array([])
avgycord = np.array([])

for i in range(elemxf):
    if (((xcord[0+a] + xcord[1+a])/2) < 0.994 and ((xcord[0+a] + xcord[1+a])/2) > 0.90 and abs((abs(ycord[0+a]))-(abs(ycord[1+a]))) > 0.00):
        Avg_Cord()
    elif (((xcord[0+a] + xcord[1+a])/2) > 0.994 and abs((abs(ycord[0+a]))-(abs(ycord[1+a]))) > 0.00):
        Avg_Cord()
    else:
        Cont_Cord()

backe_mcl = Find_MCL_for_SEG(avgxcord, avgycord, 2)
#####################################################################


def Divide_Seg_Top_Bot(Segment, Segment_MCL_fx):
    x = sy.Symbol('x')
    mcly_seg_mid = np.array([])
    for i in range(Segment.shape[0]):
        mcly_point = Segment_MCL_fx.subs(x, Segment.iloc[i, 0])
        mcly_point = float(mcly_point)
        mcly_seg_mid = np.append(mcly_seg_mid, mcly_point)
    df_mcly_seg_mid = pd.DataFrame(mcly_seg_mid)
    df_mcly_seg_mid.columns = ['mcly_seg']
    Segment.reset_index(drop=True, inplace=True)
    Segment = pd.concat([Segment, df_mcly_seg_mid], axis=1)
    top_f_seg = Segment[(Segment['y'] > Segment['mcly_seg'])]
    bot_f_seg = Segment[(Segment['y'] < Segment['mcly_seg'])]
    top_f_seg = top_f_seg.sort_values(by=['x'], ascending=False)
    bot_f_seg = bot_f_seg.sort_values(by=['x'], inplace=False)
    return(top_f_seg, bot_f_seg)


le_top_bot = Divide_Seg_Top_Bot(front, le_mcl)
backm_top_bot = Divide_Seg_Top_Bot(backm, backm_mcl)
backe_top_bot = Divide_Seg_Top_Bot(backe, backe_mcl)

le = pd.concat([le_top_bot[0], le_top_bot[1]])
top = pd.concat([backe_top_bot[0], backm_top_bot[0]])
bottom = pd.concat([backm_top_bot[1], backe_top_bot[1]])
##############################################################################
f = open("Testing.geo", "w+")
ec = 1
curve_count = 1


def Point_Create(Segment):
    global ec, f
    i = 0
    while i < Segment.shape[0]:
        f.write("Point(%s)={%s,%s,0,1};\n" % (ec, Segment.iloc[i, 0], Segment.iloc[i, 1]))
        i = i + 1
        ec = ec + 1


def BSpline_Create(start, end, number_of_elements, progresion, bump):
    global f, curve_count
    f.write("BSpline(%s)={%s:%s};\n" % (curve_count, start, end))
    if bump == 0:
        f.write("Transfinite Curve {%s}=%s Using Progression %s;\n" %
                (curve_count, number_of_elements, progresion))
    elif bump == 1:
        f.write("Transfinite Curve {%s}=%s Using  Bump 0.02\n" %
                (curve_count, number_of_elements))
    curve_count = curve_count+1


CFLE = 200  # Curved Front Leading Edge
RRH = 200  # Rear Rectangle Horizontal
RVM = 9  # Rear Vertical Middle
OEV = 400  # Outer Enclosure Vertical
IEV = 50  # Inner Enclosure Vertical
AEH = 200  # Airfoil Enclosure Horizontal

Point_Create(top)
Point_Create(le)
Point_Create(bottom)
BSpline_Create(1, top.shape[0], AEH, 1, 0)
BSpline_Create(top.shape[0], top.shape[0]+le.shape[0]+1, CFLE, 1, 0)
BSpline_Create(top.shape[0]+le.shape[0]+1, top.shape[0]+le.shape[0]+bottom.shape[0], AEH, 1, 0)
#############################################################################


def Point_From_Cords(array_x, array_y):
    global f, ec
    i = 0
    for i in range(len(array_x)):
        x = array_x[i]
        y = array_y[i]
        f.write("Point(%s)={%s,%s,0,1};\n" % (ec, x, y))
        i = i + 1
        ec = ec + 1


tophalf = int(top.shape[0]/2)
top_l = top.shape[0]-1
bottomhalf = int(bottom.shape[0]/2)
bot_l = bottom.shape[0]-1
d_rear_rect = 20
d_in = 0.25  # Distance from airfoil to inner mesh
d_in_out = 10  # Distance from airfoil to outer mesh
array_x_in = [top.iloc[0, 0], top.iloc[tophalf, 0], top.iloc[top_l, 0], 0-d_in*3,
              bottom.iloc[0, 0], bottom.iloc[bottomhalf, 0], bottom.iloc[bot_l, 0], d_rear_rect, d_rear_rect, d_rear_rect, d_rear_rect]
array_y_in = [top.iloc[0, 1]+d_in, top.iloc[tophalf, 1]+d_in, top.iloc[top_l, 1] + d_in, 0, bottom.iloc[0, 1] -
              d_in, bottom.iloc[bottomhalf, 1]-d_in, bottom.iloc[bot_l, 1]-d_in, bottom.iloc[bot_l, 1], top.iloc[0, 1], bottom.iloc[bot_l, 1] - d_in, top.iloc[0, 1] + d_in]
Point_From_Cords(array_x_in, array_y_in)
array_x_out = [d_rear_rect, top.iloc[0, 0], top.iloc[top_l, 0], -
               d_in_out*3, bottom.iloc[0, 0], bottom.iloc[bot_l, 0], d_rear_rect]
array_y_out = [d_in_out, d_in_out, d_in_out, 0, -d_in_out, -d_in_out, -d_in_out]
Point_From_Cords(array_x_out, array_y_out)
##############################################################################
in_amount_points = (top.shape[0])+(le.shape[0])+(bottom.shape[0])
BSpline_Create(in_amount_points+1, in_amount_points+3, AEH, 1, 0)
BSpline_Create(in_amount_points+3, in_amount_points+5, CFLE, 1, 0)
BSpline_Create(in_amount_points+5, in_amount_points+7, AEH, 1, 0)
BSpline_Create(in_amount_points+14, in_amount_points+16, CFLE, 1, 1)
##############################################################################


def Line(start, end, number_of_elements, progression):
    global f, curve_count
    for i in range(len(start)):
        f.write("Line(%s)={%s,%s};\n" % (curve_count, start[i], end[i]))
        f.write("Transfinite Curve {%s}=%s Using Progression %s ;\n" %
                (curve_count, number_of_elements[i], progression[i]))
        curve_count = curve_count+1


#-------------------------Outer Enclosure Lines-------------------------------#
array_start = [in_amount_points+14, in_amount_points+13,
               in_amount_points+11, in_amount_points+9, in_amount_points+9, in_amount_points+8, in_amount_points+10, in_amount_points+16, in_amount_points+17]
array_end = [in_amount_points+13, in_amount_points+12,
             in_amount_points+12, in_amount_points + 11, in_amount_points+8, in_amount_points+10, in_amount_points+18, in_amount_points+17, in_amount_points+18]
progression = [1, 1.07, 1, 1.1, 1, 1.1, 1, 1, 1.07]
number_of_elements = [AEH, RRH, OEV, IEV, RVM, IEV, OEV, AEH, RRH]
# Line[8,9,10,11,12,13,14,15,16]
Line(array_start, array_end, number_of_elements, progression)
#----------------------Airfoil & Inner Enclosure Lines------------------------#
array_start = [1, top.shape[0], top.shape[0]+le.shape[0] +
               1, top.shape[0]+le.shape[0]+bottom.shape[0]]
array_end = [in_amount_points+1, in_amount_points+3, in_amount_points+5, in_amount_points+7]
progression = [1.1, 1.1, 1.1, 1.1]
number_of_elements = [IEV, IEV, IEV, IEV]
# Line=[17,18,19,20]
Line(array_start, array_end, number_of_elements, progression)
#----------------From Inner Enclosure to Outer Enclosure Lines ---------------#
array_start = [in_amount_points+3, in_amount_points+1,
               in_amount_points+5, in_amount_points+7, in_amount_points+1, in_amount_points+7, 1, top.shape[0]+le.shape[0]+bottom.shape[0], 1]
array_end = [in_amount_points+14, in_amount_points+13,
             in_amount_points+16, in_amount_points + 17, in_amount_points+11, in_amount_points+10, in_amount_points+9, in_amount_points+8, in_amount_points]
progression = [1, 1, 1, 1, 1.07, 1.07, 1.07, 1.07, 1]
number_of_elements = [OEV, OEV, OEV, OEV, RRH, RRH, RRH, RRH, RVM]
# Line[21,22,23,24,25,26,27,28,29]
Line(array_start, array_end, number_of_elements, progression)
#------------------------------Create Surfaces--------------------------------#
Surface_Counter = 1
Surface_Loop_Array = [[7, -23, -5, 21], [18, 5, -19, -2],
                      [6, -20, -3, 19], [1, 18, -4, -17], [4, 21, 8, -22], [6, 24, -15, -23], [9, -10, -25, 22], [26, 14, -16, -24], [25, -11, -27, 17], [28, 13, -26, -20], [27, 12, -28, -29]]


def Surface_Create(line1, line2, line3, line4):
    global Surface_Counter, f
    f.write("Curve Loop(%s) = {%s, %s, %s, %s};\n" % (Surface_Counter, line1, line2, line3, line4))
    f.write("Plane Surface(%s) = {%s};\n " % (Surface_Counter, Surface_Counter))
    f.write("Transfinite Surface {%s};\n " % (Surface_Counter))
    f.write("Recombine Surface {%s};\n " % (Surface_Counter))
    Surface_Counter = Surface_Counter+1


for i in range(len(Surface_Loop_Array)):
    C = Surface_Loop_Array[i]
    l1 = C[0]
    l2 = C[1]
    l3 = C[2]
    l4 = C[3]
    Surface_Create(l1, l2, l3, l4)
#-------------------------Create Physical Groups------------------------------#
if Prog == 0:
    f.write("Physical Curve(%s) = {7, 15, 16, 14, 13, 12, 11, 10, 9, 8};\n" % ("\"FARFIELD\""))
    f.write("Physical Curve(%s) = {1, 2, 3, 29};\n" % ("\"AIRFOIL\""))
    f.write("Physical Surface(%s) = {7, 5, 1, 6, 8, 3, 2, 4, 9, 10, 11};\n" % ("\"DOMAIN\""))
    f.write("Mesh 3;\n")
    f.write("Save '%s.su2';\n" % (O_F_Name))

if Prog == 1:
    f.write("Extrude {0, 0, 1} {\nSurface{1}; Surface{6}; Surface{5}; Surface{2}; Surface{4}; Surface{3}; Surface{10}; Surface{8}; Surface{7}; Surface{9};Surface{11};Recombine;Layers{1};\n}\n")
    f.write("Physical Surface(%s) = {38};\n" % ("\"inlet\""))
    f.write("Physical Surface(%s) = {196, 174, 240, 218, 262};\n" % ("\"outlet\""))
    f.write("Physical Surface(%s) = {200, 68, 214, 90, 126, 116, 156, 270};\n" % ("\"walls\""))
    f.write("Physical Surface(%s) = {51, 1, 205, 8, 227, 7, 95, 5, 6, 73, 10, 9, 183, 249, 271, 11, 161, 139, 117, 3, 4, 2};\n" % (
        "\"frontAndBack\""))
    f.write("Physical Volume(%s) = {1, 2, 3, 9, 8, 7, 10, 6, 4, 5, 11};\n" % ("\"Vol\""))
    f.write("Mesh 3;\n")
    f.write("Save '%s.msh';\n" % (O_F_Name))
