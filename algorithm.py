from prettytable import PrettyTable
import numpy as np
from copy import deepcopy

def dynamic(matrix):
    dynamic = [0 for _ in range(len(matrix[0]))]
    
    for row_index in range(len(matrix)):
        for column_index in range(len(matrix[0])):
            if (matrix[row_index][column_index] == 1) and (dynamic[column_index] == 0):
                dynamic[column_index] = row_index + 1
            elif (matrix[row_index][column_index] == 1) and (dynamic[column_index] > 0):
                dynamic[column_index] = -1
    return(dynamic)

def matrix_G(text):
    array1 = text.split('\n')
    array2 = []
    for numb in range(len(array1)):
        elem = list(map(int, array1[numb].split()))
        array2.append(elem)
    return(array2)

def to_Gsys(matrix):
    for i in range(1, len(matrix)+1):
        current_index = dynamic(matrix).index(i)
        if current_index != i-1:
            for row_index in range(len(matrix)):
                matrix[row_index][current_index], matrix[row_index][i-1] = matrix[row_index][i-1], matrix[row_index][current_index]
    return(matrix)

def to_Hsys2(matrix):
    for i in range(len(matrix), 0, -1):
        current_index = dynamic(matrix).index(i)
        if current_index != len(matrix[0])-(len(matrix)-(i-1)):
            for row_index in range(len(matrix)):
                matrix[row_index][current_index], matrix[row_index][len(matrix[0])-(len(matrix)-(i-1))] = matrix[row_index][len(matrix[0])-(len(matrix)-(i-1))], matrix[row_index][current_index]
    return(matrix)

def output_tbl(matrix):
    out = []
    for row in matrix:
        row = ' '.join(map(str, row))
        out.append(row)
    return(out)


def output(matrix):
        strings = []
        try:
            for row in matrix:
                string = ' '.join(map(str, row))
                strings.append(string)
            out = '\n'.join(strings)
        except:
            out = ' '.join(map(str, matrix))
        return(out)

def multi_S(mat, vec):
    indexes = [i for i in range(len(vec)) if vec[i] == 0]
    k = len(mat[0])
    count = 0
    mat = deepcopy(mat)
    for numb in indexes:
        mat.pop(numb-count)
        count += 1

    s = [0 for j in range(k)]
    if mat:
        for numb in range(len(mat)):
            row = mat[numb]
            string = []
            for ind in range(len(row)):
                if s[ind] == row[ind]:
                    string.append(0)
                else:
                    string.append(1)
            s = string
        return(s)
    else:
        return(s)

def table_1(mat, k):
    mat = deepcopy(mat)
    binary_str = [0 for j in range(2**k)]

    for i in range(2**k):
        binary_str[i] = str(bin(i))[2:]

        str_len = len(binary_str[i])

        if str_len < k:
            binary_str[i] = "0" * (k - str_len) + binary_str[i]

    binary_int = []
    for row in binary_str:
        string = list(row)
        string = list(map(int, string))
        binary_int.append(string)

    code_words = []
    for row in binary_int:
        code_words.append(multi_S(mat, row))

    overall_ones_quantity = []
    for row in code_words:
        inds = [i for i in range(len(row)) if row[i] == 1]
        overall_ones_quantity.append(len(inds))

    matr_for_dmin = deepcopy(overall_ones_quantity)
    matr_for_dmin.pop(0)
    dmin = min(matr_for_dmin)

    ro = dmin - 1

    t = int(ro / 2)
    return binary_int, code_words, overall_ones_quantity, dmin, t, ro

def table_2(matr, radio):
    def trans(matrix):
        matrix = np.array(matrix)
        matrix = matrix.transpose()
        matrix = matrix.tolist()
        return(matrix)

    def trans_cut(matrix):
        cut = []
        for elem in matrix:
            cut.append(elem[len(matrix):])
        cut = trans(cut)
        return(cut)
    
    def trans_cut2(matrix):
        cut = []
        for elem in matrix:
            cut.append(elem[:len(matrix[0])-len(matrix)])
            print(cut)
        cut = trans(cut)
        print(cut)
        return(cut)

    def to_Hsys(matrix):
        full_matrix = []
        once = []
        once_np = np.eye(len(matrix))
        once_np = once_np.tolist()
        for row in once_np:
            string = list(map(int, row))
            once.append(string)
        for numb in range(len(matrix)):
            row = np.concatenate((matrix[numb], once[numb]))
            row = row.tolist()
            full_matrix.append(row)
        return(full_matrix)

    def to_Gsys2(matrix):
        full_matrix = []
        once = []
        once_np = np.eye(len(matrix))
        once_np = once_np.tolist()
        for row in once_np:
            string = list(map(int, row))
            once.append(string)
        for numb in range(len(matrix)):
            row = np.concatenate((once[numb], matrix[numb]))
            row = row.tolist()
            full_matrix.append(row)
        return(full_matrix)
        
    def vectors_of_errors(matrix):
        vectors = []
        for numb in range(len(matrix), 0, -1):
            arr = np.zeros(len(matrix))
            arr = arr.tolist()
            arr = list(map(int, arr))
            arr[numb-1] = 1
            vectors.append(arr)
        return(vectors)
    
    def syndromes(matrix):
        syn = []
        for numb in range(len(matrix), 0, -1):
            syn.append(matrix[numb-1])
        syn
        return(syn)

    if radio:
        cut = trans_cut(matr)
        matrix_Hsys = to_Hsys(cut)
        matrix_Hsys_trans = trans(matrix_Hsys)
        vectors = vectors_of_errors(matrix_Hsys_trans)
        sydromes_Hsys = syndromes(matrix_Hsys_trans)
        return(matrix_Hsys, matrix_Hsys_trans, vectors, sydromes_Hsys)
    else:
        cut = trans_cut2(matr)
        matrix_Gsys = to_Gsys2(cut)
        matrix_Hsys_trans = trans(matr)
        vectors = vectors_of_errors(matrix_Hsys_trans)
        sydromes_Hsys = syndromes(matrix_Hsys_trans)
        return(matrix_Gsys, matrix_Hsys_trans, vectors, sydromes_Hsys)

def find_e(matrix, syndrome, vecs):
    syndrome = str(syndrome)
    matrix = list(map(str, matrix))

    index_e = matrix.index(syndrome)
    return(vecs[index_e])

def plus(e, v):
    string = []
    for ind in range(len(v)):
        if e[ind] == v[ind]:
            string.append(0)
        else:
            string.append(1)
    return(string)

def enter_G(text):
    matrix_g = matrix_G(text)
    n = len(matrix_g[0])
    k = len(matrix_g)
    speed = k/n
    words = 2**k

    matrix_g_sys = to_Gsys(matrix_g)

    Is, summ, counter, dmin, t, ro = table_1(matrix_g_sys, k)
    tbl_1 = PrettyTable()
    tbl_1.add_column('Информационные слова', output_tbl(Is))
    tbl_1.add_column('Кодовые слова', output_tbl(summ))
    tbl_1.add_column('d', counter)

    matrix_Hsys, matrix_Hsys_trans, vectors, syndromes_Hsys = table_2(matrix_g_sys, True)
    tbl_2 = PrettyTable()
    tbl_2.add_column('Синдромы', output_tbl(syndromes_Hsys))
    tbl_2.add_column('Векторы ошибок', output_tbl(vectors))
    
    res = f'Скорость кода = {speed}\nКоличество кодовых слов = {words}\n\nGsys\n{output(matrix_g_sys)}\n\nHsys\n{output(matrix_Hsys)}\n\n{tbl_1}\n\ndmin = {dmin}\nКоличество ошибок, которое код может исправить = {t}\nКоличество ошибок, которое код может обнаружить = {ro}\n\n{tbl_2}\n\nHsys транспонированная\n{output(matrix_Hsys_trans)}\n\n'
    return res

def enter_H(text):
    matrix_h = matrix_G(text)
    n = len(matrix_h[0])
    k = n - len(matrix_h)
    speed = k/n
    words = 2**k

    matrix_h_sys = to_Hsys2(matrix_h)

    matrix_Gsys, matrix_Hsys_trans, vectors, syndromes_Hsys = table_2(matrix_h_sys, False)
    tbl_2 = PrettyTable()
    tbl_2.add_column('Синдромы', output_tbl(syndromes_Hsys))
    tbl_2.add_column('Векторы ошибок', output_tbl(vectors))

    Is, summ, counter, dmin, t, ro = table_1(matrix_Gsys, k)
    tbl_1 = PrettyTable()
    tbl_1.add_column('Информационные слова', output_tbl(Is))
    tbl_1.add_column('Кодовые слова', output_tbl(summ))
    tbl_1.add_column('d', counter)
    
    res = f'Скорость кода = {speed}\nКоличество кодовых слов = {words}\n\nHsys\n{output(matrix_h_sys)}\n\nGsys\n{output(matrix_h_sys)}\n\n{tbl_1}\n\ndmin = {dmin}\nКоличество ошибок, которое код может исправить = {t}\nКоличество ошибок, которое код может обнаружить = {ro}\n\n{tbl_2}\n\nHsys транспонированная\n{output(matrix_Hsys_trans)}\n\n'
    return res

def enter_VG(txt, V):
    matrix_g = matrix_G(txt)
    matrix_g_sys = to_Gsys(matrix_g)
    matrix_Hsys, matrix_Hsys_trans, vectors, syndromes_Hsys = table_2(matrix_g_sys, True)
    V = list(map(int, V.split()))
    S = multi_S(matrix_Hsys_trans, V)
    e = find_e(syndromes_Hsys, S, vectors)
    c = plus(e, V)

    k = len(matrix_g)
    Is, summ, counter, dmin, t, ro = table_1(matrix_g_sys, k)
    index_I = summ.index(c)
    I = Is[index_I]
    res = f'S = {output(S)}\nC = {output(c)}\ni = {output(I)}\n\n'
    return res

def enter_VH(txt, V):
    matrix_h = matrix_G(txt)
    matrix_h_sys = to_Hsys2(matrix_h)
    matrix_Gsys, matrix_Hsys_trans, vectors, syndromes_Hsys = table_2(matrix_h_sys, False)
    V = list(map(int, V.split()))
    S = multi_S(matrix_Hsys_trans, V)
    e = find_e(syndromes_Hsys, S, vectors)
    c = plus(e, V)

    n = len(matrix_h[0])
    k = n - len(matrix_h)
    Is, summ, counter, dmin, t, ro = table_1(matrix_Gsys, k)

    index_I = summ.index(c)
    I = Is[index_I]
    res = f'S = {output(S)}\nC = {output(c)}\ni = {output(I)}\n\n'
    return res