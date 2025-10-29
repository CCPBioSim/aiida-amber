"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""
# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from voluptuous import All, Optional, Schema

from aiida.orm import Dict

# A subset of cpptraj command line options
cmdline_options = {
    # Required("parm"): str,  # list of prmtop files as a str
    # Required("inpcrd"): str,  # list of inpcrd files as a str
    Optional("p"): All([str]),
    Optional("i"): str,
    Optional("y"): str,
    Optional("x"): str,
    Optional("ya"): str,
    Optional("xa"): str,
    Optional("c"): str,
    Optional("d"): str,
    Optional("w"): str,
    Optional("o"): str,
    Optional("defines"): bool,
    Optional("debug"): bool,
    Optional("log"): str,
    Optional("tl"): bool,
    Optional("ms"): str,
    Optional("mr"): str,
    Optional("mask"): str,
    Optional("remask"): str,
    Optional("rng"): str,
    Optional("charge"): str,
}


class CpptrajParameters(Dict):  # pylint: disable=too-many-ancestors
    """
    Command line options for cpptraj.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)

    # pylint: disable=redefined-builtin
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``CpptrajParameters(dict{'ignore-case': True})``

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(CpptrajParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return CpptrajParameters.schema(parameters_dict)

    def cmdline_params(self, input_files):
        # pylint: disable=unused-argument
        """Synthesize command line parameters.

        :param input_files: list of inputs for cpptraj command, containing
            SinglefileData aiida datatypes used in input nodes.
        :param type input_files: list

        """
        parameters = []

        # parameters.append("cpptraj")
        # required inputs
        # parameters.extend(["-i", input_files["cpptraj_script"]])
        # parm and inpcrd are added below

        parm_dict = self.get_dict()

        # check if flags need two dashes added to front instead of one
        for key, value in parm_dict.items():
            dash = "-"
            if len(key) > 2:
                dash = "--"
            if value not in [True, False]:
                parameters.extend([dash + key, value])
            else:
                parameters.extend([dash + key])

        return [str(p) for p in parameters]

    def __str__(self):
        """String representation of node.

        Append values of dictionary to usual representation. E.g.::

            uuid: b416cbee-24e8-47a8-8c11-6d668770158b (pk: 590)
            {'ignore-case': True}

        """
        string = super().__str__()
        string += "\n" + str(self.get_dict())
        return string
