"""Test for sander cli script"""

import os
import subprocess

from aiida.orm.nodes.process.process import ProcessState

from aiida_amber.utils import searchprevious

from .. import TEST_DIR


def test_launch_sander():
    """
    Run an instance of sander.
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
    # pylint: disable=unused-variable
    qb = searchprevious.build_query()
    # pylint: disable=unsubscriptable-object
    prev_calc = qb.first()[0]
    # check the process has finished and exited correctly
    assert prev_calc.process_state == ProcessState.FINISHED
    assert prev_calc.exit_status == 0
