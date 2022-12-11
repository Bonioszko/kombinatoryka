def test(a):
    a += 1
    return a


a = 2
a = test(a)
print(a)
