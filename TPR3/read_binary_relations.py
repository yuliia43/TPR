import pandas as pd
from TPR.TPR3.pareto import *


def read_from_file(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()

    cols = ["k"+str(i+1) for i in range(12)]

    df = pd.DataFrame(columns=cols)

    for i, line in enumerate(lines):
        if i == 20:
            break
        serie = pd.DataFrame({"alternative" + str(i + 1): line.split()}, index=cols).transpose()
        df = df.append(serie)
    koefs = lines[22][:-1].split(">")
    classes_strs = lines[25].split("<")
    classes = []
    for class_koefs in classes_strs:
        class_koefs = class_koefs.replace("{", "")
        class_koefs = class_koefs.replace("}", "")
        class_koefs = class_koefs.replace(" ", "")
        class_koefs = class_koefs.replace("\n", "")
        classes.append(class_koefs.split(","))
    return df, koefs, classes


def write_in_file(pareto, maj, leks, beresovskiy, podinovskiy):
    with open("output.txt", 'a', encoding="utf-8") as f:
        f.truncate(0)
        f.write("Відношення переваги Парето\n")
        f.write(pareto.to_string(header=False, index=False))
        f.write("\n\nМажоритарне відношення переваги\n")
        f.write(maj.to_string(header=False, index=False))
        f.write("\n\nЛексикографічне відношення переваги\n")
        f.write(leks.to_string(header=False, index=False))
        f.write("\n\nВідношення переваги Березовського\n")
        f.write(beresovskiy.to_string(header=False, index=False))
        f.write("\n\nВідношення переваги Подиновського\n")
        f.write(podinovskiy.to_string(header=False, index=False))


if __name__ == '__main__':
    binary_relations, koefs, classes = read_from_file("Варіант №21.txt")
    pareto, maj, leks, beresovskiy, podinovskiy = check(binary_relations, koefs, classes)
    write_in_file(pareto, maj, leks, beresovskiy, podinovskiy)
