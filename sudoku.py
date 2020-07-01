import numpy as np
import random as rd

def row_check(table, row_index) :
    """checks if the specified row of a given is valid"""
    assert(row_index >= 0)
    assert(row_index <= 8)
    row = table[row_index]
    row_nums = row[row != 0]
    return len(set(row_nums)) == len(row_nums)

def col_check(table, col_index) :
    """checks if the specified col of a given is valid"""
    assert(col_index >= 0)
    assert(col_index <= 8)
    col = table[:, col_index]
    col_nums = col[col != 0]
    return len(set(col_nums)) == len(col_nums)

def blo_check(table, blo_index) :
    """checks if the specified blo of a given is valid"""
    assert(blo_index >= 0)
    assert(blo_index <= 8)
    blo = table[(blo_index // 3) * 3 : (blo_index // 3) * 3 + 3,
               (blo_index % 3) * 3: (blo_index % 3) * 3 + 3]
    blo.flatten()
    blo_nums = blo[blo != 0]
    return len(set(blo_nums)) == len(blo_nums)

def cell_check(table, row_index, col_index) :
    blo_index = (row_index // 3) * 3 + (col_index // 3)
    return (row_check(table, row_index) and
            col_check(table, col_index) and
            blo_check(table, blo_index))

def is_full(table) :
    a = table.flatten()
    assert(len(a) == 81)
    for j in range(81) :
        if (a[j] == 0) :
            return False
    return True

def is_solved(table) :
    assert(is_full(table))
    for j in range(9) :
        if not (row_check(table, j) and
                col_check(table, j) and
                blo_check(table, j)) :
            return False
    return True

def fancy_print(table) :
    for j in range(9) :
        if (j % 3 == 0) :
            print('-' * 37)
        row_list = list(table[j])
        for j in range(9) :
            if (row_list[j] == 0) :
                row_list[j] = ' '
            else :
                row_list[j] = int(row_list[j])
        print('|', row_list[0], ' ', row_list[1], ' ', row_list[2], '|',
              row_list[3], ' ', row_list[4], ' ', row_list[5], '|',
              row_list[6], ' ', row_list[7], ' ', row_list[8], '|')
    print('-' * 37)

def fill_cell(table, j, nums_arr) :
    """
    fill the j'th cell with a random number from the j'th set in nums_arr
    """
    row_index = j // 9
    col_index = j % 9
    nums = list(nums_arr[j])
    rd.shuffle(nums)
    for n in nums :
        table[row_index][col_index] = n
        if (cell_check(table, row_index, col_index)) :
            return 1
    table[row_index][col_index] = 0
    nums_arr[j] = {}
    return 0

def back(table, j, nums_arr) :
    assert(len(nums_arr[j]) == 0)
    while (len(nums_arr[j]) == 0) :
        nums_arr[j] = set(range(1, 10))
        j = j - 1
        row_index = j // 9
        col_index = j % 9
        n = table[row_index][col_index]
        nums_arr[j].remove(n)
    return j

def possibilities(table, row_index, col_index) :
    back_up = table[row_index][col_index]
    p = []
    for n in range(1, 10) :
        table[row_index][col_index] = n
        if (cell_check(table, row_index, col_index)) :
            p.append(n)
    table[row_index][col_index] = back_up
    return p

def delete_cell(table, row_index, col_index) :
    """
    try to delete the specified cell: if solution to that cell is
    unique, then delete it; if not deletable, then return 0 and do nothing.
    effects: may modify table
    """
    assert(table[row_index][col_index])
    p = possibilities(table, row_index, col_index)
    assert(len(p) != 0)
    value = table[row_index][col_index]
    assert(value in range(1, 10))
    if (len(p) == 1) :
        assert(value == p[0])
        table[row_index][col_index] = 0
        return [1, value]
    else :
        return [0, value]

def delete_onemore(table, remaining, deleted, recovered) :
    """
    try to delete one more cell: if can find another deletable cell, then
    delete it; if none of the remaining can be deleted, then return 0 and do
    nothing.
    effects: may modify table, remaining, and deleted
    will not modify recovered.
    """
    assert(len(remaining) + len(deleted) == 81)
    assert(len(remaining) >= len(recovered))
    choices = list(set(remaining) - set(recovered))
    while (1) :
        if (len(choices) == 0) :
            return 0
        index = rd.choice(choices)
        row_index = index // 9
        col_index = index % 9
        assert(table[row_index][col_index])
        success, value = delete_cell(table, row_index, col_index)
        if success :
            remaining.remove(index)
            deleted.append([index, value])
            recovered = []
            return 1
        else :
            choices.remove(index)

def recover_last(table, remaining, deleted, recovered) :
    """
    insert the last cell deleted back to table.
    requires: deleted is not empty
    effects: may modify table, remaining, deleted, and recovered
    """
    assert(len(deleted) != 0)
    assert(len(remaining) != 81)
    index, value = deleted[len(deleted) - 1]
    row_index = index // 9
    col_index = index % 9
    assert(table[row_index][col_index] == 0)
    table[row_index][col_index] = value
    remaining.append(index)
    deleted.remove(deleted[len(deleted) - 1])
    recovered.append(index)

def new_game() :
    """generate a randomly filled """
    table = np.zeros((9, 9), dtype = int)
    #initialize a possibility array
    nums_arr = []
    for j in range(81) :
        nums_arr.append(set(range(1, 10)))
    #start to fill full table
    j = 0
    counter = 0
    while (j in range(81)) :
        success = fill_cell(table, j, nums_arr)
        counter += 1
        if success :
            j += 1
        else :
            j = back(table, j, nums_arr)
    assert(is_full(table))
    assert(is_solved(table))
    print("steps taken: ", counter)
    print("successfully initialized")
    return table

def generate(table, difficulty) :
    #start to eliminate cells
    assert(type(difficulty) == int)
    assert(difficulty >= 0)
    assert(difficulty <= 81)
    starting = list(range(81))
    for i in range(81) :
        start_index = rd.choice(starting)
        row_index = start_index // 9
        col_index = start_index % 9
        success, value = delete_cell(table, row_index, col_index)
        assert(success)
        j = 1
        remaining = list(range(81))
        remaining.remove(start_index)
        deleted = [[start_index, value]]
        recovered = []
        while j in range(difficulty + 1) :
            success = delete_onemore(table, remaining, deleted, recovered)
            if success :
                j += 1
            else :
                if (len(deleted) == 0) :
                    # meaning we have recovered till the full table.
                    starting.remove(start_index)
                    break
                recover_last(table, remaining, deleted, recovered)
                j -= 1
        if (j not in range(difficulty + 1)) :
            # meaning we have successfully eliminated specified number of
            # cells.
            print("times tried:", i+1)
            print("successfully generated, difficulty =", difficulty)
            return 1
    return 0
    print("Too hard! Cannot generate a table like that.")

def is_empty(table, row_index, col_index) :
    return table[row_index][col_index] == 0

def possibility_list(table) :
    p = []
    for j in range(81) :
        row_index = j // 9
        col_index = j % 9
        if (is_empty(table, row_index, col_index)) :
            p.append(possibilities(table, row_index, col_index))
        else :
            p.append([table[row_index][col_index]])
    return p

def related_cells(row_index, col_index) :
    r_list = set()
    for j in range(9) :
        r_list.add(j * 9 + col_index)
        r_list.add(row_index * 9 + j)
    coner_row_index = (row_index // 3) * 3
    coner_col_index = (col_index // 3) * 3
    for j in range(3) :
        for k in range(3) :
            index = (coner_row_index + j) * 9 + (coner_col_index + k)
            r_list.add(index)
    r_list = list(r_list)
    index = row_index * 9 + col_index
    r_list.remove(index)
    assert(len(r_list) == 20)
    return r_list

def fill(table, e_list, p_list, f_list) :
    """
    e_list is the list of indices of empty cells in table.
    p_list is the possibility list.
    f_list is the list of indices of cells that are empty and have only one
    possibility, which means they are the ones to be filled.
    """
    assert(len(f_list) >= 1)
    index = f_list[0]
    row_index = index // 9
    col_index = index % 9
    assert(len(p_list[index]) == 1)
    n = p_list[index][0]
    assert(table[row_index][col_index] == 0)
    table[row_index][col_index] = n
    
    e_list.remove(index)
    f_list.remove(index)
    r_list = related_cells(row_index, col_index)
    l = list(set.intersection(set(r_list), set(e_list)))
    for index in l :
        if (n in p_list[index]) :
            p_list[index].remove(n)
            if (len(p_list[index]) == 1) :
                f_list.append(index)
            else :
                assert(len(p_list[index]) != 0)

def empty_cells(table) :
    e_list = []
    for j in range(81) :
        row_index = j // 9
        col_index = j % 9
        if (table[row_index][col_index] == 0) :
            e_list.append(j)
    return e_list

def get_f_list(p_list) :
    f_list = []
    assert(len(p_list) == 81)
    for index in range(81) :
        l = len(p_list[index])
        assert(l)
        if (l == 1) :
            f_list.append(index)
    return f_list

def solve(table) :
    e_list = empty_cells(table)
    p_list = possibility_list(table)
    f_list = get_f_list(p_list)
    f_list = list(set.intersection(set(e_list), set(f_list)))
    while (len(e_list) != 0) :
        fill(table, e_list, p_list, f_list)
    assert(is_full(table))
    assert(is_solved(table))
    print("successfully solved")

HARD = 53

table = new_game()
fancy_print(table)

generate(table, 40)
fancy_print(table)
print(table)

#solve(table)
#fancy_print(table)

def plain_print(table) :
    for row in range(9) :
        for col in range(9) :
            if (col != 8) :
                print(table[row][col], end='')
            else :
                print(table[row][col])

plain_print(table)