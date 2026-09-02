"""
Calculations provided by aiida_amber.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

import os

from aiida.common import CalcInfo, datastructures
from aiida.engine import CalcJob
from aiida.orm import List, SinglefileData
from aiida.plugins import DataFactory

AntechamberParameters = DataFactory("amber.antechamber")


class AntechamberCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the antechamber executable.

    AiiDA plugin wrapper for the amber 'antechamber' command.
    """

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs['metadata']['options']['withmpi'].default = False
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        }

        # required inputs
        spec.inputs["metadata"]["options"]["parser_name"].default = "amber.antechamber"
        spec.input('metadata.options.output_filename', valid_type=str,
                   default='antechamber.out', help='name of file produced by default.')
        spec.input('metadata.options.output_dir', valid_type=str, default=os.getcwd(),
                help='Directory where output files will be saved when parsed.')
        spec.input('parameters', valid_type=AntechamberParameters,
                   help='Command line parameters for antechamber')
        spec.input("input_file", valid_type=SinglefileData,
                   help="input structure file for antechamber")

        # optional inputs
        spec.input('charge_file', valid_type=SinglefileData, required=False, help='charge file')
        spec.input('additional_file', valid_type=SinglefileData, required=False, help='additional file')
        spec.input('res_top_file', valid_type=SinglefileData, required=False, help='residue toplogy file')
        spec.input('check_file', valid_type=SinglefileData, required=False, help='check file for gaussian')
        spec.input('esp_file', valid_type=SinglefileData, required=False, help='gaussian esp file')

        # required outputs
        spec.output('stdout', valid_type=SinglefileData, help='stdout')
        spec.output('output_file', valid_type=SinglefileData, help='output file')

        # optional outputs

        # set the list of output file names as an input so that it can be
        # iterated over in the parser later.
        spec.input('antechamber_outfiles', valid_type=List, required=False,
                   help='List of antechamber output file names.')

        # IMPORTANT:
        # Use spec.outputs.dynamic = True to make the entire output namespace
        # fully dynamic. This means any number of output files
        # can be linked to a node.
        spec.outputs.dynamic = True
        spec.inputs.dynamic = True
        spec.inputs['metadata']['options'].dynamic = True

        spec.exit_code(300, "ERROR_MISSING_OUTPUT_FILES",
            message="Calculation did not produce all expected output files.")

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should
            temporarily place all files needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()

        # Setup data structures for files.
        # Any input files used
        input_options = [
            "input_file",
            "charge_file",
            "additional_file",
            "res_top_file",
            "check_file",
            "esp_file",
        ]
        # Any output files produced
        output_options = ["o"]
        cmdline_input_files = {}
        input_files = []
        output_files = []

        # Map input files to AiiDA plugin data types.
        for item in input_options:
            if item in self.inputs:
                cmdline_input_files[item] = self.inputs[item].filename
                input_files.append(
                    (
                        self.inputs[item].uuid,
                        self.inputs[item].filename,
                        self.inputs[item].filename,
                    )
                )

        # Add output files to retrieve list.
        output_files.append(self.metadata.options.output_filename)
        for item in output_options:
            if item in self.inputs.parameters:
                output_files.append(self.inputs.parameters[item])

        # Form the commandline.
        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(cmdline_input_files)

        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = input_files
        calcinfo.retrieve_list = output_files

        return calcinfo
