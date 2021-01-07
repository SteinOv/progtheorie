from decimal import Decimal

grid_x_length = 1
grid_y_length = 1
number_of_layers = 2

x = grid_x_length + 1
y = grid_y_length + 1
z = number_of_layers

# Number of points per type
corners = 8 - 2
edge_bar = (x - 2 + y - 2 + z - 2) * 4
outer_2D_inner = 2 * (x - 2) * (y - 2) + 2 * (x - 2) * (z - 2) + 2 * (y - 2) * (z - 2)
inner_3D = (x - 2) * (y - 2) * (z - 2)

# Number of combinations start corner
start = 3

# Total amount of posibilities
possibilities = 2 ** corners * 3 ** edge_bar * 4 ** outer_2D_inner * 5 ** inner_3D * start



print(inner_3D + outer_2D_inner + edge_bar + corners)
poss_up = 5 ** 2448
poss_low = 2 ** 2448

print("{:.2E}".format(Decimal(possibilities)))
print("{:.2E}".format(Decimal(poss_up)))
print("{:.2E}".format(Decimal(poss_low)))

