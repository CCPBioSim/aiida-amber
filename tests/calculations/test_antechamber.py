"""Tests for antechamber calculations."""

import os

from aiida.engine import run
from aiida.plugins import CalculationFactory, DataFactory

from .. import TEST_DIR


def run_antechamber(antechamber_code):
    """Run an instance of antechamber and return the results."""

    # Prepare input parameters
    AntechamberParameters = DataFactory("amber.antechamber")
    parameters = AntechamberParameters(
        {
            "o": "LigandA.mol2",
            "fi": "mol2",
            "fo": "mol2",
            "c": "bcc",
            "pf": "yes",
            "nc": -2,
            "at": "gaff2",
            "j": 5,
            "rn": "CHA",
        }
    )

    SinglefileData = DataFactory("core.singlefile")
    inp = SinglefileData(file=os.path.join(TEST_DIR, "input_files/antechamber", "LigA.mol2"))

    # set up calculation
    inputs = {
        "code": antechamber_code,
        "parameters": parameters,
        "input_file": inp,
        "metadata": {
            "description": "antechamber test",
        },
    }

    result = run(CalculationFactory("amber.antechamber"), **inputs)

    return result


def test_process(antechamber_code):
    """Test running a antechamber calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_antechamber(antechamber_code)

    assert "stdout" in result
    assert "output_file" in result


def test_file_name_match(antechamber_code):
    """Test that the file names returned match what was specified on inputs."""

    result = run_antechamber(antechamber_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "antechamber.out"
    assert result["output_file"].base.repository.list_object_names()[0] == "LigandA.mol2"
