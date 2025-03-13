#!/usr/bin/env python3
import sys
from parse import parse_xsl


if __name__=="__main__":
    
    for arg in sys.argv:
        agenda_sheet = parse_xsl(arg)

        