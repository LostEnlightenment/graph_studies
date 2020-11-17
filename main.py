###############################################################################
# программа генерирует матрицу смежности M, описывающую граф со случайным
# выбором связей с учётом предпочтения высокостепенным узлам
# (модель Барабаши-Альберт). Затем выводится на график респределение узлов
# графа по степеням.
###############################################################################

import numpy as np
import random as rnd
import matplotlib.pyplot as plt

M = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], int)  # инициализация
# 'затравки' - начальной матрицы 3 x 3, которая определяет полносвязный граф
# из трёх узлов

N = 20  # число итераций роста графа (на каждой итерации
# присоединяется 1 узел)

m = M.shape[0]  # эта переменная будет получать инкремент в цикле
# (m отвечает за рост матрицы)

for i in range(N):  # внутри этого цикла генерируется матрица M
    print('\n\nитерация :', i + 1)
    print('присоединение нового узла ...')
    grow = np.zeros(m, int).reshape(1, m)
    M = np.concatenate((M, grow), axis=0)
    grow = np.zeros(m + 1, int).reshape(1, m + 1)
    M = np.concatenate((M, grow.T), axis=1)
    print(M)
    print(M.shape)

    print('генерация первой связи нового узла ...')
    wts = np.sum(M, axis=1).tolist()
    wts[m] = 0  # исключение связи "с собой" из числа потенциальных связей
    print('wts = ', wts)

    nodes = np.arange(0, m + 1, 1)
    print('nodes = ', nodes)

    link_1 = rnd.choices(nodes, wts)[0].astype(int)  # генерация первой связи
    # нового узла
    print('link 1 = ', link_1)
    M[m, link_1] = 1
    M[link_1, m] = 1
    print(M)

    print('генерация второй связи нового узла ...')
    wts = np.sum(M, axis=1).tolist()
    wts[m] = 0  # исключение связи "с собой" из числа потенциальных связей
    wts[link_1] = 0  # исключение связи, кратной первой
    # из числа потенциальных связей
    print('wts = ', wts)

    link_2 = rnd.choices(nodes, wts)[0].astype(int)  # генерация второй связи
    # нового узла
    print('link 2 = ', link_2)
    M[m, link_2] = 1
    M[link_2, m] = 1
    print(M)
    m += 1

pw_min = 2  # минимальная степень узла в графе
pws = np.sum(M, axis=1).tolist()
print('\n\nсписок степеней каждого из узлов: ', pws)
pw_max = max(pws)
print('макимальная степень: ', pw_max)

N_nds = []  # населённость узлами каждой из степеней,
# отображается столбиком на графике
j = 0
for i in range(pw_min, pw_max+1):
    N_nds.append(pws.count(i))
    j += 1

print('список населённостей: ', N_nds)
print('в сумме составляют ', np.sum(N_nds), 'узла/узлов')
N_arr = np.arange(pw_min, pw_max+1)  # степени по возрастанию
# отображаются на оси абсцисс
print('степени по возрастанию от мин. до макс.: ', N_arr)

plt.bar(N_arr, N_nds)  # график распределения узлов графа по степеням
lgnd = plt.legend([r'$N_{k}(k)$'],
                  loc='upper center', shadow=True)
lgnd.get_frame().set_facecolor('#cccccc')

plt.show()
