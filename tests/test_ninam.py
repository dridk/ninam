import ninam.__main__ as nim 





def test_payload():


    payload = "hello"

    for bit in (1,2,4):
        spaces = nim.payload_to_space(payload.encode(),bit)
        assert nim.space_to_payload(spaces,bit) == payload.encode()
    



def test_encode_decode():

    message = """
    Fifteen seconds later he was out of the house and lying in front of
    a big yellow bulldozer that was advancing up his garden path.
    Mr L Prosser was, as they say, only human. In other words he
    was a carbon-based life form descended from an ape. More
    specifically he was forty, fat and shabby and worked for the local
    council. Curiously enough, though he didn't know it, he was also
    a direct male-line descendant of Genghis Khan, though
    intervening generations and racial mixing had so juggled his
    genes that he had no discernible Mongoloid characteristics, and
    the only vestiges left in Mr L Prosser of his mighty ancestry were
    a pronounced stoutness about the tum and a predilection for
    little fur hats.
    """

    payload = "I love you" 


    stegano_message = nim.encode(message,payload)
    assert payload == nim.decode(stegano_message)


def test_extra_large():

    # message with 8 spaces 
    message ="a short very and nice message with 8 spaces"
    
    # This payload required 16 bits 
    payload = "ah"

    encoded = nim.encode(message, payload, bitsize=1)
    end = encoded[-8:]

    # Last 8 caracters must be extra spaces
    for letter in end:
        assert ord(letter) in nim.WHITESPACE
    
