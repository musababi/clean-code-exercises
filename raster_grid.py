# TODO: refactor & clean up this class.
#  - Familiarize yourself with the code and what it does (it is easiest to read the tests first)
#  - refactor ...
#     - give the functions/variables proper names
#     - make the function bodies more readable
#     - clean up the test code where beneficial
#     - make sure to put each individual change in a small, separate commit
#     - take care that on each commit, all tests pass
from typing import Tuple, Iterable
from dataclasses import dataclass

class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def vector_to(self, point) -> Vector:
        return Vector(point.x - self.x, point.y - self.y)

class RasterGrid:
    @dataclass
    class Cell:
        index_x: int
        index_y: int

    def __init__(self,
                 x0: float,
                 y0: float,
                 x1: float,
                 y1: float,
                 nx: int,
                 ny: int) -> None:
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._nx = nx
        self._ny = ny
        self._number_of_cells = nx*ny

    @property
    def cells(self) -> Iterable[Cell]:
        return (
            self.Cell(i, j) for i in range(self._nx) for j in range(self._ny)
        )

    @property
    def number_of_cells(self):
        return self._number_of_cells

    def get_cell_center(self, cell: Cell) -> Tuple[float, float]:
        center_x = self._x0 + (float(cell.index_x) + 0.5)*(self._x1 - self._x0)/self._nx
        center_y = self._y0 + (float(cell.index_y) + 0.5)*(self._y1 - self._y0)/self._ny
        return (
            center_x,
            center_y
        )

    def get_cell(self, x: float, y: float) -> Cell:
        eps = 1e-6*max(
            (self._x1-self._x0)/self._nx,
            (self._y1-self._y0)/self._ny
        )
        if abs(x - self._x1) < eps:
            ix = self._nx - 1
        elif abs(x - self._x0) < eps:
            ix = 0
        else:
            ix = int((x - self._x0)/((self._x1 - self._x0)/self._nx))
        if abs(y - self._y1) < eps:
            iy = self._ny - 1
        elif abs(y - self._y0) < eps:
            iy = 0
        else:
            iy = int((y - self._y0)/((self._y1 - self._y0)/self._ny))
        return self.Cell(ix, iy)


def test_number_of_cells():
    x0 = 0.0
    y0 = 0.0
    dx = 1.0
    dy = 1.0
    assert RasterGrid(x0, y0, dx, dy, 10, 10).number_of_cells == 100
    assert RasterGrid(x0, y0, dx, dy, 10, 20).number_of_cells == 200
    assert RasterGrid(x0, y0, dx, dy, 20, 10).number_of_cells == 200
    assert RasterGrid(x0, y0, dx, dy, 20, 20).number_of_cells == 400


def test_locate_cell():
    grid = RasterGrid(0.0, 0.0, 2.0, 2.0, 2, 2)
    cell = grid.get_cell(0, 0)
    assert cell.index_x == 0 and cell.index_y == 0
    cell = grid.get_cell(1, 1)
    assert cell.index_x == 1 and cell.index_y == 1
    cell = grid.get_cell(0.5, 0.5)
    assert cell.index_x == 0 and cell.index_y == 0
    cell = grid.get_cell(1.5, 0.5)
    assert cell.index_x == 1 and cell.index_y == 0
    cell = grid.get_cell(0.5, 1.5)
    assert cell.index_x == 0 and cell.index_y == 1
    cell = grid.get_cell(1.5, 1.5)
    assert cell.index_x == 1 and cell.index_y == 1


def test_cell_center():
    grid = RasterGrid(0.0, 0.0, 2.0, 2.0, 2, 2)
    cell = grid.get_cell(0.5, 0.5)
    assert abs(grid.get_cell_center(cell)[0] - 0.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 0.5) < 1e-7
    cell = grid.get_cell(1.5, 0.5)
    assert abs(grid.get_cell_center(cell)[0] - 1.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 0.5) < 1e-7
    cell = grid.get_cell(0.5, 1.5)
    assert abs(grid.get_cell_center(cell)[0] - 0.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 1.5) < 1e-7
    cell = grid.get_cell(1.5, 1.5)
    assert abs(grid.get_cell_center(cell)[0] - 1.5) < 1e-7 and abs(grid.get_cell_center(cell)[1] - 1.5) < 1e-7


def test_cell_iterator() -> None:
    grid = RasterGrid(0.0, 0.0, 2.0, 2.0, 2, 2)
    count = sum(1 for _ in grid.cells)
    assert count == grid.number_of_cells

    cell_indices_without_duplicates = set(list(
        (cell.index_x, cell.index_y) for cell in grid.cells
    ))
    assert len(cell_indices_without_duplicates) == count
