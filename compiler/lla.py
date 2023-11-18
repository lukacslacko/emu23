#!/usr/bin/python3
from sys import argv

import backend.default
from compiler.parse import parse, find_lines
from compiler.compile import compile

print(argv)

input_file = "input.lla" if len(argv) < 2 else argv[1]
backend_name = "default"
if len(argv) >= 3:
  backend_name = argv[2]
backend = None
if backend_name == "default":
  backend = backend.default.DefaultBackend()

if backend is None:
  raise ValueError(f"Bad backend {backend_name}")

with open(input_file, "r") as f:
  tokens = parse(f.read())
  l = find_lines(tokens)
  print("\n".join(" ".join(r) + " ;" for r in l))
