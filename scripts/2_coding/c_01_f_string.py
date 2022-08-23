w_bird = 5
w_fruit = 1
fruit = "coconut"

# String addition: Clunky, manual declaration of variables to strings:
str_add = (
    "A "
    + str(w_bird)
    + " ounce bird could not carry a "
    + str(w_fruit)
    + " pound "
    + fruit
    + "."
)
print(str_add)

# String formatting: Automatic casting to str, but inputs at the end:
str_format = "A {} ounce bird could not carry a {} pound {}.".format(
    w_bird, w_fruit, fruit
)
print(str_format)

# f-string: Awesomeness.
f_str = f"A {w_bird} ounce bird could not carry a {w_fruit} pound {fruit}."
print(f_str)
