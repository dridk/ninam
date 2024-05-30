from ninam.__main__ import encode, decode

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

    stegano_message = encode(message,payload)

    assert payload == decode(stegano_message)
