from cs50 import get_int

# Prompt user for the height of the pyramid
while True:
    height = get_int("Height: ")

    if height in range(1, 9):
        break

# Print the pyramid
for i in range(height):
    print(" " * (height - (i + 1)), end="")
    print("#" * (i + 1), end="")
    print("  ", end="")
    print("#" * (i + 1))
