"""This module handles reading and parsing XML files

@Author: Bradley Knorr
@Date: 1/22/2024
"""

import xml.etree.ElementTree as ET

def get_column_mappings(
    column_mapping: str,
    tag_name: str,
    key: str,
    value: str,
    default_value: str = None,
) -> dict:
    """Convert column mapping XML to dictionary of properties to map columns to

    Args:
        column_mapping (str): XML of column mappings
        tag_name (str): tag to pull values from

    Returns:
        dict: column mappings {key: column name, value: property name}
    """
    # parse XML from ColumnInfo column of database
    parsed_xml = ET.ElementTree(ET.fromstring(column_mapping))
    root = parsed_xml.getroot()

    # get all input tags
    tags = get_tag(root, tag_name)

    property_mapping = dict()

    # create dict mapping tag attributes 'id' to 'source'
    for tag in tags:
        # pull number from id attribute
        if "autoMap" not in tag.attrib or tag.attrib["autoMap"] == "0":
            property_mapping[tag.attrib[key]] = None
        elif value in tag.attrib:
            property_mapping[tag.attrib[key]] = tag.attrib[value]
        elif "autoMap" in tag.attrib:
            property_mapping[tag.attrib[key]] = default_value
        else:
            property_mapping[tag.attrib[key]] = None

    return property_mapping

def get_tag(root: ET.ElementTree, tag: str) -> list:
    """Recursively search for List of all specified tags in XML

    Args:
        root (ET.ElementTree Element): ET.ElementTree
        tag (string): tag name

    Returns:
        list: list of ET.ElementTree Elements
    """
    elements = []

    # loop through each tag on level below root
    for child in root:
        # if tag name found, add it to list
        if child.tag == tag:
            elements.append(child)
        # if tag name not found, try next level
        elif len(elements) < 1:
            elements = get_tag(child, tag)

    return elements

def get_tag_from_specific_branch(
    root: ET.ElementTree, tag: str, branch: list, is_full_branch=False
) -> list:
    """Recursively search for List of all specified tags in XML down a certain branch

    Args:
        root (ET.ElementTree Element): ET.ElementTree
        tag (string): tag name
        branch (list): list of tags to follow down
        is_full_branch (list): if the exact branch path was provided to save from
            searching every tag

    Returns:
        list: list of ET.ElementTree Elements
    """
    elements = []

    # if there was not a reason to call get_tag_from_specific_branch, just call get_tag
    if (
        branch is None
        or len(branch) == 0
        or (len(branch) == 1 and branch[-1] == tag)
    ):
        return get_tag(root, tag)

    # if last item in branch list is same as tag to search for, assume it is a duplicate
    if branch[-1] == tag:
        branch = branch[:-1]

    # loop through each tag on level below root
    for child in root:
        # if tag name found and it has gone down the required branch, add it to list
        if child.tag == tag and len(branch) == 0:
            elements.append(child)
        # if tag name not found, try next level
        elif len(elements) < 1:
            # if first branch tag was found, remove it from the list, and go through next level
            if len(branch) > 0 and branch[0] == child.tag:
                branch = branch[1:]
                elements = get_tag_from_specific_branch(
                    child, tag, branch
                )
            # if branch tag was not found, only go through next level if full branch
            #   was not provided
            elif not is_full_branch:
                elements = get_tag_from_specific_branch(
                    child, tag, branch
                )

    return elements

def get_tag_with_condition(
    root: ET.ElementTree, tag: str, attrib: str, attrib_values: set
) -> list:
    """Recursively search for List of all specified tags in XML and filter results
        by attribute value

    Args:
        root (ET.ElementTree Element): ET.ElementTree
        tag (string): tag name
        attrib (string): tag name
        attrib_values (set): set of attribute values to filter results by

    Returns:
        list: list of ET.ElementTree Elements
    """
    elements = []

    # loop through each tag on level below root
    for child in root:
        # if tag name found, add it to list
        if child.tag == tag and child.attrib[attrib] in attrib_values:
            elements.append(child)
        # if tag name not found, try next level
        elif len(elements) < 1:
            elements = get_tag(child, tag)

    return elements
