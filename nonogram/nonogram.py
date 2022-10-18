import copy
import itertools
import hashlib
import json

"""
 This file is dedicated to converting nonograms (Griddlers)
 into Constraint Satisfaction Problems (CSPs)
"""

def domain_filtering(variables, domains, constraints, print_state):
    queue = get_all_arcs(constraints)
    while queue: # while queue has elements
        i, j = queue.pop(0) # select first element in arc queue
        revised = revise(variables, domains, constraints, i, j) # checks if arc is consistent
        if revised:
            # print_state((variables, domains, constraints))
            for (k, i) in get_all_neighboring_arcs(constraints, i):
                # arc was not consistent all neighboring arcs therfore need to be arc-consistent checked again
                if k != i:
                    queue.append((k, i))
    return domains

def revise(variables, domains, constraints, i, j):
    revised = False
    for x in domains[i]: # for every value in current domain for i
        satisfiable = False
        for y in domains[j]: # for every value in current domain for j
            filter_function = constraints[i][j]
            if filter_function(i,j,(x,y)):
                satisfiable = True # assigned value is satisfiable
                break
        if not satisfiable: # value is not satisfiable
            domains[i].remove(x) # remove value from domains
            revised = True # revise function did indeed remove a unvalid value from domains.
    return revised


def get_all_arcs(constraints):
    # Returns all arcs in problem
    return [(i, j) for i in constraints for j in constraints[i]]


def get_all_neighboring_arcs(constraints, variable):
    # Returns only arcs where given variable is present.
    result = [(i, variable) for i in constraints[variable]]
    result.extend([(variable, i) for i in constraints[variable]])
    return result

def is_solution(csp):
    # If all domains have a single value the csp is solved.
    
    _, domains, _ = csp
    for key, value in domains.items():
        if len(value) != 1:
            return False
    return True

def is_solvable(csp):
    _, domains, _ = csp
    # If any domain has zero possible values the csp is unsolvable.
    for _, value in domains.items():
        if len(value) == 0:
            return False
    return True

# Heuristics to select value that reduces domain most
def most_reducing_value(csp):
    variables, domains, constraints = csp
    value = 0
    for variable in variables:
        value += len(domains[variable])
    return value

# Heuristic to find variable with least possible values
def select_minimum_remaining_variable(csp):
    variables, domains, constraints = csp
    minimum = float("inf")
    min_variable = None
    for variable in variables:
        for domain in domains[variable]:
            domain_size = len(domain)
            if domain_size > 1 and domain_size < minimum:
                minimum = domain_size
                min_variable = variable
    return min_variable


def generate_successors(csp):
    # Generates all domain reduced successor for a csp state.
    variables, domains, constraints = csp
    successors = []

    # Loop over possible values for all variables
    for variable in variables:
        for value in domains[variable]:

            # Copy domain to prevent catastrophe
            assignment = copy.deepcopy(domains)

            # Make assumption
            assignment[variable] = [value]

            # Domain filter assumption
            assignment = domain_filtering(variables, assignment, constraints, print_nonogram)
            successor_state = (variables, assignment, constraints)
            if is_solvable(successor_state):
                successors.append(successor_state) # Only add solvable states
    return successors


# Hash csp state for closed sets
def hash_state(csp):
    variables, domains, constraints = csp
    return hashlib.sha1(json.dumps(domains, sort_keys=True)).hexdigest()


# Combination of best_first_search and GAC to that solves CSP's
def gac_and_best_first(variables, domains, constraints):

    # Reduce domains with GAC
    reduced_domains = domain_filtering(variables, domains, constraints, print_nonogram)

    # Pack problem into tuple such that it's ready for best-first search
    problem = (variables, reduced_domains, constraints)

    # Checks if CSP problem can be solved (no domains with zero values)
    if not is_solvable(problem):
        print('No solution')
        exit()

    # There is no need to search for an solution when domain filtering solves it.
    if is_solution(problem):
        print_nonogram(problem)
    else:
        # Search for a solution utilizing a general best-first algorithm
        result, generated, expanded = best_first_search(problem, hash_state, is_solution, generate_successors, most_reducing_value, print_nonogram)  # type: ignore

        # Display Stats from search
        print_nonogram(result)
        print("Generated Nodes", generated)
        print("Expanded Nodes", expanded)

def create_nonogram_csp(lines):

    number_of_cols = int(lines[0][0])
    number_of_rows =  int(lines[0][1])

    row_spec = [row for row in lines[1:number_of_rows + 1]][::-1]
    col_spec = [col for col in lines[len(lines) - 1 - number_of_cols:len(lines) - 1]]

    # Finished reading file, time to turn this into a CSP problem

    variables = []
    domains = {}
    constraints = {}

    # Add all rows and their domain
    for i in range(len(row_spec)):
        segment_specification = map(int, list(row_spec[i].split()))
        domain = generate_domains_from_specifications(number_of_cols, segment_specification)
        variable = "R" + str(i)

        variables.append(variable)
        domains[variable] = domain
        constraints[variable] = {}

    # Add all cols and their domain
    for i in range(len(col_spec)):
        segment_specification = map(int, list(col_spec[i].split()))
        domain = generate_domains_from_specifications(number_of_rows, segment_specification)
        variable = "C" + str(i)

        variables.append(variable)
        domains[variable] = domain
        constraints[variable] = {}

    # Only thing left now is creating some constraints betwen rows and cols
    row_variables = filter(lambda x: 'R' in x, variables)
    col_variables = filter(lambda x: 'C' in x, variables)


    for (row, col) in itertools.product(row_variables, col_variables):
        constraints[row][col] = compatible_value_pair
        constraints[col][row] = compatible_value_pair

    # Return nonogramp represented as a CSP
    gac_and_best_first(variables, domains, constraints)

def generate_domains_from_specifications(length, specifications):
    # Clever function to generate possible domains for a rows and cols

    domain = []
    min_placement = []
    for s in specifications:
        for i in range(s):
            min_placement.append(1)
        min_placement.append(0)
    min_placement.pop(len(min_placement) - 1)

    insert_indices = [i + 1 for i, x in enumerate(min_placement) if x == 0]
    insert_indices.extend([0, len(min_placement)])
    combinations = itertools.combinations_with_replacement(insert_indices, length - len(min_placement))

    for c in combinations:
        result = min_placement[:]
        insert_positions = list(c)
        insert_positions.sort()
        offset = 0
        for index in insert_positions:
            result.insert(index + offset, 0)
            offset += 1
        domain.append(result)
    return domain

# takes a row and a column and checks if the value where they meet is the same
def compatible_value_pair(i, j, value_pair):
    x, y = value_pair
    x_index = int(i[1:])
    y_index = int(j[1:])
    return x[y_index] == y[x_index]

# Prints nonogram to console
def print_nonogram(result):
    _, domains, _ = result

    sorted_keys = []
    for key in domains.keys():
        if "R" in key:
            sorted_keys.append(int(key[1:]))
    sorted_keys.sort()
    for key in sorted_keys:
        for bit in domains['R' + str(key)][0]:
            if bit == 1:
                print('*', end="")
            else:
                print(' ', end="")
        print()
    print()
