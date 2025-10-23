# FRER with dynamic History Length, sorting, and shaping function


## Pre-print Paper
- https://zenodo.org/records/17105428

### Info
- Simulation scenario is defined in `scenario.xml`.
- Topology is in .ned file. No wireless links so far, only Ethernet links with the delay configuration based on `scenario.xml`.
- The parameters which can be configured in the `omnetpp.ini` are below:
    ```*.s2.bridging.streamRelay.merger.seqNum.record = vector
    *.s2.bridging.streamRelay.merger.enableReordering = false
    *.s2.bridging.streamRelay.merger.dynamicBuffersize = true
    *.s2.bridging.streamRelay.merger.periodicEmission = false
    *.s2.bridging.streamRelay.merger.bufferSize = 5
    *.s2.bridging.streamRelay.merger.timerInterval = 10ms
    *.s2.bridging.streamRelay.merger.senderTransmissionInterval = 1ms
    *.s2.bridging.streamRelay.merger.jitter = 10ms
    *.s2.bridging.streamRelay.merger.startSequence = 0
    ```
  - Enable `dynamicBuffersize` = enable the DHL algo. in the paper.
  - Enable `enableReordering` = enable the sorting algo. in the paper.
  - Enable `periodicEmission` = enable the shaping function in the paper.
  - Therefore, if the users plan to apply the sorting plus shaping algo. then enable both `enableReordering` and `periodicEmission`.
  - `bufferSize` = the default history length
  - `timerInterval` = \tau in the paper, which means in each \tau time the history lengh will be updated.
  - `jitter` = the parameter J in the DHL algo.
### INET code
- The inet source code is here: https://github.com/TUDComnetsTSN/inet4.5_FRER

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
  - Also plot the link delay seperately for the presentation.
#### Fig. 6.
- plot_seqNum.py: Plot the sequence number over time.
#### Old figure
- plot_barChart.py: Plot the bar chart for out-of-order ratio, and packet duplicate ratio.

