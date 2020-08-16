#!/bin/env python3
import click
from org_email.convert import Converter
from org_email.generator import Generator
import sys


@click.command()
@click.option("--input", help="the input file")
@click.option("--output", help="the output file")
def main(input: str, output: str):
    doc: str = ""
    with open(input, "r") as f:
        lines = f.readlines()
        converter = Converter(lines)
        org_lines = converter.convert()
        generator = Generator(org_lines)
        doc = generator.generate()

    with open(output, "w") as f:
        f.write(doc)


if __name__ == "__main__":
    main()
    print(sys.version)
