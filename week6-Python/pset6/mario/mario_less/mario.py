from cs50 import get_int

# prompt user for the height of the pyramid
while True:
    height = get_int("Height: ")

    if height in range(1, 9):
        break

# iterate through the height of the pyramid
for i in range(height):
    # print the blocks
    print(" " * (height - (i + 1)), end="")
    print("#" * (i + 1))
