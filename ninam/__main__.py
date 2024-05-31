import argparse
import sys
import logging
import math

WHITESPACE = [32,8198,8201,8200,160,8192,8193,8194,8195,8196,8197,8202,8239,8287,8199,9]


def assert_wrong_bitsize(bitsize = 2):

    def is_power_of_two(n):
        return (n != 0) and (n & (n-1) == 0)

    if not is_power_of_two(bitsize):
        raise Exception(f"bitsize must be a power of 2")

    if 2**bitsize > len(WHITESPACE):
        raise Exception(f"Not enough whitespace symbols to use {bitsize} per whitespace ")


def max_payload_size(text:str, bitsize=2):
    """
    Check the maximum size of the payload
    """

    return math.floor(text.count(' ') / ( 8 / bitsize))


def payload_to_space(payload:bytes, bitsize=2)->list[bytes]:
    """
    Transform a payload into white spaces     

    Examples : 

        with 1 bits per space:
     
        payload = 10000011  10000000   
        spaces  = ABBBBBAA  ABBBBBBB 

        with 2 bits per space:
            payload = 10 00 00 11  10 00 00 00   

        spaces  = A  B  A  C   A  B  B  B 

        with 4 bits per space:
    
        payload = 1000 0011  1000 0000   
        spaces  = A    B     A    C
    
   
    """
    assert_wrong_bitsize(bitsize)

    spaces = []
    symbols_count = 2**bitsize 
    symbols = WHITESPACE[:symbols_count]
    max = 8//bitsize
    for byte in payload:
        # write one byte
        for i in range(0, max):
            mask = 2**bitsize-1
            shift = (max-i-1) * bitsize
            mask = mask << shift
            read = (byte & mask) >> shift
            symbol = symbols[read]
            spaces.append(symbol)

    return spaces
        


def space_to_payload(spaces:list[bytes], bitsize = 2) -> bytes:
    """
    Transform a list of white spaces into a payload

    Exemples : 
    
    With bitsize = 1 
    
        spaces  = ABABABAB
        payload = 10101010

    With bitsize = 2 

        spaces  = A  B  C  D
        payload = 01 00 11 10

    With bitsize = 4

        spaces  =  A     B 
        payload =  0111  1110
        
    """
    
    assert_wrong_bitsize(bitsize)
    
    payload = bytearray()
    max = 8//bitsize
    for i in range(0, len(spaces), max):
        # One chunk = 1 byte
        chunk = spaces[i: i+max]
        # Start reading one byte 
        byte = 0x0
        for i, space in enumerate(chunk):
            index = WHITESPACE.index(space)            
            shift = (max-1-i) * bitsize
            byte = byte | (index << shift)

        if byte != 0x0:
            payload.append(byte)
        

    return bytes(payload)

def encode(text:str, payload:str, bitsize=2):
    """ 
    Encode a payload into a text
    """
    payload = payload.encode()
    max_size = max_payload_size(text, bitsize)


    if len(payload) > max_size:
        logging.warning(f"Your payload ({len(payload)} bytes) exeed the amount of white space available in the text ({max_size} bytes). Spaces will be added at the end of the file")
        diff = (len(payload) - max_size) 
        space_required = math.floor((8/bitsize) * diff)
        text += ' ' * space_required
        
    
    spaces = payload_to_space(payload, bitsize)
    index = 0
    encoded = ""
    for letter in text:
        if letter == " " and index < len(spaces):
            encoded += chr(spaces[index])
            index+=1 
        else:
            encoded += letter

    return encoded


def decode(text:str, bitsize=2):
    """
    Extract payload from text 
    """
    spaces = []
    for letter in text:
        if ord(letter) in WHITESPACE:
            spaces.append(ord(letter))

    payload = "".join([f"{chr(i)}" for i in space_to_payload(spaces, bitsize)])
    return payload


def main_cli():

    description= """
    Ninam is a steganography tool to encode or decode a payload in a text file.
    It works by replacing the space character with other unicode space characters.

    You can select how many bit you want to encode by specify the bitsize arguments.
    By default, it uses 2 bits per white space.

    Usage examples:    
        
        ninam encode -i input.txt -p iloveyou > output.txt
        ninam decode -i output.txt 
    """

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", help="Choose command")

    encode_parser = subparsers.add_parser("encode", help="Encode file with payload")
    encode_parser.add_argument("-i", "--input",type=argparse.FileType("r"), default=sys.stdin)
    encode_parser.add_argument("-p", "--payload", required=True, help="Payload to encode")
    encode_parser.add_argument("-b", "--bitsize", required=False, choices=[1,2,4], type=int, default=2, help="How many bit per white space")

    decode_parser= subparsers.add_parser("decode", help="Extract payload from text")
    decode_parser.add_argument("-i", "--input",type=argparse.FileType("r"), default=sys.stdin)
    decode_parser.add_argument("-b", "--bitsize", required=False, choices=[1,2,4], type=int, default=2, help="How many bit per white space")
    args = parser.parse_args()

    if args.command == "encode":
        text = args.input.read()
        payload = args.payload 
        print(encode(text, payload, args.bitsize))        

    if args.command == "decode":
        text = args.input.read()
        payload = decode(text, args.bitsize)
        print(payload)            


if __name__ == "__main__":
    main_cli()

