"""Test for parmed cli script"""

import os
import subprocess

from aiida.orm.nodes.process.process import ProcessState

from aiida_amber.utils import searchprevious

from .. import TEST_DIR


def test_launch_parmed():
    """
    Run an instance of parmed.
    """
    # get input file paths
    parmed_in = os.path.join(TEST_DIR, "input_files", "parmed", "parmed_1264_na.in")
    prmtop_in = os.path.join(TEST_DIR, "input_files", "parmed", "1D23_tip4pew.prmtop")
    inpcrd_in = os.path.join(TEST_DIR, "input_files", "parmed", "1D23_tip4pew.inpcrd")

    subprocess.check_output(
        [
            "aiida_parmed",
            "-i",
            parmed_in,
            "-p",
            prmtop_in,
            "-c",
            inpcrd_in,
        ]
    )

    # append run process to qb
    qb = searchprevious.build_query()
    prev_calc = qb.first()[0]
    # check the process has finished and exited correctly
    assert prev_calc.process_state == ProcessState.FINISHED
    assert prev_calc.exit_status == 0
