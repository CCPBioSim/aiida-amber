"""Test for sander cli script"""

import os
import subprocess

from aiida.orm.nodes.process.process import ProcessState
from click.testing import CliRunner

from aiida_amber.cli.sander import cli
from aiida_amber.utils import searchprevious

from .. import TEST_DIR


def test_launch_sander():
    """
    Run an instance of sander.
    Verify the actual installed console-script entry point (aiida_sander) works.
    """
    # get input file paths
    mdin = os.path.join(TEST_DIR, "input_files", "sander", "01_Min.in")
    prmtop = os.path.join(TEST_DIR, "input_files", "sander", "parm7")
    inpcrd = os.path.join(TEST_DIR, "input_files", "sander", "rst7")

    subprocess.check_output(
        [
            "aiida_sander",
            "-i",
            mdin,
            "-p",
            prmtop,
            "-c",
            inpcrd,
            "-o",
            "01_Min.out",
            "-r",
            "01_Min.ncrst",
            "-inf",
            "01_Min.mdinfo",
        ]
    )
    # append run process to qb
    qb = searchprevious.build_query()
    prev_calc = qb.first()[0]
    # check the process has finished and exited correctly
    assert prev_calc.process_state == ProcessState.FINISHED
    assert prev_calc.exit_status == 0


def test_cli_launch_sander(sander_code):
    """Invoke the sander cli in-process to cover cli/sander.py."""
    mdin = os.path.join(TEST_DIR, "input_files", "sander", "01_Min.in")
    prmtop = os.path.join(TEST_DIR, "input_files", "sander", "parm7")
    inpcrd = os.path.join(TEST_DIR, "input_files", "sander", "rst7")
    result = CliRunner().invoke(
        cli,
        ["-i", mdin, "-p", prmtop, "-c", inpcrd, "-o", "01_Min.out", "-r", "01_Min.ncrst", "-inf", "01_Min.mdinfo"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
