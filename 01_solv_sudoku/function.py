from utils import *

# `grid` is defined in the test code scope as the following:
# (note: changing the value here will _not_ change the test code)
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """

    starting_grid = {k: v for k, v in zip(boxes, grid)}

    # display(starting_grid)
    all_numbers = set()
    all_numbers.add('1')
    all_numbers.add('2')
    all_numbers.add('3')
    all_numbers.add('4')
    all_numbers.add('5')
    all_numbers.add('6')
    all_numbers.add('7')
    all_numbers.add('8')
    all_numbers.add('9')

    final_grid = starting_grid.copy()

    for k in starting_grid.keys():
        if starting_grid[k] not in '123456789':
            _peers = peers[k]
            not_avail_values = set()
            for pk in _peers:
                if starting_grid[pk] != '.':
                    not_avail_values.add(starting_grid[pk])
                    available_values = all_numbers - not_avail_values
                    available_values_str = "".join(
                        list(sorted(available_values)))

                    final_grid[k] = available_values_str

    return final_grid


def grid_values_sol(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):

    for unit in unitlist:
        # unit is a list of keys
        all_numbers = '123456789'
        for num in all_numbers:
            dplaces = []
            for box in unit:
                if num in values[box]:
                    dplaces.append((box, num))
            # print(dplaces)
            if len(dplaces) == 1:
                values[dplaces[0][0]] = dplaces[0][1]

    return values


# display(grid_values(grid))
# print("\n################################################################################n")
# print(eliminate(grid_values_sol(grid)))
# display(only_choice(eliminate(grid_values_sol(grid))))


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


print(reduce_puzzle(grid_values_sol(grid)))
if reduce_puzzle(grid_values_sol(grid)):
    display(reduce_puzzle(grid_values_sol(grid)))


grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
values = grid_values_sol(grid2)
display(reduce_puzzle(values))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


print()
print()
display(search(values))
