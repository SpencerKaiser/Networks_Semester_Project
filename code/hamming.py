# CSE4344 - Networks
# Luke Oglesbee

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
  #Calculate values for parity bits
  while parity_bits:
    bit = parity_bits.pop(0)
    index = bit-1
    comp = 0
    while (index < len(output)):
      for i in range(index,index+bit):
        if i < len(output):
          # print "%s %s %s" % (i, index, output[i])
          comp = (comp + output[i])%2
        else:
          break
      index += 2*bit
    output[bit-1] = comp
    # print comp
  return "".join(str(x) for x in output)

def decode(input):
  #empty for now
  output = ""

num = "1001010010101001010100101010101110101111111000001010101001010101010"
num = "10011010"
print num
print encode(num)