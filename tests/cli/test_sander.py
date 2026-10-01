"""Test for sander cli script"""

import os
import subprocess

from aiida.orm.nodes.process.process import ProcessState
from click.testing import CliRunner

from aiida_amber.cli.sander import cli
from aiida_amber.utils import searchprevious

from .. import TEST_DIR


def test_launch_sander_min():
    """
    Run an instance of sander.
    Verify the actual installed console-script entry point (aiida_sander) works.
    """
    # get input file paths
    min = os.path.join(TEST_DIR, "input_files", "sander", "01_Min.in")
    prmtop = os.path.join(TEST_DIR, "input_files", "sander", "top.parm7")
    inpcrd = os.path.join(TEST_DIR, "input_files", "sander", "inpcrd.rst7")

    subprocess.check_output(
        [
            "aiida_sander",
            "-i",
            min,
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


def test_cli_launch_sander_min(sander_code):
    """Invoke the sander cli in-process to cover cli/sander.py."""
    min = os.path.join(TEST_DIR, "input_files", "sander", "01_Min.in")
    prmtop = os.path.join(TEST_DIR, "input_files", "sander", "top.parm7")
    inpcrd = os.path.join(TEST_DIR, "input_files", "sander", "inpcrd.rst7")
    result = CliRunner().invoke(
        cli,
        ["-i", min, "-p", prmtop, "-c", inpcrd, "-o", "01_Min.out", "-r", "01_Min.ncrst", "-inf", "01_Min.mdinfo"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0


def test_launch_sander_md():
    """
    Run an instance of sander.
    Verify the actual installed console-script entry point (aiida_sander) works.
    """
    # get input file paths
    mdin = os.path.join(TEST_DIR, "input_files", "sander", "02_md.in")
    prmtop = os.path.join(TEST_DIR, "input_files", "sander", "top.parm7")
    inpcrd = os.path.join(TEST_DIR, "input_files", "sander", "inpcrd.rst7")

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
            "02_md.out",
            "-r",
            "02_md.ncrst",
            "-inf",
            "02_md.mdinfo",
        ]
    )
    # append run process to qb
    qb = searchprevious.build_query()
    prev_calc = qb.first()[0]
    # check the process has finished and exited correctly
    assert prev_calc.process_state == ProcessState.FINISHED
    assert prev_calc.exit_status == 0


def test_cli_launch_sander_md(sander_code):
    """Invoke the sander cli in-process to cover cli/sander.py."""
    mdin = os.path.join(TEST_DIR, "input_files", "sander", "02_md.in")
    prmtop = os.path.join(TEST_DIR, "input_files", "sander", "top.parm7")
    inpcrd = os.path.join(TEST_DIR, "input_files", "sander", "inpcrd.rst7")
    result = CliRunner().invoke(
        cli,
        ["-i", mdin, "-p", prmtop, "-c", inpcrd, "-o", "02_md.out", "-r", "02_md.ncrst", "-inf", "02_md.mdinfo"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
