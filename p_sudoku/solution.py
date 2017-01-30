import re;

rows = 'ABCDEFGHI'
cols = '123456789'
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[r+c for r, c in zip(rows, cols)], [r+c for r, c in zip(rows, cols[::-1])]]
assignments = []

# Standard version sudoku
s_unitlist = row_units + column_units + square_units
s_units = dict((s, [u for u in s_unitlist if s in u]) for s in boxes)
s_peers = dict((s, set(sum(s_units[s],[]))-set([s])) for s in boxes)

# Diagonal version sudoku
d_unitlist = row_units + column_units + square_units + diagonal_units
d_units = dict((s, [u for u in d_unitlist if s in u]) for s in boxes)
d_peers = dict((s, set(sum(d_units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values, diagonal=True):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        diagonal(bool): whether this sudoku is a diagonal one
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    unitlist_temp = d_unitlist if diagonal else s_unitlist;
    for unit in unitlist_temp:
        for box in unit:
            digits = values[box]
            if (len(digits) > 1):
                # Here I recoginize any array of same boxes that of same length as
                # the value in the box. For example: ['23','23'] are twins, ['123'.'123','123']
                # are triplets.
                twins = [temp_box for temp_box in unit if values[temp_box] == digits]
                if (len(twins) == len(digits)): # Find naked twins
                    for b in unit:
                        if (values[b] != digits):
                            values[b] = re.sub('['+digits+']', '', values[b])
    return values

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '.' for empties."
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values, diagonal=True):
    """Eliminate the immediate impossible values indicated by following basic rules.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        diagonal(bool): whether this sudoku is a diagonal one
    Returns:
        the values dictionary with the elimination strategy applied.
    """
    peers_temp = d_peers if diagonal else s_peers
    # Extract the solved values first
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        # Using the solved value to eliminate the value possibilities in other box
        for peer in peers_temp[box]:
            # Only eliminate the value if it is not solved
            if len(values[peer]) > 1:
                assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values, diagonal=True):
    """Eliminate values using the Only-Choice strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        diagonal(bool): whether this sudoku is a diagonal one
    Returns:
        the values dictionary with the Only-Choice strategy applied.
    """
    unitlist_temp = d_unitlist if diagonal else s_unitlist
    for unit in unitlist_temp:
        for digit in '123456789':
            # Search for a digit which only appeared once inside each unit
            # (which is the only-choice for this unit)
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values, diagonal=True):
    """Reduce the possible values in the board by recursivly apply the above
        three strategies.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        diagonal(bool): whether this sudoku is a diagonal one
    Returns:
        the values dictionary with the three strategies appled.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values, diagonal)
        # Use the Only Choice Strategy
        values = only_choice(values, diagonal)
        # Use the Naked Twin Strategy
        values = naked_twins(values, diagonal)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid, diagonal=True):
    result = search(grid_values(grid), diagonal)
    return result if result else grid_values(grid)


def search(values, diagonal=True):
    """Search through the tree of all possible sudokus to find a solution and avoid
        to stuck in a failure leaf.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        diagonal(bool): whether this sudoku is a diagonal one
    Returns:
        the solved sudoku values dictionary.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values, diagonal)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku,s, value)
        attempt = search(new_sudoku)
        if (attempt and (all(len(values[s]) == 1 for s in boxes))):
            return attempt
    return values
if __name__ == '__main__':
    # I replaced the given sudoku with a harder one (said by the sudoku generator)
    diag_sudoku_grid = '...5..43.85..4...64.2.3..57...7...6...7.1.9...6...3...34..7.6.97...9..14.91..5...'
    display(solve(diag_sudoku_grid, True))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
