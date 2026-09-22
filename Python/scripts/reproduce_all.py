#!/usr/bin/env python3
"""Convenience driver for the open-source Python reproduction.

The default is a laptop-friendly run. The generated repository already contains
higher-cost outputs from the conversion run; use the individual scripts with larger
--starts values for publication-grade random-start statistics.
"""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]

def run(*args):
    cmd=[sys.executable,*map(str,args)]; print('+',' '.join(cmd)); subprocess.run(cmd,cwd=ROOT,check=True)

def main():
    run('scripts/validate_core.py')
    run('scripts/search_selected_phases.py')
    for I in (1.5,2.5,3.5):
        run('scripts/reproduce_fig2.py','--spin',I,'--points',21,'--starts',1)
        run('scripts/reproduce_fig6_7.py','--spin',I,'--points',31,'--tmax',1.1)
        run('scripts/reproduce_fig12.py','--spin',I,'--points',31,'--tmax',1.1)
    run('scripts/reproduce_fig3.py','--points',11,'--starts',1)
    run('scripts/reproduce_fig13.py')
    print('Done. See results/.')
if __name__=='__main__': main()
