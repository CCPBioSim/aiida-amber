"""
Data types provided by plugin

Register data types via the "aiida.data" entry point in setup.json.
"""
# You can directly use or subclass aiida.orm.data.Data
# or any other data type listed under 'verdi data'
from voluptuous import Optional, Required, Schema

from aiida.orm import Dict

# A subset of pdb4amber command line options
cmdline_options = {
    Required("out", default="stdout"): str,
    Optional("y"): bool,
    Optional("nohyd"): bool,
    Optional("d"): bool,
    Optional("dry"): bool,
    Optional("s"): str,
    Optional("strip"): str,
    Optional("m"): str,
    Optional("mutate"): str,
    Optional("p"): bool,
    Optional("prot"): bool,
    Optional("a"): bool,
    Optional("amber-compatible-residues"): bool,
    Optional("constantph"): bool,
    Optional("most-populous"): bool,
    Optional("keep-altlocs"): bool,
    Optional("reduce"): bool,
    Optional("no-reduce-db"): bool,
    Optional("pdbid"): str,
    Optional("add-missing-atoms"): bool,
    Optional("model"): str,
    Optional("l"): str,
    Optional("logfile"): str,
    Optional("v"): bool,
    Optional("version"): bool,
    Optional("leap-template"): bool,
    Optional("no-conect"): str,
    Optional("noter"): str,
}


class Pdb4amberParameters(Dict):
    """
    Command line options for pdb4amber.

    This class represents a python dictionary used to
    pass command line options to the executable.
    """

    # "voluptuous" schema  to add automatic validation
    schema = Schema(cmdline_options)
    
    def __init__(self, dict=None, **kwargs):
        """
        Constructor for the data class

        Usage: ``Pdb4amberParameters(dict{'ignore-case': True})``

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict

        """
        dict = self.validate(dict)
        super().__init__(dict=dict, **kwargs)

    def validate(self, parameters_dict):
        """Validate command line options.

        Uses the voluptuous package for validation. Find out about allowed keys using::

            print(Pdb4amberParameters).schema.schema

        :param parameters_dict: dictionary with commandline parameters
        :param type parameters_dict: dict
        :returns: validated dictionary
        """
        return Pdb4amberParameters.schema(parameters_dict)

    def cmdline_params(self, input_files):
        """Synthesize command line parameters.

        :param input_files: list of inputs for pdb4amber command, containing
            SinglefileData aiida datatypes used in input nodes.
        :param type input_files: list

        """
        parameters = []

        # parameters.append("pdb4amber")
        # required inputs
        parameters.extend(["-i", input_files["input_file"]])
        # no optional inputs


        parm_dict = self.get_dict()

        for key, value in parm_dict.items():
            dash = "-"
            if len(key) > 1:
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
