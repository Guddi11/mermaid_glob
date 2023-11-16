#! /usr/bin/python3
"""
:author:	R Gutmann
:date:		2023-11-16

Script to glob a directory structure and display as mermaid diagram.

:note: Todo
    - formatting of diagram via args
    - allow appending to existing file
    - independent filepath for saving

"""

import os
import pathlib
import argparse


def pathcheck(pathstring):
    """Argparse type check function. Ensures given path is a directory."""
    path = pathlib.Path(pathstring)
    if not path.is_dir():
        raise ValueError("Path does not point to a directory.")
    return path


def main(args):
    """Main working function."""
    path = args.path
    filename = args.outfile + ".md"
    double = set()
    with open(path / filename, "w", encoding="utf-8") as fout:
        fout.write("```mermaid\n")
        fout.write("graph LR\n")
        for root, dirname, files in os.walk(path):
            if len(dirname) == 0 and len(files) == 0:
                continue

            parent = root.split("/")[-1]
            if parent in args.omit:
                continue

            for name in dirname + files:
                if name in args.omit:
                    continue
                if name in double:
                    fout.write(f"  {parent} --> {parent}/{name}\n")
                    continue
                double.add(name)
                fout.write(f"  {parent} --> {name}\n")

        fout.write("```")

    print(f"Written to {path /filename}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "MermaidGlob",
        """Outputs a mermaid graph of the folder structure to a given path.""",
    )

    parser.add_argument(
        "path", help="Path to folder that should be displayed.", type=pathcheck
    )
    parser.add_argument("outfile", help="Filename of output file.", default="mermaid")
    parser.add_argument(
        "--omit",
        "-o",
        action="append",
        help="List of names to be omitted in diagram.",
        default=[],
        type=str,
    )
    arguments = parser.parse_args()

    main(arguments)
