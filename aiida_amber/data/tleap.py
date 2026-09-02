"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""

# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from aiida.orm import Dict
from voluptuous import Optional, Schema

# A subset of tleap's command line options
cmdline_options = {
    # Required("o", default="mdout"): str,
    Optional("r"): str,
}


class TleapParameters(Dict):  # pylint: disable=too-many-ancestors
    """
    Command line options for tleap.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)

    # pylint: disable=redefined-builtin
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``TleapParameters(dict{'ignore-case': True})``

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(TleapParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return TleapParameters.schema(parameters_dict)

    def cmdline_params(self, input_files):
        """Synthesize command line parameters.

        :param input_files: list of inputs for tleap command, containing
            SinglefileData aiida datatypes used in input nodes.
        :param type input_files: list

        """
        parameters = []

        # parameters.append("tleap")
        # required inputs
        parameters.extend(["-f", input_files["tleapscript"]])
        # optional inputs
        if "dirs" in input_files:
            for dir in input_files["dirs"]:
                parameters.extend(["-I", input_files["dirs"][dir]])

        parm_dict = self.get_dict()

        for key, value in parm_dict.items():
            parameters.extend(["-" + key, value])

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
