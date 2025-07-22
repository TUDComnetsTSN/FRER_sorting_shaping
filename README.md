# FRER with dynamic History Length, sorting, and shaping function
- run_sim.py: Build and run simulation and export the vec to csv files
    - EX: `python3 run_sim.py --export --prefix dynamicHL`
    - baseline_linkDelay.csv requires manually run: `opp_scavetool export --filter 'name =~ "linkDelay:vector"' -o baseline_linkDelay.csv General-#0.vec` from the results folder.
- plot_linkDelay.py: Plot link delay, history length, and reordering buffer size.
- plot_arrivalJitter.py: Plot inter-arrival interval jitter in CDF, box, or violin plot.
- plot_barChart.py: Plot the bar chart for out-of-order ratio, and packet duplicate ratio.
- lot_seqNum.py: Plot the sequence number over time.

