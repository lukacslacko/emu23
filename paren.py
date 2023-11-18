def paren(tokens: list[str]) -> int:
  if not tokens[0] in ["(","{","["]:
    return 0
  o=tokens[0]
  c={'(':')','{':'}','[':']'}[o]
  i=0
  d=0
  while i < len(tokens):
    if tokens[i]==o:
      d+=1
    if tokens[i]==c:
      d-=1
      if d==0:
        return i
    i+=1
  raise ValueError(tokens)
