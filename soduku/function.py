from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

def grid_values(grid):
    # In this function, you will take a sudoku as a string
    # and return a dictionary where the keys are the boxes,
    # for example 'A1', and the values are the digit at each
    # box (as a string) or '.' if the box has no value
    # assigned yet.
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def eliminate(values):
    # Write a function that will take as an input, the sudoku in dictionary form,
    # run through all the boxes, applying the eliminate technique,
    # and return the resulting sudoku in dictionary form.
    for key in values:
        value = values[key]
        if (len(value) == 1):
            # Row elimination
            for row in row_units:
                if key in row:
                    for row_unit in row:
                        if (len(values[row_unit]) != 1):
                            values[row_unit] = values[row_unit].replace(value, '');
            # Column elimination
            for col in column_units:
                if key in col:
                    for col_unit in col:
                        if (len(values[col_unit]) != 1):
                            values[col_unit] = values[col_unit].replace(value, '');
            # 3 * 3 elimination
            for square in square_units:
                if key in square:
                    for square_unit in square:
                        if (len(values[square_unit]) != 1):
                            values[square_unit] = values[square_unit].replace(value, '');
    return values;

display(eliminate(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')));
# display(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'));
