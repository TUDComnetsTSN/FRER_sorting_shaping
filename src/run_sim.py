#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from pathlib import Path
import argparse


def export_vector(filter_expr: str, output_filename: str, vec_path: Path):
    """
    Runs `opp_scavetool export` on the given .vec file and writes the CSV.
    """
    output_path = vec_path.parent / output_filename
    cmd = [
        "opp_scavetool", "export",
        "--filter", filter_expr,
        "-o", str(output_path),
        str(vec_path)
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✔ Exported `{vec_path.name}` → `{output_path.name}`")
    except subprocess.CalledProcessError as e:
        print(f"✖ Export failed for {vec_path.name}: {e}")


def run_simulation(script_dir: Path, frer_exe: Path, ned_arg: str, x_arg: str, image_path: Path, src_inet: Path, ini_path: Path) -> subprocess.CompletedProcess:
    """
    Executes the FRER simulation and returns the completed process.
    """
    cmd = [
        str(frer_exe), '-u', 'Cmdenv',
        '-n', ned_arg,
        '-x', x_arg,
        f"--image-path={image_path}",
        '-l', str(src_inet),
        str(ini_path)
    ]
    print(f"Running: {cmd!s}", file=sys.stderr)
    return subprocess.run(
        cmd,
        cwd=str(script_dir),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )


def find_vec_file(results_dir: Path, specified: str = None) -> Path:
    """
    Finds the .vec file in results_dir. If specified provided, checks that first.
    """
    if specified:
        candidate = Path(specified)
        if not candidate.exists():
            candidate = results_dir / candidate.name
        if candidate.exists():
            return candidate
        else:
            raise FileNotFoundError(f"Specified vec file not found: {specified}")
    vecs = sorted(results_dir.glob('*.vec'))
    if not vecs:
        raise FileNotFoundError(f"No .vec files found in {results_dir}")
    return vecs[0]


def export_all_vectors(prefix: str , vec_file: Path):
    """
    Exports both historyLength and seqNum vectors to CSV with the given prefix.
    """
    exports = [
        ('name =~ "historyLength:vector"', f"{prefix}_historyLength.csv"),
        ('name =~ "seqNum:vector"', f"{prefix}_seqNum.csv"),
    ]
    for filter_expr, out_name in exports:
        export_vector(filter_expr, out_name, vec_file)


def main():
    parser = argparse.ArgumentParser(
        description="Run FRER sim and optionally export vec to CSV"
    )
    parser.add_argument(
        "--prefix", type=str, default=None,
        help="Prefix for output CSV files (e.g. baseline, DynamicHL). Required if --export is set."
    )
    parser.add_argument(
        "--export", action="store_true",
        help="If set, after the run it will export vectors to CSV (requires --prefix)."
    )
    parser.add_argument(
        "--vec-filename", type=str, default=None,
        help="Specify the .vec file to export (default: first in results)"
    )
    args = parser.parse_args()

    # Setup paths
    script_dir = Path(__file__).resolve().parent
    frer_exe = script_dir / 'FRER'
    if not frer_exe.exists() or not os.access(frer_exe, os.X_OK):
        print(f"Error: FRER binary not usable at {frer_exe}", file=sys.stderr)
        sys.exit(1)

    inet_root = (script_dir.parent / '..' / 'inet4.5').resolve()
    image_path = inet_root / 'images'
    src_inet = inet_root / 'src' / 'INET'
    simulations_dir = script_dir.parent / 'simulations'
    results_dir = simulations_dir / 'results'
    ini_path = simulations_dir / 'omnetpp.ini'
    if not ini_path.exists():
        print(f"Error: ini file not found at {ini_path}", file=sys.stderr)
        sys.exit(1)

    ned_paths = [
        simulations_dir,
        script_dir,
        inet_root / 'examples',
        inet_root / 'showcases',
        inet_root / 'src',
        inet_root / 'tests' / 'validation',
        inet_root / 'tests' / 'networks',
        inet_root / 'tutorials'
    ]
    ned_arg = ":".join(str(p.resolve()) for p in ned_paths)
    x_arg = (
        "inet.applications.voipstream;"
        "inet.common.selfdoc;"
        "inet.emulation;"
        "inet.examples.emulation;"
        "inet.examples.voipstream;"
        "inet.linklayer.configurator.gatescheduling.z3;"
        "inet.showcases.emulation;"
        "inet.showcases.visualizer.osg;"
        "inet.transportlayer.tcp_lwip;"
        "inet.visualizer.osg"
    )

    # Run simulation
    try:
        result = run_simulation(script_dir, frer_exe, ned_arg, x_arg, image_path, src_inet, ini_path)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"\nFRER exited with code {e.returncode}", file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode)
    # pause briefly to let files flush
    time.sleep(1)

    # only export if explicitly asked
    if args.export:
        if not args.prefix:
            print("Error: --export requires you to also pass --prefix", file=sys.stderr)
            sys.exit(1)
        try:
            vec_file = find_vec_file(results_dir, args.vec_filename)
            export_all_vectors(args.prefix, vec_file)
        except FileNotFoundError as fnf:
            print(f"Error: {fnf}", file=sys.stderr)
            sys.exit(1)
    else:
        print("✔ Simulation complete; skipping CSV export (use --export to enable).")


if __name__ == "__main__":
    main()
