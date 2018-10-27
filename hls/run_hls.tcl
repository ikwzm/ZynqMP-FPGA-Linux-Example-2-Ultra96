open_project -reset negative
set_top negative
add_files     ../negative.c
add_files -tb ../negative_tb.c

open_solution -reset "solution1"
set_part {xczu3eg-sfva625-1-e} -tool vivado
create_clock -period 10 -name default

# csim_design
csynth_design
# cosim_design
export_design -rtl verilog -format ip_catalog

exit
