from sudoku.sudokuRUN import sudokuRUN
from nonogram.nonogramRUN import nonogramRUN

method = input("Input sudoku or nonogram : ")

if method == "sudoku":
    print(f"Start \"{method}\" Program")
    sudokuRUN()
elif method == "nonogram": 
    print(f"Start \"{method}\" Program")
    nonogramRUN()
else:
    print(f"{method} is Wrong Input")
    exit()