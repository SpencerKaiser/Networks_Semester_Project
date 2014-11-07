import random

codes = []

CRCpolynomial = 11000000000000101

def generatePackets():
    print("Function - generateEPC()")
    print("\r")

    file = open("../data/EPCcodes.txt", "w")
    for i in range(0, 1000):
        EPCcode = "";
        for j in range(0, 112):
            bit = random.randint(0, 1)
            EPCcode += str(bit)
        file.write(EPCcode + "\n")
        codes.append(EPCcode)

    file.close()

def readPackets():
    print("Function - readEPC()")
    print("\r")

    for code in codes:
        print(code)



def main():
    generatePackets()
    readPackets();

main()