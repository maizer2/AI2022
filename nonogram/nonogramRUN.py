def nonogramRUN():

    print("-"*30)
    
    rows_cols = input("rows ,cols : ").split(" ")
    while not len(rows_cols) == 2:
        print("too many values to unpack (expected 2)")
        rows_cols = input("rows ,cols : ").split(" ")

    rows, cols = int(rows_cols[0]), int(rows_cols[1])

    print("-"*30)

    row_values, col_values = [], []

    for row in range(1, rows + 1):

        row_value = input(f"Row{row} value : ").split(" ")
        while not len(row_value) <= 3:
            print("too many values to unpack (expected under 4)")
            row_value = input(f"Row{row} value : ").split(" ")
        row_values.append(tuple(row_value))

    for col in range(1, cols + 1):

        col_value = input(f"Col{col} value : ").split(" ")
        while not len(col_value) <= 3:
            print("too many values to unpack (expected under 4)")
            col_value = input(f"Col{col} value : ").split(" ")
        col_values.append(tuple(col_value))

    print(row_values)
    print(col_values)
