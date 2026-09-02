"""
Calculations provided by aiida_amber.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""

import os

from aiida.common import CalcInfo, datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData
from aiida.plugins import DataFactory

SanderParameters = DataFactory("amber.sander")


class SanderCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the sander executable.

    AiiDA plugin wrapper for the amber 'sander' command.
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
        spec.inputs["metadata"]["options"]["parser_name"].default = "amber.sander"
        spec.input('metadata.options.output_filename', valid_type=str,
                   default='sander.out')
        spec.input('metadata.options.output_dir', valid_type=str, default=os.getcwd(),
                help='Directory where output files will be saved when parsed.')
        spec.input('parameters', valid_type=SanderParameters,
                   help='Command line parameters for sander')
        spec.input("mdin", valid_type=SinglefileData,
                   help="input control data for the min/md run.")
        spec.input("prmtop", valid_type=SinglefileData,
                   help="input molecular topology, force field, "
                   "periodic box type, atom and residue names.")
        spec.input("inpcrd", valid_type=SinglefileData,
                   help="input initial coordinates and (optionally) "
                   "velocities and periodic box size.")

        # optional inputs
        spec.input("refc", valid_type=SinglefileData, required=False,
                   help="input (optional) reference coords for position "
                   "restraints; also used for targeted MD.")
        spec.input("mtmd", valid_type=SinglefileData, required=False,
                   help="input (optional) containing list of files and "
                   "parameters for targeted MD to multiple targets.")
        spec.input("inptraj", valid_type=SinglefileData, required=False,
                   help="input coordinate sets in trajectory format, when "
                   "imin=5 or 6.")
        spec.input("inpdip", valid_type=SinglefileData, required=False,
                   help="input polarizable dipole file, when indmeth=3.")
        spec.input("cpin", valid_type=SinglefileData, required=False,
                   help="input protonation state definitions.")
        spec.input("cprestrt", valid_type=SinglefileData, required=False,
                   help="protonation state definitions, final protonation "
                   "states for restart (same format as cpin).")
        spec.input("cein", valid_type=SinglefileData, required=False,
                   help="input redox state definitions.")
        spec.input("cerestrt", valid_type=SinglefileData, required=False,
                   help="redox state definitions, final redox states for "
                   "restart (same format as cein).")
        spec.input("evbin", valid_type=SinglefileData, required=False,
                   help="input input for EVB potentials.")

        # required outputs
        spec.output('stdout', valid_type=SinglefileData, help='stdout')
        spec.output("mdout", valid_type=SinglefileData,
                    help="output user readable state info and diagnostics -o "
                    "stdout will send output to stdout (to the terminal) "
                    "instead of to a file.")
        spec.output("mdinfo", valid_type=SinglefileData,
                    help="output latest mdout-format energy info.")

        # optional outputs
        spec.output("mdcrd", valid_type=SinglefileData, required=False,
                    help="output coordinate sets saved over trajectory.")
        spec.output("mdvel", valid_type=SinglefileData, required=False,
                    help="output velocity sets saved over trajectory.")
        spec.output("mdfrc", valid_type=SinglefileData, required=False,
                    help="output force sets saved over trajectory.")
        spec.output("mden", valid_type=SinglefileData, required=False,
                    help="output extensive energy data over trajectory "
                    "(not synchronized with mdcrd or mdvel).")
        spec.output("restrt", valid_type=SinglefileData, required=False,
                    help="output final coordinates, velocity, and box "
                    "dimensions if any - for restarting run.")
        spec.output("rstdip", valid_type=SinglefileData, required=False,
                    help="output polarizable dipole file, when indmeth=3.")
        spec.output("cpout", valid_type=SinglefileData, required=False,
                    help="output protonation state data saved over trajectory.")
        spec.output("ceout", valid_type=SinglefileData, required=False,
                    help="output redox state data saved over trajectory.")
        spec.output("suffix", valid_type=str, required=False,
                    help="output this string will be added to all unspecified "
                    "output files that are printed (for multisander runs, it "
                    "will append this suffix to all output files).")

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
        input_options = [
            "mdin",
            "prmtop",
            "inpcrd",
            "refc",
            "mtmd",
            "inptraj",
            "inpdip",
            "cpin",
            "cein",
            "evbin",
        ]
        output_options = [
            "o",
            "inf",
            "x",
            "v",
            "frc",
            "e",
            "r",
            "rdip",
            "cprestrt",
            "cpout",
            "cerestrt",
            "ceout",
            "suffix",
        ]
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
