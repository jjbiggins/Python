# Author: João Gustavo A. Amorim & Gabriel Kunz
# Author email: joaogustavoamorim@gmail.com and gabriel-kunz@uergs.edu.br
# Coding date:  apr 2019
# Black: True

"""
    * This code implement the Hamming code:
        https://en.wikipedia.org/wiki/Hamming_code - In telecommunication,
    Hamming codes are a family of linear error-correcting codes. Hamming
    codes can detect up to two-bit errors or correct one-bit errors
    without detection of uncorrected errors. By contrast, the simple
    parity code cannot correct errors, and can detect only an odd number
    of bits in error. Hamming codes are perfect codes, that is, they
    achieve the highest possible rate for codes with their block length
    and minimum distance of three.

    * the implemented code consists of:
        * a function responsible for encoding the message (emitterConverter)
            * return the encoded message
        * a function responsible for decoding the message (receptorConverter)
            * return the decoded message and a ack of data integrity

    * how to use:
            to be used you must declare how many parity bits (sizePari)
        you want to include in the message.
            it is desired (for test purposes) to select a bit to be set
        as an error. This serves to check whether the code is working correctly.
            Lastly, the variable of the message/word that must be desired to be
        encoded (text).

    * how this work:
            declaration of variables (sizePari, be, text)

            converts the message/word (text) to binary using the
        text_to_bits function
            encodes the message using the rules of hamming encoding
            decodes the message using the rules of hamming encoding
            print the original message, the encoded message and the
        decoded message

            forces an error in the coded text variable
            decodes the message that was forced the error
            print the original message, the encoded message, the bit changed
        message and the decoded message
"""

# Imports
import numpy as np


# Functions of binary conversion--------------------------------------
def text_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    """
    >>> text_to_bits("msg")
    '011011010111001101100111'
    """
    bits = bin(int.from_bytes(text.encode(encoding, errors), "big"))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding="utf-8", errors="surrogatepass"):
    """
    >>> text_from_bits('011011010111001101100111')
    'msg'
    """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, "big").decode(encoding, errors) or "\0"


# Functions of hamming code-------------------------------------------
def emitterConverter(sizePar, data):
    """
    :param sizePar: how many parity bits the message must have
    :param data:  information bits
    :return: message to be transmitted by unreliable medium
            - bits of information merged with parity bits

    >>> emitterConverter(4, "101010111111")
    ['1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1']
    """
    if sizePar + len(data) <= 2**sizePar - (len(data) - 1):
        print("ERROR - size of parity don't match with size of data")
        exit(0)

    dataOut = []
    parity = []
    binPos = [bin(x)[2:] for x in range(1, sizePar + len(data) + 1)]

    # sorted information data for the size of the output data
    dataOrd = []
    # data position template + parity
    dataOutGab = []
    # parity bit counter
    qtdBP = 0
    # counter position of data bits
    contData = 0

    for x in range(1, sizePar + len(data) + 1):
        # Performs a template of bit positions - who should be given,
        # and who should be parity
        if qtdBP < sizePar:
            if (np.log(x) / np.log(2)).is_integer():
                dataOutGab.append("P")
                qtdBP = qtdBP + 1
            else:
                dataOutGab.append("D")
        else:
            dataOutGab.append("D")

        # Sorts the data to the new output size
        if dataOutGab[-1] == "D":
            dataOrd.append(data[contData])
            contData += 1
        else:
            dataOrd.append(None)

    for bp in range(1, sizePar + 1):
        # Bit counter one for a given parity
        contBO = 0
        for contLoop, x in enumerate(dataOrd):
            if x is not None:
                try:
                    aux = (binPos[contLoop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    contBO += 1
        parity.append(contBO % 2)

    # Mount the message
    ContBP = 0  # parity bit counter
    for x in range(sizePar + len(data)):
        if dataOrd[x] is None:
            dataOut.append(str(parity[ContBP]))
            ContBP += 1
        else:
            dataOut.append(dataOrd[x])

    return dataOut


def receptorConverter(sizePar, data):
    """
    >>> receptorConverter(4, "1111010010111111")
    (['1', '0', '1', '0', '1', '0', '1', '1', '1', '1', '1', '1'], True)
    """
    # data position template + parity
    dataOutGab = []
    # Parity bit counter
    qtdBP = 0
    # Counter p data bit reading
    contData = 0
    # list of parity received
    parityReceived = []
    dataOutput = []

    for x in range(1, len(data) + 1):
        # Performs a template of bit positions - who should be given,
        #  and who should be parity
        if qtdBP < sizePar and (np.log(x) / np.log(2)).is_integer():
            dataOutGab.append("P")
            qtdBP = qtdBP + 1
        else:
            dataOutGab.append("D")

        # Sorts the data to the new output size
        if dataOutGab[-1] == "D":
            dataOutput.append(data[contData])
        else:
            parityReceived.append(data[contData])
        contData += 1

    # -----------calculates the parity with the data
    dataOut = []
    parity = []
    binPos = [bin(x)[2:] for x in range(1, sizePar + len(dataOutput) + 1)]

    #  sorted information data for the size of the output data
    dataOrd = []
    # Data position feedback + parity
    dataOutGab = []
    # Parity bit counter
    qtdBP = 0
    # Counter p data bit reading
    contData = 0

    for x in range(1, sizePar + len(dataOutput) + 1):
        # Performs a template position of bits - who should be given,
        # and who should be parity
        if qtdBP < sizePar and (np.log(x) / np.log(2)).is_integer():
            dataOutGab.append("P")
            qtdBP = qtdBP + 1
        else:
            dataOutGab.append("D")

        # Sorts the data to the new output size
        if dataOutGab[-1] == "D":
            dataOrd.append(dataOutput[contData])
            contData += 1
        else:
            dataOrd.append(None)

    for bp in range(1, sizePar + 1):
        # Bit counter one for a certain parity
        contBO = 0
        for contLoop, x in enumerate(dataOrd):
            if x is not None:
                try:
                    aux = (binPos[contLoop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    contBO += 1
        parity.append(str(contBO % 2))

    # Mount the message
    ContBP = 0  # Parity bit counter
    for x in range(sizePar + len(dataOutput)):
        if dataOrd[x] is None:
            dataOut.append(str(parity[ContBP]))
            ContBP += 1
        else:
            dataOut.append(dataOrd[x])

    ack = parityReceived == parity
    return dataOutput, ack


# ---------------------------------------------------------------------
"""
# Example how to use

# number of parity bits
sizePari = 4

# location of the bit that will be forced an error
be = 2

# Message/word to be encoded and decoded with hamming
# text = input("Enter the word to be read: ")
text = "Message01"

# Convert the message to binary
binaryText = text_to_bits(text)

# Prints the binary of the string
print("Text input in binary is '" + binaryText + "'")

# total transmitted bits
totalBits = len(binaryText) + sizePari
print("Size of data is " + str(totalBits))

print("\n --Message exchange--")
print("Data to send ------------> " + binaryText)
dataOut = emitterConverter(sizePari, binaryText)
print("Data converted ----------> " + "".join(dataOut))
dataReceiv, ack = receptorConverter(sizePari, dataOut)
print(
    "Data receive ------------> "
    + "".join(dataReceiv)
    + "\t\t -- Data integrity: "
    + str(ack)
)


print("\n --Force error--")
print("Data to send ------------> " + binaryText)
dataOut = emitterConverter(sizePari, binaryText)
print("Data converted ----------> " + "".join(dataOut))

# forces error
dataOut[-be] = "1" * (dataOut[-be] == "0") + "0" * (dataOut[-be] == "1")
print("Data after transmission -> " + "".join(dataOut))
dataReceiv, ack = receptorConverter(sizePari, dataOut)
print(
    "Data receive ------------> "
    + "".join(dataReceiv)
    + "\t\t -- Data integrity: "
    + str(ack)
)
"""
