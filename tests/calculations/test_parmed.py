""" Tests for parmed calculations."""
import os

from aiida.engine import run
from aiida.orm import SinglefileData
from aiida.plugins import CalculationFactory, DataFactory

from aiida_amber.data.parmed_input import ParmedInputData


def run_parmed(parmed_code):
    """Run an instance of sander and return the results."""

    # Prepare input parameters
    ParmedParameters = DataFactory("amber.parmed")
    parameters = ParmedParameters(
        {
            "parm": "1D23_tip4pew.prmtop",
            "inpcrd": "1D23_tip4pew.inpcrd",
        }
    )

    # set up calculation
    inputs = {
        "code": parmed_code,
        "parameters": parameters,
        "metadata": {
            "description": "parmed test",
        },
    }

    # Prepare input parameters in AiiDA formats.
    # Set the parmed script as a ParmedInputData type node
    inputs["parmed_script"] = ParmedInputData(
        file=os.path.join(os.getcwd(), "tests/input_files/parmed", "parmed_1264_na.in")
    )

    # Find the inputs and outputs referenced in the parmed script
    calc_inputs, calc_outputs = inputs["parmed_script"].calculation_inputs_outputs
    # add input files and dirs referenced in parmed file into inputs
    inputs.update(calc_inputs)
    inputs.update(calc_outputs)

    inputs["prmtop_files"] = {}
    inputs["prmtop_files"]["1D23_tip4pew_prmtop"] = SinglefileData(
        file=os.path.join(
            os.getcwd(), "tests/input_files/parmed", "1D23_tip4pew.prmtop"
        )
    )
    inputs["inpcrd_files"] = {}
    inputs["inpcrd_files"]["1D23_tip4pew_inpcrd"] = SinglefileData(
        file=os.path.join(
            os.getcwd(), "tests/input_files/parmed", "1D23_tip4pew.inpcrd"
        )
    )

    result = run(CalculationFactory("amber.parmed"), **inputs)
    return result


def test_process(parmed_code):
    """Test running a parmed calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_parmed(parmed_code)

    assert "stdout" in result
    assert "output_files_1D23_1264_na_tip4pew_prmtop" in result
    assert "output_files_1D23_1264_na_tip4pew_inpcrd" in result


def test_file_name_match(parmed_code):
    """Test that the file names returned match what was specified on inputs."""

    result = run_parmed(parmed_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "parmed.out"
    assert (
        result[
            "output_files_1D23_1264_na_tip4pew_prmtop"
        ].base.repository.list_object_names()[0]
        == "1D23_1264_na_tip4pew.prmtop"
    )
    assert (
        result[
            "output_files_1D23_1264_na_tip4pew_inpcrd"
        ].base.repository.list_object_names()[0]
        == "1D23_1264_na_tip4pew.inpcrd"
    )
