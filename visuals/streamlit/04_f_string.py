w_bird = 5
w_fruit = 1
type_fruit = 'coconut'

# String addition, clunky, manual declaration of variables to strings:
str_add = "A " + str(w_bird) + " ounce bird could not carry a " + str(w_fruit) + " pound " + type_fruit + "."
print(str_add)

# String formatting, automatic typing to str, but inputs at the end:
str_format = "A {} ounce bird could not carry a {} pound {}.".format(w_bird, w_fruit, type_fruit)
print(str_format)

# f-string, awesomeness.
f_str = f"A {w_bird} ounce bird could not carry a {w_fruit} pound {type_fruit}."
print(f_str)