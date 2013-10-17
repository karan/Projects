# Find Cost of Tile to Cover W x H Floor - Calculate
# the total cost of tile it would take to cover a floor
# plan of width and height, using a cost entered by the user.

# Use input as the input can be integer and float
cost = input("What's the cost per sq. feet? ")
width = input("What's the width of the floor? ")
height = input("What's the height of the floor? ")

print "The total cost is $%.2f for %.2f square feet" \
      % (width * height * cost, width * height)
