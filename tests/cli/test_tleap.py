"""Test for tleap cli script"""

import os
import subprocess

from aiida.orm.nodes.process.process import ProcessState

from aiida_amber.utils import searchprevious

from .. import TEST_DIR


def test_launch_tleap():
    """
    Run an instance of tleap.
    """
    # get input file paths
    tleap_in = os.path.join(TEST_DIR, "input_files", "tleap", "tleap.in")

    subprocess.check_output(
        [
            "aiida_tleap",
            "-f",
            tleap_in,
        ]
    )
    # append run process to qb
    qb = searchprevious.build_query()
    prev_calc = qb.first()[0]
    # check the process has finished and exited correctly
    assert prev_calc.process_state == ProcessState.FINISHED
    assert prev_calc.exit_status == 0
