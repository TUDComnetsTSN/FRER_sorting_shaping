#!/usr/bin/env python3
import re
import subprocess
import sys
import time
from pathlib import Path
from export_vector import export_seqnum_vector

ROOT        = Path(__file__).resolve().parent        # …/FRER/src
SIM_DIR     = ROOT.parent / "simulations"             # …/FRER/simulations
INI_PATH    = SIM_DIR / "omnetpp.ini"
RUN_SIM     = ROOT / "run_sim.py"

# read original ini once
orig_ini = INI_PATH.read_text()

try:
    for j in range(0, 11):
        print(f"\n=== Running simulation with jitter={j}ms ===")

        # 1) build patched ini by replacing the entire line's value via a function
        pattern = r'(\*\.s2\.bridging\.streamRelay\.merger\.jitter\s*=\s*)\S+'
        def repl(m):
            # m.group(1) is the "…jitter = " prefix
            return f"{m.group(1)}{j}ms"
        patched = re.sub(pattern, repl, orig_ini)
        INI_PATH.write_text(patched)

        # 2) run the sim
        subprocess.run([sys.executable, str(RUN_SIM)], check=True)

        # 3) pick up the newest .vec file
        results_dir = SIM_DIR / "results"
        vecs = sorted(results_dir.glob("*.vec"))
        if not vecs:
            raise FileNotFoundError(f"No .vec file found after jitter={j}ms")
        vec_name = vecs[-1].name

        # 4) export seqNum via your export_vector helper
        csv_name = f"dynamicHL_J{j}_seqNum.csv"
        export_seqnum_vector(
            'name =~ "seqNum:vector"',
            csv_name,
            vec_name
        )
        time.sleep(1)  # give some time for the export to finish

finally:
    # restore the original ini
    INI_PATH.write_text(orig_ini)
    print("\nRestored original omnetpp.ini")
