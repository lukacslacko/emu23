def includes(lines, included=[]):
  result = []
  loadedlines = []
  for line in lines:
    if line.startswith("include "):
      fnames = line.split(" ")[1:]
      for fname in fnames:
        if fname in included:
          continue
        included.append(fname)
        with open(fname, "r") as f:
          loadedlines += includes(list(f.read().split("\n")), included)
      continue
    loadedlines.append(line)
  return loadedlines

def preproc(lines, included=[]):
  result = []
  macros = dict()
  loadedlines = includes(lines)
  #print("Loaded ", loadedlines)
  for line in loadedlines:
    if line.startswith("$") and "=" in line:
      macros[line.split("=")[0]] = line.split("=")[1].split(" ")
      continue
    if line.startswith("$"):
      parts = line.split(" ")
      for exp in macros[parts[0]]:
        if "%" in exp:
          exp = exp[:-2] + " " + parts[int(exp[-1])]
        result.append(exp)
        continue
    result.append(line)
  return result
