import argparse
import sys

WHITESPACE = [32,8198,8201,8200]


def payload_to_space(payload:bytes)->list:
    """
    Transform a payload as a list of white space         
    """
    for byte in payload:

        b1 = (byte & 0b11000000) >> 6
        b2 = (byte & 0b00110000) >> 4
        b3 = (byte & 0b00001100) >> 2
        b4 = (byte & 0b00000011)

        for b in (b1,b2,b3,b4):
            code = WHITESPACE[b]
            yield chr(code)
        

def space_to_payload(spaces:list) -> bytes:
    """
    Transform a list of whitespace into bytes
    """
    spaces = [ord(s) for s in spaces]

    for i in range(0, len(spaces) - 4, 4):
        letter = 0b00000000
        p1 = WHITESPACE.index(spaces[i])
        p2 = WHITESPACE.index(spaces[i+1])
        p3 = WHITESPACE.index(spaces[i+2])
        p4 = WHITESPACE.index(spaces[i+3])
            
        letter = letter|(p1 << 6)
        letter = letter|(p2 << 4)
        letter = letter|(p3 << 2)
        letter = letter|p4 
        yield letter


def encode(text:str, payload:str):
    """ 
    Encode a payload into a text
    """
    payload = payload.encode()

    spaces = list(payload_to_space(payload))
    index = 0
    encoded = ""
    for letter in text:
        if letter == " " and index < len(spaces):
            encoded += spaces[index]
            index+=1 
        else:
            encoded += letter

    return encoded


def decode(text:str):
    """
    Extract payload from text 
    """
    spaces = []
    for letter in text:
        if ord(letter) in WHITESPACE:
            spaces.append(letter)

    payload = "".join([f"{chr(i)}" for i in space_to_payload(spaces)])

    return payload


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Encode or decode files with payload")
    subparsers = parser.add_subparsers(dest="command", help="Choose command")

    encode_parser = subparsers.add_parser("encode", help="Encode file with payload")
    encode_parser.add_argument("-i", "--input",type=argparse.FileType("r"), default=sys.stdin)
    encode_parser.add_argument("-p", "--payload", required=True, help="Payload to encode")

    decode_parser= subparsers.add_parser("decode", help="Extract payload from text")
    decode_parser.add_argument("-i", "--input",type=argparse.FileType("r"), default=sys.stdin)
    args = parser.parse_args()

    if args.command == "encode":
        text = args.input.read()
        payload = args.payload 
        print(encode(text, payload))        

    if args.command == "decode":
        text = args.input.read()
        payload = decode(text)
        print(payload)            
    # message = """
    # Hello Mrs Dupont,
    # I hope you're well. I'm writing to ask if it would be possible for me to work 
    # from home tomorrow. I'm having some transport problems at the moment, and I'm worried 
    # that this might affect my punctuality at the office. 
    # What's more, I have all the equipment I need at home to complete my tasks efficiently.
    # I can assure you that I will remain contactable throughout the day and will meet
    # all deadlines and scheduled meetings. If you have any particular 
    # preferences or requirements for my work tomorrow, please let me know and I will organise accordingly.    
    # """
    # payload = "ilove you"

    # encoded = encode(message, payload)


