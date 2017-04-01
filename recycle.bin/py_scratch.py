table = [
    36, 50, 97, 36, 48, 54, 36, 81, 81, 80, 111, 77, 77, 119, 53,
    85, 109, 84, 54, 72, 75, 75, 82, 115, 122, 75, 104, 100, 117, 73,
    57, 103, 68, 56, 75, 48, 79, 84, 70, 113, 115, 101, 48, 102, 107,
    109, 98, 53, 111, 98, 79, 75, 47, 99, 116, 81, 50, 99, 55, 101
]

ascii_dict = dict()
ascii_in_number = range(0, 256)
for i in ascii_in_number:
    ascii_dict[str(i)] = chr(i)

for items in table:
    print(ascii_dict['{}'.format(items)], end='')
