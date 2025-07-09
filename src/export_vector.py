import subprocess
from pathlib import Path

def export_seqnum_vector(filter_expr: str,
                         output_filename: str,
                         vec_filename: str):
    """
    Runs `opp_scavetool export` on the given .vec file and writes the CSV
    into the same directory as the .vec.

    Args:
        filter_expr (str): e.g. 'name =~ "seqNum:vector"'
        output_filename (str): e.g. 'output.csv'
        vec_filename (str): e.g. 'General-#0.vec'
    """
    # 1) Locate this script and go up to the FRER folder
    script_dir = Path(__file__).resolve().parent       # …/samples/FRER/src
    frer_dir   = script_dir.parent                     # …/samples/FRER

    # 2) Build the path to the .vec directory
    results_dir = frer_dir / "simulations" / "results" # …/samples/FRER/simulations/results
    vec_path    = results_dir / vec_filename           # …/results/General-#0.vec

    # 3) Set the output CSV in the same folder
    output_path = vec_path.parent / output_filename    # …/results/output.csv

    # 4) Invoke scavetool
    cmd = [
        "opp_scavetool", "export",
        "--filter", filter_expr,
        "-o", str(output_path),
        str(vec_path)
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✔ Exported `{vec_path.name}` → `{output_path}`")
    except subprocess.CalledProcessError as e:
        print(f"✖ Export failed: {e}")

if __name__ == "__main__":
    export_seqnum_vector(
        'name =~ "historyLength:vector"',
        "dynamicHL_historyLength.csv",
        "General-#0.vec"
    )
