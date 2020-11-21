import pandas as pd


def read_from_file(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()

    cols = ["K"+str(i+1) for i in range(12)]

    alternatives = pd.DataFrame(columns=cols)

    for i in range(15):
        serie = pd.DataFrame({"A" + str(i + 1): lines[i+1].split()}, index=cols).transpose()
        alternatives = alternatives.append(serie.astype("int64"))

    weights = pd.Series(lines[17].split(), index=cols)
    c, d = lines[19].split()
    return alternatives, weights.astype("int64"), float(c), float(d)


if __name__ == '__main__':
    alternatives, weights, c, d = read_from_file("Варіант №21 умова.txt")
    print(alternatives)