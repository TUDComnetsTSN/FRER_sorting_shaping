# FRER with dynamic History Length, sorting, and shaping function


## Pre-print
- https://zenodo.org/records/17105428


## Plotting tools
- run_sim.py: Build and run simulation and export the vec to csv files
    - EX: `python3 run_sim.py --export --prefix dynamicHL`
    - baseline_linkDelay.csv requires manually run: `opp_scavetool export --filter 'name =~ "linkDelay:vector"' -o baseline_linkDelay.csv General-#0.vec` from the results folder.
- run_jitter_experiments.py
    - run with different Jitter configuration

#### Fig. 3.
- plot_jitter_ratios.py: The out-of-order ratio and duplicate ratio are presented.
#### Fig. 4.
- plot_arrivalJitter.py: Plot inter-arrival interval jitter in CDF, box, or violin plot.
#### Fig. 5.
- plot_linkDelay.py: Plot link delay, history length, and reordering buffer size.
#### Fig. 6.
- plot_seqNum.py: Plot the sequence number over time.
#### Old figure
- plot_barChart.py: Plot the bar chart for out-of-order ratio, and packet duplicate ratio.

