dtmc

module possession

    // state: i.e. area of the pitch where ball is in possession
    s : [0..8] init {possession begins}
        // 0 - 6: areas of the pitch
        // 7    : posession lost
        // 8    : goal scored

    [] s=0 -> {zero_to_zero}  : (s'=0) + {zero_to_one}  : (s'=1) + {zero_to_two}  : (s'=2) + {zero_to_three}  : (s'=3) + {zero_to_four}  : (s'=4) + {zero_to_five}  : (s'=5) + {zero_to_six}  : (s'=6) + {zero_to_PL}  : (s'=7) + {zero_to_G}  : (s'=8);
    [] s=1 -> {one_to_zero}   : (s'=0) + {one_to_one}   : (s'=1) + {one_to_two}   : (s'=2) + {one_to_three}   : (s'=3) + {one_to_four}   : (s'=4) + {one_to_five}   : (s'=5) + {one_to_six}   : (s'=6) + {one_to_PL}   : (s'=7) + {one_to_G}   : (s'=8);
    [] s=2 -> {two_to_zero}   : (s'=0) + {two_to_one}   : (s'=1) + {two_to_two}   : (s'=2) + {two_to_three}   : (s'=3) + {two_to_four}   : (s'=4) + {two_to_five}   : (s'=5) + {two_to_six}   : (s'=6) + {two_to_PL}   : (s'=7) + {two_to_G}   : (s'=8);
    [] s=3 -> {three_to_zero} : (s'=0) + {three_to_one} : (s'=1) + {three_to_two} : (s'=2) + {three_to_three} : (s'=3) + {three_to_four} : (s'=4) + {three_to_five} : (s'=5) + {three_to_six} : (s'=6) + {three_to_PL} : (s'=7) + {three_to_G} : (s'=8);
    [] s=4 -> {four_to_zero}  : (s'=0) + {four_to_one}  : (s'=1) + {four_to_two}  : (s'=2) + {four_to_three}  : (s'=3) + {four_to_four}  : (s'=4) + {four_to_five}  : (s'=5) + {four_to_six}  : (s'=6) + {four_to_PL}  : (s'=7) + {four_to_G}  : (s'=8);
    [] s=5 -> {five_to_zero}  : (s'=0) + {five_to_one}  : (s'=1) + {five_to_two}  : (s'=2) + {five_to_three}  : (s'=3) + {five_to_four}  : (s'=4) + {five_to_five}  : (s'=5) + {five_to_six}  : (s'=6) + {five_to_PL}  : (s'=7) + {five_to_G}  : (s'=8);
    [] s=6 -> {six_to_zero}   : (s'=0) + {six_to_one}   : (s'=1) + {six_to_two}   : (s'=2) + {six_to_three}   : (s'=3) + {six_to_four}   : (s'=4) + {six_to_five}   : (s'=5) + {six_to_six}   : (s'=6) + {six_to_PL}   : (s'=7) + {six_to_G}   : (s'=8);
    
    // absorbing states
    [] s=7 -> (s'=7);
    [] s=8 -> (s'=8);

endmodule

rewards 
    s = 7 : 1;
endrewards

