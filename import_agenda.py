#!/usr/bin/env python3
import sys
from parse import parse_xsl

# def import_agenda():


if __name__=="__main__":
    # processing multiple files
    for arg in sys.argv:
        agenda_sheet = parse_xsl(arg)

        