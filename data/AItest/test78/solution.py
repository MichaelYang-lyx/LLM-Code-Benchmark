
def decimal_to_binary(decimal):
    # Convert integer to binary and remove the prefix '0b'
    binary_str = bin(decimal)[2:]
    # Add 'db' at the beginning and end of the string
    return "db" + binary_str + "db"
