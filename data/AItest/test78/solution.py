
def decimal_to_binary(decimal):
    binary = bin(decimal)[2:]
    return f"db{binary}db"

print(decimal_to_binary(15))   # returns "db1111db"
print(decimal_to_binary(32))   # returns "db100000db"
