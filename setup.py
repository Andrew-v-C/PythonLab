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


def engFormatReal(value, precision):
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


def engFormat(value, precision, polar):
    if sp.im(value) == 0:
        return engFormatReal(sp.re(value), precision)
    else:
        if polar:
            magnitude = engFormatReal(sp.Abs(value), precision)
            angle = f"{sp.arg(value) * (180 / pi):.{precision}f}"
            return f"{magnitude} < {angle}"
        else:
            realPart = engFormatReal(sp.re(value), precision)
            imagPart = engFormatReal(abs(sp.im(value)), precision)
            sign = "+" if sp.im(value) >= 0 else "-"
            return f"{realPart} {sign} j {imagPart}"


def engPrint(input, precision=2, polar=False):
    # Determine if input is a matrix
    if isinstance(input, sp.Matrix):
        # Evaluate symbols
        input = input.evalf()
        # Determine column widths
        colWidths = [0] * input.cols
        for j in range(input.cols):
            for i in range(input.rows):
                valueStr = engFormat(input[i, j], precision, polar)
                colWidths[j] = max(colWidths[j], len(valueStr))
        # Print input rows
        for i in range(input.rows):
            print("[ ", end="")
            for j in range(input.cols):
                valueStr = engFormat(input[i, j], precision, polar)
                for k in range(int((colWidths[j] - len(valueStr)) / 2)):
                    valueStr = " " + valueStr
                while len(valueStr) < colWidths[j]:
                    valueStr = valueStr + " "
                if j < input.cols - 1:
                    valueStr = valueStr + "  "
                print(valueStr, end="")
            print(" ]")
    else:
        print(engFormat(input, precision, polar))
    print()
