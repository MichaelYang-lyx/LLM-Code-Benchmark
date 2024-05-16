
def tri(n):
    # Initialize the sequence
    tri_sequence = [0, 3]

    for i in range(2, n+1):
        if i % 2 == 0:
            tri_sequence.append(1 + i / 2)
        else:
            tri_sequence.append(tri_sequence[i - 1] + tri_sequence[i - 2] + tri_sequence[i + 1])
            # since we calculate tri_sequence[i + 1] using the formula in the odd case,
            # ensure that the list has one extra entry at the end to hold this value
            if i == n:  # we're at the last number
                break  # don't add an extra entry beyond the range we're interested in
            tri_sequence.append(0)

    return tri_sequence
