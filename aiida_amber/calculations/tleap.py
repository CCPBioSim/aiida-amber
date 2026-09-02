"""
Calculations provided by aiida_amber.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

import os

from aiida.common import CalcInfo, datastructures
from aiida.engine import CalcJob
from aiida.orm import FolderData, List, SinglefileData
from aiida.plugins import DataFactory

TleapParameters = DataFactory("amber.tleap")


class TleapCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the tleap executable.

    AiiDA plugin wrapper for the amber 'tleap' command.
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
        spec.inputs["metadata"]["options"]["parser_name"].default = "amber.tleap"
        spec.input('metadata.options.output_filename', valid_type=str,
                   default='tleap.out', help='name of file produced by default.')
        spec.input('metadata.options.output_dir', valid_type=str, default=os.getcwd(),
                help='Directory where output files will be saved when parsed.')
        spec.input('parameters', valid_type=TleapParameters,
                   help='Command line parameters for tleap')
        spec.input("tleapscript", valid_type=SinglefileData,
                   help="input file for tleap commands")

        # optional inputs
        spec.input_namespace("tleap_inpfiles", valid_type=SinglefileData,
                    required=False, dynamic=True, help="inputs referenced in tleap input file")
        spec.input_namespace("tleap_dirs", valid_type=FolderData, required=False, dynamic=True,
                   help="path to directory where inputs referenced in tleap input file are")
        spec.input_namespace("dirs", valid_type=FolderData, required=False, dynamic=True,
                   help="path to directory where custom leaprc are")

        # required outputs
        spec.output('stdout', valid_type=SinglefileData, help='stdout')

        # optional outputs

        # set the list of output file names as an input so that it can be
        # iterated over in the parser later.
        spec.input('tleap_outfiles', valid_type=List, required=False,
                   help='List of tleap output file names.')

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
        # pylint: disable=too-many-branches
        codeinfo = datastructures.CodeInfo()

        # Setup data structures for files.
        input_options = [
            "tleapscript",
            "tleap_inpfiles",
            "tleap_dirs",
            "dirs",
        ]
        output_options = []
        cmdline_input_files = {}
        input_files = []
        output_files = []

        # Map input files to AiiDA plugin data types.
        for item in input_options:
            if item in self.inputs:
                # If we have a dynamics data type then iterate the dict.
                if item == "tleap_dirs":
                    for directory, obj in self.inputs[item].items():
                        input_files.append(
                            (
                                obj.uuid,
                                ".",
                                directory,
                            )
                        )
                elif item == "tleap_inpfiles":
                    for _, obj in self.inputs[item].items():
                        input_files.append(
                            (
                                obj.uuid,
                                obj.filename,
                                obj.filename,
                            )
                        )
                elif item == "dirs":
                    cmdline_input_files[item] = self.inputs[item].filename
                    for directory, obj in self.inputs[item].items():
                        input_files.append(
                            (
                                obj.uuid,
                                ".",
                                directory,
                            )
                        )
                else:
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
        if "tleap_outfiles" in self.inputs:  # check there are output files.
            for name in self.inputs.tleap_outfiles:
                output_files.append(str(name))  # save output filename to list

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
