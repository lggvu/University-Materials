"""Cryptarithmetic puzzle.

First attempt to solve equation CP + IS + FUN = TRUE
where each letter represents a unique digit.

This problem has 72 different solutions in base 10.
"""


from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s=%i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count


def CPIsFunSat():
    """Solve the CP+IS+FUN==TRUE cryptarithm."""
    # Constraint programming engine
    model = cp_model.CpModel()

    base = 10



    t = model.NewIntVar(1, base - 1, 'T')
    w = model.NewIntVar(0, base - 1, 'W')

    f = model.NewIntVar(1, base - 1, 'F')
    o = model.NewIntVar(0, base - 1, 'O')
    u = model.NewIntVar(0, base - 1, 'U')
    r = model.NewIntVar(0, base - 1, 'R')


    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [t, w, o, f, u, r]

    # Verify that we have enough digits.
    assert base >= len(letters)

    # Define constraints.
    model.AddAllDifferent(letters)

    # TWO + TWO = FOUR
    model.Add(t * base * base + w * base + o + t * base * base + w * base + o
             == f * base * base * base + o * base * base + u * base + r)

    ### Solve model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(letters)
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    # Solve.
    status = solver.Solve(model, solution_printer)

    print()
    print('Statistics')
    print('  - status          : %s' % solver.StatusName(status))
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    CPIsFunSat()PythPyt