# ввод значений
n = int(input("Number: "))
b = int(input("Notation (2-9): "))

# проверка значений
if b >= 2 and b <= 9:
    # проверка, отрицательное ли число
    sign = ""
    if n < 0:
        sign = "-"
    n = abs(n)

    # перевод в нужную систему счисления
    if n == 0:
        res = "0"
    else:
        res = ""
        while n > 0:
            res = str(n % b) + res
            n //= b
    print("Result:", sign + res)
else:
    print("Error")