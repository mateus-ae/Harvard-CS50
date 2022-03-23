from cs50 import get_float

# prompt user for the change owed. it can't be 0 or negative
while True:
    change = get_float("Change owed: $")
    
    if change > 0:
        break

# Create a list to store the amount of each type of coin
coins = []

# Calculate the amount for each coin
for i in [0.25, 0.10, 0.05, 0.01]:
    if change < 0.05:
        cur_coins = change / i
    else:
        cur_coins = change // i

    # insert the calculated amount into the coins list
    coins.append(int(cur_coins))

    # calculate the remaining change
    change = change - (i * int(cur_coins))
    change = float(f"{change:.2f}")

# Sum the coins and print this value
sum_coins = sum(coins)

print(sum_coins)
