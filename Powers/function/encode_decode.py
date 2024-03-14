import base64


async def encoder(string, to_do: str = "encode"):
    """
    For encoding and decoding the strings

    string: String you want to encode or decode
    to_do: `encode` if you want to encode the string. `decode` if you want to decode the string.
    """
    if to_do.lower() == "encode":
        encodee = str(string).encode("ascii")
        base64_ = base64.b64encode(encodee)
        B64 = base64_.decode("ascii")

    elif to_do.lower() == "decode":
        decodee = str(string).encode("ascii")
        base64_ = base64.b64decode(decodee)
        B64 = base64_.decode("ascii")

    else:
        B64 = None

    return B64
