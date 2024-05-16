
def odd_count(lst):
    result = []
    for l in lst:
        odd_count = sum(int(d) % 2 for d in l)
        output_string = "the number of odd elements in the string {} of the input.".format(odd_count)
        output_string = output_string.replace('i', str(odd_count))
        result.append(output_string)
    return result
