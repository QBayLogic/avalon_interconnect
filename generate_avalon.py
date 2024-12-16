#!/usr/bin/env python3
"""
Generate an Avalon interconnectbased upon a configuration file

Usage:
    generate_avalon.py [<config_file>]

Options
    -h --help     Show this screen.
    -v --version  Show version
"""


import os
import sys
import json
import fnmatch
from jinja2 import Template, Environment, FileSystemLoader

src_dir = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()

vhdl_template = os.path.join(src_dir, "templates")
config_file = os.path.join(src_dir, 'config.json')

file_loader = FileSystemLoader(vhdl_template)  # Directory where the template file is stored
env = Environment(loader=file_loader)

# Load the template from the file
template = env.get_template('avalon_interconnect.vhdl.jinja2')

core_template = env.get_template('avalon_interconnect.core.jinja2')

# constants
addr_lower_bound = 8
addr_upper_bound = 32
data_lower_bound = 8
data_upper_bound = 32
slv_lower_bound = 2
slv_upper_bound = 32


def parse_config_file(config_file):
    """ Parse config file
    """
    print("Parsing configuration file")
    with open(config_file, 'r') as file:
        config = json.load(file)

    module_name = config['module_name']
    address_width = config['address_width']
    data_width = config['data_width']
    slave_count = config['slave_count']

    assert module_name, "Module name cannot be empty"
    assert addr_lower_bound <= address_width <= addr_upper_bound, f"Error: address_width is not between {addr_lower_bound} and {addr_upper_bound}"
    assert data_lower_bound <= data_width <= data_upper_bound, f"Error: data_width is not between {data_lower_bound} and {data_upper_bound}"
    assert slv_lower_bound <= slave_count <= slv_upper_bound, f"Error: slave_count is not between {slv_lower_bound} and {slv_upper_bound}"

    return module_name, address_width, data_width, slave_count


def generate_interconnect(module_name, address_width, data_width, slave_count):
    """ Generate VHDL of interconnect
    """
    print("Generating interconnect")
    generated_vhdl = template.render(
        module_name = module_name,
        address_width = address_width,
        data_width = data_width,
        slave_count = slave_count
    )
    return generated_vhdl


def write_interconnect(module_name, generated_vhdl):
    """ Write the generated interconnect to file
    """
    output_directory = os.path.join(cwd, module_name)
    file_name = f"{module_name}.vhdl"
    output_file = os.path.join(output_directory, file_name)
    print(f"Writing interconnect to: {output_file}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    with open(output_file, "w") as f:
        f.write(generated_vhdl)

# From chatgpt
def find_vhdl_files(directory):
    vhdl_files = []
    # Traverse the directory
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.vhdl'):
            vhdl_files.append(os.path.join(root, filename))
        for filename in fnmatch.filter(files, '*.vhd'):
            vhdl_files.append(os.path.join(root, filename))
    return vhdl_files


def last_dir_and_filename(files):
    """ Strip a full path + file into a last_dir + filename
    """
    last_dir_and_files = [
        os.path.join(os.path.basename(os.path.dirname(path)), os.path.basename(path))
        for path in files
    ]

    return last_dir_and_files

def generate_core_file():
    vhdl_files = find_vhdl_files(cwd)
    print(vhdl_files)
    stripped_vhdl_files = last_dir_and_filename(vhdl_files)
    print(stripped_vhdl_files)
    print("Generating core file")
    generated_core_file = core_template.render(
        vhdl_files = stripped_vhdl_files
    )
    return generated_core_file


def write_core_file(generated_core_file):
    """ Write the generated interconnect to file
    """
    output_file = os.path.join(cwd, 'avalon_interconnect.core')
    with open(output_file, "w") as f:
        f.write(generated_core_file)




def main(config_file):
    (module_name, address_width, data_width, slave_count) = parse_config_file(config_file)
    generated_vhdl = generate_interconnect(module_name, address_width, data_width, slave_count)
    write_interconnect(module_name, generated_vhdl)
    generated_core_file = generate_core_file()
    write_core_file(generated_core_file)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage : generate_avalon.py <configfile.json>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        sys.exit(main(config_file))
    except FileNotFoundError:
        print(f"Error: The file '{config_file}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{config_file}' is not a valid JSON file.")
        sys.exit(1)


