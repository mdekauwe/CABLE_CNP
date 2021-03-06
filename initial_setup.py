#!/usr/bin/env python

"""
Get repository, copy locally to user area, download and build the executables

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (11.03.2019)"
__email__ = "mdekauwe@gmail.com"

import os
import shutil
import sys
import datetime
import subprocess

sys.path.append("scripts")
from get_cable import GetCable
from build_cable import BuildCable
from run_cable_site import RunCable
from set_default_paths import set_paths

now = datetime.datetime.now()
date = now.strftime("%d_%m_%Y")
cwd = os.getcwd()
(sysname, nodename, release, version, machine) = os.uname()

#------------- User set stuff ------------- #
user = "mgk576"

#
## user directories ...
#
src_dir = "src"
run_dir = "runs"
log_dir = "logs"
plot_dir = "plots"
output_dir = "outputs"
restart_dir = "restart_files"
namelist_dir = "namelists"

# If this is set the code will download a specific repo, otherwise
user_path = "trunk_CNP"

#
## Needs different paths for NCI, storm ... this is set for my mac
## comment out the below and set your own, see scripts/set_default_paths.py
#
(met_dir, NCDIR, NCMOD, FC, CFLAGS, LD, LDFLAGS) = set_paths(nodename)

# ------------------------------------------- #

# clean out old src directory
if os.path.exists(src_dir):
    shutil.rmtree(src_dir)
    os.makedirs(src_dir)

#
## Get CABLE ...
#
G = GetCable(src_dir=src_dir, user=user)

if user_path is None:
    # Setup for the head of the trunk
    repo = "Trunk"
    G.main(repo_name=repo, trunk=True)
else:
    # Setup for user specified path
    repo = user_path
    G.main(repo_name=repo, trunk=False, share=True)

#
## Build CABLE ...
#
B = BuildCable(src_dir=src_dir, NCDIR=NCDIR, NCMOD=NCMOD, FC=FC,
               CFLAGS=CFLAGS, LD=LD, LDFLAGS=LDFLAGS)
B.main(repo_name=repo)

if not os.path.exists(run_dir):
    os.makedirs(run_dir)

for fname in ["run_cable_site_CNP.py", "seasonal_plot.py", \
              "seasonal_plot_CNP.py", "plot_casa_outputs_simulation.py",
              "clean_up.sh"]:
    infname = os.path.join("scripts", fname)
    ofname = os.path.join(run_dir, fname)
    shutil.copy(infname, ofname)

fname = "build_cable.py"
infname = os.path.join("scripts", fname)
shutil.copy(infname, fname)
