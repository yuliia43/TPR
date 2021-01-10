import numpy as np
import pandas as pd


# виконання операції об'єднання
def union_operation(R1, R2):
    union = np.maximum(R1, R2)
    return union


# виконання операції перетину
def intersection_operation(R1, R2):
    intersection = np.minimum(R1, R2)
    return intersection


# виконання операції доповнення
def addition_operation(R):
    addition = 1 - R
    return addition


# виконання операції композиції
def composition_operation (R1, R2):
    comp_cols = []
    for i in range(0, len(R1)):
        row = R1.iloc[i].to_numpy()[:, None]
        min_row = np.minimum(row, R2)
        comp_cols.append(np.max(min_row, axis=0))
    composition = pd.DataFrame(data=comp_cols, index=R1.index)
    return composition


# перевірка властивості рефлексивності
def check_reflection(R):
    main_diagonal = R.to_numpy().diagonal()
    refl = False
    if np.min(main_diagonal) == 1:
        refl = True
        if len(np.where(main_diagonal >= np.max(R, axis=1))) == R.shape[0]:
            print("СЛАБКА РЕФЛЕКСИВНІСТЬ")
        elif np.where(R == 1)[0].shape[0] == main_diagonal.shape[0]:
            print("СИЛЬНА РЕФЛЕКСИВНІСТЬ")
        else:
            print("РЕФЛЕКСИВНІСТЬ")
    else:
        print("Рефлексивність відсутня")
    return refl


# перевірка властивості антирефлексивності
def check_antireflection(R):
    main_diagonal = R.to_numpy().diagonal()
    if np.max(main_diagonal) == 0:
        if len(np.where(main_diagonal <= np.min(R, axis=1))) == R.shape[0]:
            print("СЛАБКА АНТИРЕФЛЕКСИВНІСТЬ")
        elif np.where(R == 0)[0].shape[0] == main_diagonal.shape[0]:
            print("СИЛЬНА АНТИРЕФЛЕКСИВНІСТЬ")
        else:
            print("АНТИРЕФЛЕКСИВНІСТЬ")
    else:
        print("Антирефлексивність відсутня")


def check_symmetry(R):
    if np.all(R-R.T == 0):
        print("СИМЕТРИЧНІСТЬ")
    else:
        copy_R = R.copy().to_numpy()
        np.fill_diagonal(copy_R, 0)
        if np.all(np.minimum(copy_R, copy_R.T) == 0):
            if check_antireflection(R):
                print("АСИМЕТРИЧНІСТЬ")
            else:
                print("АНТИСИМЕТРИЧНІСТЬ")
        else:
            print("Симетричність, асиметричність, антисиметричність відсутні")


def check_fullness(R):
    if np.all(np.maximum(R, R.T) > 0):
        if np.all(np.maximum(R, R.T) == 1):
            print("СИЛЬНА ПОВНОТА")
        else:
            print("СЛАБКА ПОВНОТА")
    else:
        print("Повнота відсутня")


# перевірка властивості транзитивності
def check_transitivity(R):
    R = R.to_numpy()
    isTransitive = True
    for x in range(0, len(R)):
        for y in range(0, len(R)):
            for z in range(0, len(R)):
                if min(R[x][y],R[y][z]) > R[x][z]:
                    isTransitive = False
                    break

    if isTransitive:
        print("ТРАНЗИТИВНІСТЬ")
    else:
        print("Транзитивність відсутня")


# пошук альфа-рівнів з заданим альфа
def alpha_level(alpha, R):
    alpha = np.where(R >= alpha, 1, 0)
    alpha = pd.DataFrame(alpha, columns=R.columns, index=R.index)
    return alpha


# побудова асоційованих відношень строгої переваги
def assosiate_relation(R):
    RS = np.where(R >= R.T, R-R.T, 0)
    RS = pd.DataFrame(RS, columns=R.columns, index=R.index)
    return RS


# побудова відношення квазі-еквівалентності
def quasi_equialent_relation(R):
    RE = np.minimum(R, R.T)
    return RE


# відношення байдужості
def indifference(R):
    result = np.maximum(1-np.maximum(R, R.T), np.minimum(R, R.T))
    return result


#пошук множини недомінованих альтернатив
def max_not_dominate(RS):
    miu = 1 - np.max(RS, axis=0)
    return find_best_and_ranging(miu)


def find_best_and_ranging(miu):
    ranging = miu.sort_values(ascending=False)
    best = ranging[ranging == np.max(ranging)].index
    return list(best), ranging


#задача пошуку рішення з 1м експертом
def one_expert(R):
    print("Задача ПР з одним експертом\n____________________________")
    RS = assosiate_relation(R)
    best_u, ranging = max_not_dominate(RS)
    print("Ранжування")
    print(ranging.to_string())
    print("Найкращі альтернативи: ", best_u)


# побудова згортки відношень переваги
def convolution_advantage_relation(list_of_experts):
    MP = list_of_experts[0]
    for expert in list_of_experts[1:]:
        MP = np.minimum(MP, expert)

    return MP

# побудова опуклої згортки відношень
def convex_convolution_relation(list_of_experts, weights):
    MQ = list_of_experts[0]*weights[0]
    for expert_idx in range(1, len(list_of_experts)):
        MQ = MQ + weights[expert_idx]*list_of_experts[expert_idx]

    return MQ

# пошук множини недомінованих альтернатив
def not_dominate_subset(MPS, MQS):
    _, UPnd = max_not_dominate(MPS)
    _, UQnd = max_not_dominate(MQS)

    return UPnd, UQnd

# пошук найкращих альтернатив
def best_alternatives(UPnd, UQnd):
    print("________________________________\nЗадача ПР групою експертів\n____________________________")
    intersection = intersection_operation(UPnd, UQnd)
    best, ranging = find_best_and_ranging(intersection)
    print("Ранжування:")
    print(ranging.to_string())
    print("Найкращі альтернативи: ", best)

def several_experts(list_of_experts, weights):
    MP = convolution_advantage_relation(list_of_experts)
    MQ = convex_convolution_relation(list_of_experts, weights)
    MPS = assosiate_relation(MP)
    MQS = assosiate_relation(MQ)
    UPnd, UQnd = not_dominate_subset(MPS, MQS)
    best_alternatives(UPnd, UQnd)

# пошук властивостей
def find_properties(list_of_experts):
    union = union_operation(list_of_experts[0], list_of_experts[1])
    print("Об'єднання відношень M1 та M2")
    print(union)
    print("Перетин відношень M1 та M2")
    intersection = intersection_operation(list_of_experts[0], list_of_experts[1])
    print(intersection)
    print("Доповнення відношення M1")
    addition1 = addition_operation(list_of_experts[0])
    print(addition1)
    print("Доповнення відношення M2")
    addition2 = addition_operation(list_of_experts[1])
    print(addition2)
    print("Відношення байдужості M1")
    indifference1 = indifference(list_of_experts[0])
    print(indifference1)
    print("Відношення байдужості M2")
    indifference2 = indifference(list_of_experts[1])
    print(indifference2)
    print("Композиція відношень M1 та M2")
    composition = composition_operation(list_of_experts[0], list_of_experts[1])
    print(composition)
    print("Альфа-рівень при альфа = 0.5")
    alpha = alpha_level(0.5, list_of_experts[0])
    print(alpha)
    print("Альфа-рівень при альфа = 0.9")
    alpha = alpha_level(0.9, list_of_experts[0])
    print(alpha)
    print("Відношення строгої переваги:")
    RS = assosiate_relation(list_of_experts[0])
    print(RS)
    print("Відношення квазі-еквівалентності:")
    RE = quasi_equialent_relation(list_of_experts[0])
    print(RE)
    for i, expert in enumerate(list_of_experts):
        print("________________________________")
        print("Властивості відношення М"+str(i+1))
        refl = check_reflection(expert)
        if not refl:
            check_antireflection(expert)
        check_symmetry(expert)
        check_fullness(expert)
        check_transitivity(expert)
    print("________________________________")


if __name__ == '__main__':
    weights = [0.2, 0.12, 0.23, 0.31, 0.14]
    rows = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    M1 = pd.DataFrame(data={'A1': [0.9, 0.9, 1.0, 0.2, 0.1, 0.3],
                            'A2': [0.5, 1.0, 0.6, 0.1, 0.5, 0.9],
                            'A3': [0.2, 0.3, 0.9, 0.6, 0.3, 0.1],
                            'A4': [0.2, 0.8, 0.6, 0.5, 0.3, 0.1],
                            'A5': [0.3, 1.0, 0.2, 0.3, 0.5, 0.8],
                            'A6': [1.0, 0.0, 0.4, 0.9, 0.5, 0.2]},
                      index=rows)
    M2 = pd.DataFrame(data={'A1': [0.8, 0.2, 0.2, 0.2, 0.5, 0.1],
                            'A2': [0.1, 0.5, 0.2, 0.3, 0.5, 0.6],
                            'A3': [0.4, 0.5, 0.5, 0.1, 0.8, 0.8],
                            'A4': [0.0, 0.8, 0.7, 0.1, 0.4, 0.4],
                            'A5': [0.7, 1.0, 0.1, 0.8, 0.5, 0.7],
                            'A6': [0.4, 0.6, 0.4, 0.2, 0.2, 1.0]},
                      index=rows)
    M3 = pd.DataFrame(data={'A1': [0.1, 0.8, 0.3, 0.9, 0.2, 0.6],
                            'A2': [0.7, 0.7, 0.6, 0.8, 0.6, 0.7],
                            'A3': [0.1, 0.1, 0.4, 0.2, 0.2, 0.6],
                            'A4': [0.8, 0.9, 0.2, 0.7, 0.0, 0.1],
                            'A5': [0.3, 0.3, 0.2, 0.8, 0.4, 0.8],
                            'A6': [0.8, 1.0, 0.2, 0.8, 0.5, 0.7]},
                      index=rows)
    M4 = pd.DataFrame(data={'A1': [0.9, 0.7, 0.8, 0.0, 0.4, 0.6],
                            'A2': [1.0, 0.4, 0.7, 0.6, 0.6, 0.3],
                            'A3': [0.8, 0.8, 0.4, 0.7, 0.6, 0.2],
                            'A4': [0.7, 0.7, 0.6, 0.8, 0.6, 0.3],
                            'A5': [1.0, 0.4, 1.0, 0.3, 0.6, 0.1],
                            'A6': [0.2, 0.9, 0.9, 0.7, 0.8, 0.4]},
                      index=rows)
    M5 = pd.DataFrame(data={'A1': [0.6, 0.3, 0.8, 0.7, 0.2, 0.8],
                            'A2': [0.6, 0.9, 1.0, 0.8, 0.3, 0.8],
                            'A3': [0.3, 1.0, 0.8, 0.8, 0.7, 0.2],
                            'A4': [0.3, 0.3, 0.5, 0.3, 0.5, 0.6],
                            'A5': [0.1, 0.7, 0.6, 0.3, 0.3, 0.7],
                            'A6': [0.8, 0.0, 0.3, 0.7, 0.5, 0.7]},
                      index=rows)

    find_properties([M1, M2, M3, M4, M5])
    one_expert(M1)
    several_experts([M1, M2, M3, M4, M5], weights)
