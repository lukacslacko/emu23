#!/usr/bin/python3
from sys import argv

from parse import parse, find_lines

print(argv)

input_file = "input.lla" if len(argv) < 2 else argv[1]

with open(input_file, "r") as f:
  tokens = parse(f.read())
  l = find_lines(tokens)
  print("\n".join(" ".join(r) + " ;" for r in l))
