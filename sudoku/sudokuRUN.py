import copy
from docs.sudokucsp import SudokuCSP
from docs.csp import backtracking_search, mrv, unordered_domain_values, no_inference

def sudokuRUN():

    print("-"*30)
    print("SUDOKU INPUT")
    temp_arr = []

    for row in range(1, 10):
        temp = ""

        temp = input(f"Row {row} : ")

        while not len(temp.split(" ")) == 9:
            print("please 9 input values")
            temp = input(f"Row {row} : ")

        temp_arr.append(temp.split(" "))
    
    original_sudoku = []
    for arr in temp_arr:
        item_list = []
        for temp in arr:
            item_list.append(int(temp))
        original_sudoku.append(item_list)

    current_sudoku = copy.deepcopy(original_sudoku)

    s = SudokuCSP(current_sudoku)

    a = backtracking_search(
        csp=s, 
        select_unassigned_variable=mrv, 
        order_domain_values=unordered_domain_values,
        inference=no_inference
        )

    if a:
        for i in range(9):
            for j in range(9):
                index = i * 9 + j
                current_sudoku[i][j] = a.get("CELL" + str(index))

    print("-"*30)
    print("SUDOKU OUTPUT")
    
    for i in range(9):
        print(f"Row {i} : ", end="")
        for j in range(9):
            print(current_sudoku[i][j], end=" ")
        print()
