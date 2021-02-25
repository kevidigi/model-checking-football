"dtmc\n\n
module possession\n\n
\t// state: i.e. area of the pitch where ball is in possession\n
\ts : [0..8] init {possession begins}\n
\t\t// 0 - 6: areas of the pitch\n
\t\t// 7    : posession lost\n
\t\t// 8    : goal scored\n\n
\t[] s=0 -> {" + str(trans_mat[0][0]) + "} : (s'=0) + {" + 
    str(trans_mat[0][1]) + "}  : (s'=1) + {" + 
    str(trans_mat[0][2]) + "}  : (s'=2) + {" + 
    str(trans_mat[0][3]) + "}  : (s'=3) + {" + 
    str(trans_mat[0][4]) + "}  : (s'=4) + {" + 
    str(trans_mat[0][5]) + "}  : (s'=5) + {" + 
    str(trans_mat[0][6]) + "}  : (s'=6) + {" + 
    str(trans_mat[0][7]) + "}  : (s'=7) + {" + 
    str(trans_mat[0][8]) + "}  : (s'=8);\n\t
    [] s=1 -> {" + str(trans_mat[1][0]) + "} : (s'=0) + {" + 
    str(trans_mat[1][1]) + "}  : (s'=1) + {" + 
    str(trans_mat[1][2]) + "}  : (s'=2) + {" + 
    str(trans_mat[1][3]) + "}  : (s'=3) + {" + 
    str(trans_mat[1][4]) + "}  : (s'=4) + {" + 
    str(trans_mat[1][5]) + "}  : (s'=5) + {" + 
    str(trans_mat[1][6]) + "}  : (s'=6) + {" + 
    str(trans_mat[1][7]) + "}  : (s'=7) + {" + 
    str(trans_mat[1][8]) + "}  : (s'=8);\n\t
    [] s=2 -> {" + str(trans_mat[2][0]) + "} : (s'=0) + {" + 
    str(trans_mat[2][1]) + "}  : (s'=1) + {" + 
    str(trans_mat[2][2]) + "}  : (s'=2) + {" + 
    str(trans_mat[2][3]) + "}  : (s'=3) + {" + 
    str(trans_mat[2][4]) + "}  : (s'=4) + {" + 
    str(trans_mat[2][5]) + "}  : (s'=5) + {" + 
    str(trans_mat[2][6]) + "}  : (s'=6) + {" + 
    str(trans_mat[2][7]) + "}  : (s'=7) + {" + 
    str(trans_mat[2][8]) + "}  : (s'=8);\n\t
    [] s=3 -> {" + str(trans_mat[3][0]) + "} : (s'=0) + {" + 
    str(trans_mat[3][1]) + "}  : (s'=1) + {" + 
    str(trans_mat[3][2]) + "}  : (s'=2) + {" + 
    str(trans_mat[3][3]) + "}  : (s'=3) + {" + 
    str(trans_mat[3][4]) + "}  : (s'=4) + {" + 
    str(trans_mat[3][5]) + "}  : (s'=5) + {" + 
    str(trans_mat[3][6]) + "}  : (s'=6) + {" + 
    str(trans_mat[3][7]) + "}  : (s'=7) + {" + 
    str(trans_mat[3][8]) + "}  : (s'=8);\n\t
    [] s=4 -> {" + str(trans_mat[4][0]) + "} : (s'=0) + {" + 
    str(trans_mat[4][1]) + "}  : (s'=1) + {" + 
    str(trans_mat[4][2]) + "}  : (s'=2) + {" + 
    str(trans_mat[4][3]) + "}  : (s'=3) + {" + 
    str(trans_mat[4][4]) + "}  : (s'=4) + {" + 
    str(trans_mat[4][5]) + "}  : (s'=5) + {" + 
    str(trans_mat[4][6]) + "}  : (s'=6) + {" + 
    str(trans_mat[4][7]) + "}  : (s'=7) + {" + 
    str(trans_mat[4][8]) + "}  : (s'=8);\n\t
    [] s=5 -> {" + str(trans_mat[5][0]) + "}  : (s'=0) + {" + 
    str(trans_mat[5][1]) + "}  : (s'=1) + {" + 
    str(trans_mat[5][2]) + "}  : (s'=2) + {" + 
    str(trans_mat[5][3]) + "}  : (s'=3) + {" + 
    str(trans_mat[5][4]) + "}  : (s'=4) + {" + 
    str(trans_mat[5][5]) + "}  : (s'=5) + {" + 
    str(trans_mat[5][6]) + "}  : (s'=6) + {" + 
    str(trans_mat[5][7]) + "}  : (s'=7) + {" + 
    str(trans_mat[5][8]) + "}  : (s'=8);\n\t
    [] s=6 -> {" + str(trans_mat[6][0]) + "} : (s'=0) + {" + 
    str(trans_mat[6][1]) + "}  : (s'=1) + {" + 
    str(trans_mat[6][2]) + "}  : (s'=2) + {" + 
    str(trans_mat[6][3]) + "}  : (s'=3) + {" + 
    str(trans_mat[6][4]) + "}  : (s'=4) + {" + 
    str(trans_mat[6][5]) + "}  : (s'=5) + {" + 
    str(trans_mat[6][6]) + "}  : (s'=6) + {" + 
    str(trans_mat[6][7]) + "}  : (s'=7) + {" + 
    str(trans_mat[6][8]) + "}  : (s'=8);\n
\n
\t// absorbing states\n
\t[] s=7 -> (s'=7);\n
\t[] s=8 -> (s'=8);\n
\n
endmodule"

