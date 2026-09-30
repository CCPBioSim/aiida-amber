"""Test for antechamber cli script"""

import os
import subprocess

from aiida.orm.nodes.process.process import ProcessState
from click.testing import CliRunner

from aiida_amber.cli.antechamber import cli
from aiida_amber.utils import searchprevious

from .. import TEST_DIR


def test_launch_antechamber():
    """
    Run an instance of antechamber.
    Verify the actual installed console-script entry point (aiida_antechamber) works.
    """
    # get input file paths
    inp = os.path.join(TEST_DIR, "input_files", "antechamber", "LigA.mol2")

    subprocess.check_output(
        [
            "aiida_antechamber",
            "-i",
            inp,
            "-o",
            "LigandA.mol2",
            "-fi",
            "mol2",
            "-fo",
            "mol2",
            "-c",
            "bcc",
            "-pf",
            "yes",
            "-nc",
            "-2",
            "-at",
            "gaff2",
            "-j",
            "5",
            "-rn",
            "CHA",
        ]
    )
    # append run process to qb
    qb = searchprevious.build_query()
    prev_calc = qb.first()[0]
    # check the process has finished and exited correctly
    assert prev_calc.process_state == ProcessState.FINISHED
    assert prev_calc.exit_status == 0


def test_cli_launch_antechamber(antechamber_code):
    """Invoke the antechamber cli in-process to cover cli/antechamber.py."""
    inp = os.path.join(TEST_DIR, "input_files", "antechamber", "LigA.mol2")
    result = CliRunner().invoke(
        cli,
        [
            "-i",
            inp,
            "-o",
            "LigandA.mol2",
            "-fi",
            "mol2",
            "-fo",
            "mol2",
            "-c",
            "bcc",
            "-pf",
            "yes",
            "-nc",
            "-2",
            "-at",
            "gaff2",
            "-j",
            "5",
            "-rn",
            "CHA",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
