""" Tests for tleap calculations."""
import os

from aiida.engine import run
from aiida.plugins import CalculationFactory, DataFactory

from aiida_amber.data.tleap_input import TleapInputData


def run_tleap(tleap_code):
    """Run an instance of sander and return the results."""

    # Prepare input parameters
    TleapParameters = DataFactory("amber.tleap")
    parameters = TleapParameters({})

    # set up calculation
    inputs = {
        "code": tleap_code,
        "parameters": parameters,
        "metadata": {
            "description": "tleap test",
        },
    }

    # Prepare input parameters in AiiDA formats.
    # Set the tleap script as a TleapInputData type node
    inputs["tleapscript"] = TleapInputData(
        file=os.path.join(os.getcwd(), "tests/input_files/tleap", "tleap.in")
    )

    # Find the inputs and outputs referenced in the tleap script
    calc_inputs, calc_outputs = inputs["tleapscript"].calculation_inputs_outputs
    # add input files and dirs referenced in tleap file into inputs
    inputs.update(calc_inputs)
    inputs.update(calc_outputs)

    result = run(CalculationFactory("amber.tleap"), **inputs)
    return result


def test_process(tleap_code):
    """Test running a tleap calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_tleap(tleap_code)

    assert "stdout" in result
    assert "complex_prmtop" in result
    assert "complex_inpcrd" in result


def test_file_name_match(tleap_code):
    """Test that the file names returned match what was specified on inputs."""

    result = run_tleap(tleap_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "tleap.out"
    assert (
        result["complex_prmtop"].base.repository.list_object_names()[0]
        == "complex.prmtop"
    )
    assert (
        result["complex_inpcrd"].base.repository.list_object_names()[0]
        == "complex.inpcrd"
    )
