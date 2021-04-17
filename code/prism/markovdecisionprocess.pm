mdp

module passes_and_shots

	// states: 0-6 = zones on the pitch; 7 = possession lost; 8 = goal scored
	s : [0..8];
	// player actions from zone 0 (s=0)
	[pass_0_0]	      s=0 ->
	0.9055121113866107 : (s'=0) + (1 - 0.9055121113866107) : (s'=7);
	[pass_0_1]	      s=0 ->
	0.8096805630752572 : (s'=1) + (1 - 0.8096805630752572) : (s'=7);
	[pass_0_2]	      s=0 ->
	0.7466875935321385 : (s'=2) + (1 - 0.7466875935321385) : (s'=7);
	[pass_0_3]	      s=0 ->
	0.8102130818269146 : (s'=3) + (1 - 0.8102130818269146) : (s'=7);
	[pass_0_4]	      s=0 ->
	0.6955666045162627 : (s'=4) + (1 - 0.6955666045162627) : (s'=7);
	[pass_0_5]	      s=0 ->
	0.3562488663159804 : (s'=5) + (1 - 0.3562488663159804) : (s'=7);
	[pass_0_6]	      s=0 ->
	0.6746698679471789 : (s'=6) + (1 - 0.6746698679471789) : (s'=7);
	[shoot_0]	       s=0 ->
	0.007867820613690008 : (s'=8) + (1 - 0.007867820613690008) : (s'=7);

	// player actions from zone 1 (s=1)
	[pass_1_0]	      s=1 ->
	0.9377396472392638 : (s'=0) + (1 - 0.9377396472392638) : (s'=7);
	[pass_1_1]	      s=1 ->
	0.8372992953679104 : (s'=1) + (1 - 0.8372992953679104) : (s'=7);
	[pass_1_2]	      s=1 ->
	0.8151378446115288 : (s'=2) + (1 - 0.8151378446115288) : (s'=7);
	[pass_1_3]	      s=1 ->
	0.7984104046242775 : (s'=3) + (1 - 0.7984104046242775) : (s'=7);
	[pass_1_4]	      s=1 ->
	0.7862407862407862 : (s'=4) + (1 - 0.7862407862407862) : (s'=7);
	[pass_1_5]	      s=1 ->
	0.43760340345072085 : (s'=5) + (1 - 0.43760340345072085) : (s'=7);
	[pass_1_6]	      s=1 ->
	0.40876732858748593 : (s'=6) + (1 - 0.40876732858748593) : (s'=7);
	[shoot_1]	       s=1 ->
	0.005434225366553881 : (s'=8) + (1 - 0.005434225366553881) : (s'=7);

	// player actions from zone 2 (s=2)
	[pass_2_0]	      s=2 ->
	0.9249657498155759 : (s'=0) + (1 - 0.9249657498155759) : (s'=7);
	[pass_2_1]	      s=2 ->
	0.8348262757871878 : (s'=1) + (1 - 0.8348262757871878) : (s'=7);
	[pass_2_2]	      s=2 ->
	0.7675201346315663 : (s'=2) + (1 - 0.7675201346315663) : (s'=7);
	[pass_2_3]	      s=2 ->
	0.8424684804246848 : (s'=3) + (1 - 0.8424684804246848) : (s'=7);
	[pass_2_4]	      s=2 ->
	0.7921987462270722 : (s'=4) + (1 - 0.7921987462270722) : (s'=7);
	[pass_2_5]	      s=2 ->
	0.522697795071336 : (s'=5) + (1 - 0.522697795071336) : (s'=7);
	[pass_2_6]	      s=2 ->
	0.8040243135610983 : (s'=6) + (1 - 0.8040243135610983) : (s'=7);
	[shoot_2]	       s=2 ->
	0.010622477161674103 : (s'=8) + (1 - 0.010622477161674103) : (s'=7);

	// player actions from zone 3 (s=3)
	[pass_3_0]	      s=3 ->
	0.9333595439355219 : (s'=0) + (1 - 0.9333595439355219) : (s'=7);
	[pass_3_1]	      s=3 ->
	0.7899505766062603 : (s'=1) + (1 - 0.7899505766062603) : (s'=7);
	[pass_3_2]	      s=3 ->
	0.8004381389526393 : (s'=2) + (1 - 0.8004381389526393) : (s'=7);
	[pass_3_3]	      s=3 ->
	0.8351767080833641 : (s'=3) + (1 - 0.8351767080833641) : (s'=7);
	[pass_3_4]	      s=3 ->
	0.5240994419076611 : (s'=4) + (1 - 0.5240994419076611) : (s'=7);
	[pass_3_5]	      s=3 ->
	0.4531457687195392 : (s'=5) + (1 - 0.4531457687195392) : (s'=7);
	[pass_3_6]	      s=3 ->
	0.7505400795906765 : (s'=6) + (1 - 0.7505400795906765) : (s'=7);
	[shoot_3]	       s=3 ->
	0.004558693174623275 : (s'=8) + (1 - 0.004558693174623275) : (s'=7);

	// player actions from zone 4 (s=4)
	[pass_4_0]	      s=4 ->
	0.8403041825095057 : (s'=0) + (1 - 0.8403041825095057) : (s'=7);
	[pass_4_1]	      s=4 ->
	0.9075418112969391 : (s'=1) + (1 - 0.9075418112969391) : (s'=7);
	[pass_4_2]	      s=4 ->
	0.7641653905053599 : (s'=2) + (1 - 0.7641653905053599) : (s'=7);
	[pass_4_3]	      s=4 ->
	0.44807121661721067 : (s'=3) + (1 - 0.44807121661721067) : (s'=7);
	[pass_4_4]	      s=4 ->
	0.6910486510892877 : (s'=4) + (1 - 0.6910486510892877) : (s'=7);
	[pass_4_5]	      s=4 ->
	0.43635634028892456 : (s'=5) + (1 - 0.43635634028892456) : (s'=7);
	[pass_4_6]	      s=4 ->
	0.2033271719038817 : (s'=6) + (1 - 0.2033271719038817) : (s'=7);
	[shoot_4]	       s=4 ->
	0.01550131926121372 : (s'=8) + (1 - 0.01550131926121372) : (s'=7);

	// player actions from zone 5 (s=5)
	[pass_5_0]	      s=5 ->
	0.8108108108108109 : (s'=0) + (1 - 0.8108108108108109) : (s'=7);
	[pass_5_1]	      s=5 ->
	0.7074829931972789 : (s'=1) + (1 - 0.7074829931972789) : (s'=7);
	[pass_5_2]	      s=5 ->
	0.8050749711649365 : (s'=2) + (1 - 0.8050749711649365) : (s'=7);
	[pass_5_3]	      s=5 ->
	0.7485380116959064 : (s'=3) + (1 - 0.7485380116959064) : (s'=7);
	[pass_5_4]	      s=5 ->
	0.6368330464716007 : (s'=4) + (1 - 0.6368330464716007) : (s'=7);
	[pass_5_5]	      s=5 ->
	0.5706607650964275 : (s'=5) + (1 - 0.5706607650964275) : (s'=7);
	[pass_5_6]	      s=5 ->
	0.6009538950715422 : (s'=6) + (1 - 0.6009538950715422) : (s'=7);
	[shoot_5]	       s=5 ->
	0.04394754149096677 : (s'=8) + (1 - 0.04394754149096677) : (s'=7);

	// player actions from zone 6 (s=6)
	[pass_6_0]	      s=6 ->
	0.8677839851024208 : (s'=0) + (1 - 0.8677839851024208) : (s'=7);
	[pass_6_1]	      s=6 ->
	0.4412532637075718 : (s'=1) + (1 - 0.4412532637075718) : (s'=7);
	[pass_6_2]	      s=6 ->
	0.7472620050547599 : (s'=2) + (1 - 0.7472620050547599) : (s'=7);
	[pass_6_3]	      s=6 ->
	0.9098045498237745 : (s'=3) + (1 - 0.9098045498237745) : (s'=7);
	[pass_6_4]	      s=6 ->
	0.43578721117678665 : (s'=4) + (1 - 0.43578721117678665) : (s'=7);
	[pass_6_5]	      s=6 ->
	0.44190871369294604 : (s'=5) + (1 - 0.44190871369294604) : (s'=7);
	[pass_6_6]	      s=6 ->
	0.5506458797327394 : (s'=6) + (1 - 0.5506458797327394) : (s'=7);
	[shoot_6]	       s=6 ->
	0.016736401673640166 : (s'=8) + (1 - 0.016736401673640166) : (s'=7);

	// absorbing states
	[] s=7 -> (s'=7);
	[] s=8 -> (s'=8);

endmodule

label "possession_lost" = (s=7);
label "goal" = (s=8);