from nonogram.nonogram import *

def nonogramRUN():
    lines = []

    print("-"*30)
    
    rows_cols = input("rows ,cols : ").split(" ")

    while not len(rows_cols) == 2:
        print("too many values to unpack (expected 2)")
        rows_cols = input("rows ,cols : ").split(" ")

    lines.append(rows_cols)

    print("-"*30)
    rows = []
    cols = []

    for row in range(1, int(lines[0][0]) + 1):
        rows.append(input(f"Row{row} value : "))

    lines += rows[::-1]
    # lines += rows


    for col in range(1, int(lines[0][1]) + 1):
        cols.append(input(f"Col{col} value : "))
    
    lines += cols + ['']

    create_nonogram_csp(lines)
