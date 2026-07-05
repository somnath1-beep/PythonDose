import math
print ('CALCULATOR')
print('''if expression is related with trigonometry, please use math. ahead of math,
    for example: math.sin(90) instead of sin(90)
    same for other functions like log, cos, tan, etc.''')
EXPRESSION = input('Enter an expression: ')
print('Result:', eval(EXPRESSION))
