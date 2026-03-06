import sympy as sp


pi = sp.pi
e = sp.E
j = sp.I

k_B = 1.380649e-23  # Boltzmann constant (J/K)
q_e = 1.602176634e-19  # elementary charge (C)


prefixes = [
    (-12, " p"),  # pico
    (-9, " n"),  # nano
    (-6, " u"),  # micro
    (-3, " m"),  # milli
    (0, ""),  # no prefix
    (3, " k"),  # kilo
    (6, " M"),  # mega
    (9, " G"),  # giga
    (12, " T"),  # tera
]


def engFormat(value, precision=2):
    if value == 0:
        return "0"
    exponent = int(sp.floor(sp.log(abs(value), 10)))
    if exponent >= -12 and exponent <= 12:
        exponent = (exponent // 3) * 3
        prefix = dict(prefixes)[exponent]
    else:
        prefix = f" x 10^{exponent}"
    significand = value / (10**exponent)
    return f"{significand:.{precision}f}{prefix}"


def engFormatComplex(value, precision=2, polar=False):
    if sp.im(value) == 0:
        return engFormat(sp.re(value), precision)
    else:
        if polar:
            magnitude = engFormat(sp.Abs(value), precision)
            angle = f"{sp.arg(value) * (180 / pi):.{precision}f}"
            return f"{magnitude} < {angle}"
        else:
            realPart = engFormat(sp.re(value), precision)
            imagPart = engFormat(abs(sp.im(value)), precision)
            sign = "+" if sp.im(value) >= 0 else "-"
            return f"{realPart} {sign} j {imagPart}"


def printNumber(number, precision=2, polar=False):
    print(engFormatComplex(number, precision, polar))
    print()


def printMatrix(matrix, precision=2, polar=False):
    # Determine column widths
    colWidths = [0] * matrix.cols
    for j in range(matrix.cols):
        for i in range(matrix.rows):
            valueStr = engFormatComplex(matrix[i, j], precision, polar)
            colWidths[j] = max(colWidths[j], len(valueStr))
    # Print matrix rows
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            valueStr = engFormatComplex(matrix[i, j], precision, polar)
            while len(valueStr) < colWidths[j]:
                valueStr = valueStr + " "
            if j < matrix.cols - 1:
                valueStr = valueStr + "  "
            print(valueStr, end="")
        print()
    print()
