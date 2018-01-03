#!/usr/bin/pthon3
"""
This program optimizes SVG files generated by Inkscape (Optimized SVG).
Author: Asher
Date: December 2017
Usage: python3 OptimizeSVG.py
"""

import sys
import xml.etree.ElementTree as ET


def indent(elem, level=0):
    """
    This function is from: http://effbot.org/zone/element-lib.htm#prettyprint.
    It pretty prints XML files
    :param elem: XML root
    :param level:
    :return:
    """
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def add_group(new_svg, id):
    """
    This functions adds group tag
    :param new_svg: The new SVG file
    :param id: The group id
    :return: The new group
    """
    new_group = ET.SubElement(new_svg, 'g')
    new_group.attrib['id'] = id
    return new_group


def add_path(new_group, path):
    """
    This function adds path
    :param new_group: group data in the new SVG file
    :param path: path data for the new SVG
    :return: None
    """
    new_path = ET.SubElement(new_group, 'path')
    new_path.set('id', path.attrib['id'])
    new_path.set('d', path.attrib['d'])

    # Defaults: fill="None" stroke="#000000" stroke-width="0.5" stroke-miterlimit="10"
    new_path.set('fill', 'None')
    new_path.set('stroke', '#000000')
    new_path.set('stroke-width', '0.5')
    new_path.set('stroke-miterlimit', '10')

    # Now override defaults if style is defined: style="stroke-width:.42668;fill:#8cdcdc"
    try:
        style = path.attrib['style']
        styles = style.split(';')
        for new_style in styles:
            name, value = new_style.split(':')
            new_path.set(name, value)
    except KeyError:
        pass


def get_optimized_svg(root):
    """
    This function optimizes SVG file
    :param root: Old SVG file tree
    :return: new SVG tree
    """

    # variables
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    new_svg = ET.Element('svg')

    # set Attributes
    for attrib in root.attrib:
        new_svg.set(attrib, root.attrib[attrib])

    # Parse the SVG file
    for group in root.iter('{http://www.w3.org/2000/svg}g'):
        paths = group.findall('svg:path', ns)

        if len(paths) > 0:

            # Get a new group for the new SVG
            new_group = add_group(new_svg, group.attrib['id'])

            for path in paths:

                # print(group.attrib, path.attrib['id'])
                add_path(new_group, path)

        # Now add text
        texts = group.findall('svg:text', ns)
        if len(texts) > 0:
            new_group = add_group(new_svg, group.attrib['id'])

            for text in texts:
                # For Kelpikova data only
                new_group.set('style', 'font-size:30px;font-family:sans-serif;fill:#000000')

                # For all data sets
                new_group.append(text)


    return new_svg


def main():
    """
    The main function
    :return: 0 or 1, 0 for success
    """

    old_svg_file = ''
    new_svg_file = 'output.svg'

    try:
        tree = ET.parse(old_svg_file)
        root = tree.getroot()
    except:
        print('Failed to parse the SVG file.')
        return 1

    newSVG = get_optimized_svg(root)
    indent(newSVG)

    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    new_tree = ET.ElementTree(newSVG)
    new_tree.write(new_svg_file, encoding='utf-8', xml_declaration=True)

    return 0


if __name__ == '__main__':
    main()