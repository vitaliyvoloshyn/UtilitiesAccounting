from datetime import date
import decimal

a = [1, 2, 4, 7, 11, 16, 23]


def d(b: list):
    for i in range(1, len(b)):
        diff = b[i] - b[i - 1]
        yield diff


if __name__ == '__main__':
    for x in d(a):
        print(x)
