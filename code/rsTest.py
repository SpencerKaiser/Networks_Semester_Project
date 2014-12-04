import rs
import noise
import converter

reedSolomon = rs.RSCoder(128, 112)
c = converter.Converter()
bitstream = "0100110010011101100000010100100110001110101011111011100111110010010010001011110011010110001000101001111000010101"
rsLength = 8

codedstream = reedSolomon.encode(bitstream)
print "Encoded: " + str(codedstream) + "\r"
afternoise = noise.gaussian_RS(codedstream, 0.03)
print "Noise: " + str(afternoise) + "\r"
decodedstream = reedSolomon.decode(afternoise)
print "Decoded: " + str(decodedstream) + "\r"
# outputString = ""
# for i in range(0, 28):
#     outputString += chr(decodedstream[i])
#
# print "String: " + outputString