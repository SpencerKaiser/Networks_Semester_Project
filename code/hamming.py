# CSE4344 - Networks
# Luke Oglesbee

__verbose = False

def encode(input):
  """Encode an input string
      input: string of 1's and 0's as data to encoded
      output: string of 1's and 0's as input data with hamming code"""
  #TODO: check for valid input...
  #Make space for parity bits
  output = [0]
  parity_bits = [1]
  index = 2
  for i in input:
    if ((index-1 & (index)) == 0): #Check for power of 2
      parity_bits.append(index)
      output.append(0)
      index += 1
    output.append(int(i))
    index += 1
  #Calculate values for parity bits and insert into output
  while parity_bits:
    if __verbose: print "".join(str(x)+" " for x in output)
    bit = parity_bits.pop(0)
    index = bit-1
    comp = 0
    output[bit-1] = calc_parity(output, bit)
  return "".join(str(x) for x in output)

def calc_parity(message, parity_bit):
  """I hope this makes life better..."""
  comp = 0
  index = parity_bit-1
  while(index < len(message)):
    for i in range(index,index+parity_bit):
      if (i >= len(message)):
        break;
      comp = comp + message[i]
    index += 2*parity_bit
  return comp%2

def decode(input):
  output = [int(x) for x in input]
  parity_errors = []
  parity_bits = []
  parity_bit = 1
  while parity_bit < len(output):
    parity_bits.append(parity_bit)
    parity_bit *= 2
  parity_check = list(parity_bits)
  parity_errors = []
  while parity_check:
    parity_bit = parity_check.pop(0)
    if (1 == calc_parity(output, parity_bit)):
      parity_errors.append(parity_bit)
  if __verbose: print parity_errors
  if __verbose: print output
  # Fix error if exists
  if parity_errors:
    bad_bit = reduce(lambda x,y: x+y, parity_errors, 0)-1
    output[bad_bit] = (output[bad_bit]+1)%2
  if __verbose: print output
  # Remove parity bits from message
  while parity_bits:
    parity_bit = parity_bits.pop()
    if __verbose: print parity_bit
    output.pop(parity_bit-1)
  if __verbose: print output
  return "".join(str(x) for x in output)
  # return "".json(str(x) for x in output)