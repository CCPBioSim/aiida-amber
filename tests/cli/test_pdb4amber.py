""" Test for pdb4amber cli script

"""

import os
import subprocess

from aiida.orm.nodes.process.process import ProcessState

from aiida_amber.utils import searchprevious

from click.testing import CliRunner
from aiida_amber.cli.pdb4amber import cli

from .. import TEST_DIR


def test_launch_pdb4amber():
    """
    Run an instance of pdb4amber.
    Verify the actual installed console-script entry point (aiida_pdb4amber) works.
    """
    # get input file paths
    inp = os.path.join(TEST_DIR, "input_files", "pdb4amber", "Protein.pdb")

    subprocess.check_output(
        [
            "aiida_pdb4amber",
            "-i", inp,
            "--out", "test.pdb",
            "--dry",
            "--reduce",
            "--logfile", "test.log",
            "--leap-template", 
        ]
    )
    # append run process to qb
    qb = searchprevious.build_query()
    prev_calc = qb.first()[0]
    # check the process has finished and exited correctly
    assert prev_calc.process_state == ProcessState.FINISHED
    assert prev_calc.exit_status == 0


def test_cli_launch_pdb4amber(pdb4amber_code):
    """Invoke the pdb4amber cli in-process to cover cli/pdb4amber.py."""
    inp = os.path.join(TEST_DIR, "input_files", "pdb4amber", "Protein.pdb")
    result = CliRunner().invoke(
        cli,
        ["-i", inp, "--out", "test.pdb", "--dry", "--reduce",
         "--logfile", "test.log", "--leap-template"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
