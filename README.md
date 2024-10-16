# Avalon generator

The avalon generator is a tool to create an avalon interconnect in an easy way.
One can describe, in a configuration file, an avalon interconnect and then generate the VHDL and fusesoc core file.

## Features

- Human readable JSON input file
- VHDL code geenration
- Fusesoc core file generation

## Usage

```sh
./generate_avalon <config_file>
```

## Configuration file

The configuration file is written in JSON.

Hereby an example with explanation.

```JSON
{
module_name = "avalon_interconnect_1m14s",
address_width = 32,
data_width = 32,
slave_count = 5
}
```

The above example will generate an interconnect with a single avalon master input and 5 slaves.
Some notes:

- The module name cannot be left empty
- The address range is bounded between 8 and 32-bits.
- The data range is bounded between 8 and 32-bits.
- The slave_count is bounded between 2 and 16.


## Verification

ToDo

