#!/usr/bin/env python
"""
Functions for parsing various gromacs input/output files and extracting
metadata into a dictionary.
"""

from biosim_extractor.metadata.populatemetadata import MetadataPopulator
from biosim_schema.utils.paths import engine_mappings_path, schema_yaml_path


def extract_amber_files(top_file, traj_file, log_file):
    """Extract metadata from topology, trajectory, and Amber log files."""

    mapping_path = engine_mappings_path()
    biosim_path = schema_yaml_path()

    populator = MetadataPopulator(
        schema_path=mapping_path,
        top_file=top_file,
        traj_file=[traj_file],
        log_file=log_file,
        engine="amber",
        store_file_metadata=True,
    )

    result = populator.populate()
    populator.validate(result, biosimschema_path=biosim_path)

    return result
