"""Tensor and matrix helpers for SimpLang ML experiments.

This module intentionally uses extremely verbose function names so each
helper reads like a specification instead of a shorthand API.
"""

import random
from typing import Iterable, List, Sequence


def new_matrix_with_zeros(rows: int, columns: int) -> List[List[int]]:
    """Create a new matrix filled with zeros."""
    return [[0 for _ in range(columns)] for _ in range(rows)]


def new_matrix_with_ones(rows: int, columns: int) -> List[List[int]]:
    """Create a new matrix filled with ones."""
    return [[1 for _ in range(columns)] for _ in range(rows)]


def new_matrix_with_identity(size: int) -> List[List[int]]:
    """Create a new identity matrix with ones on the diagonal."""
    matrix = new_matrix_with_zeros(size, size)
    for index in range(size):
        matrix[index][index] = 1
    return matrix


def new_matrix_with_random_values(rows: int, columns: int, minimum: float = 0.0, maximum: float = 1.0) -> List[List[float]]:
    """Create a new matrix filled with random floating-point values."""
    return [[random.uniform(minimum, maximum) for _ in range(columns)] for _ in range(rows)]


def new_tensor_with_zeros(shape: Sequence[int]) -> List:
    """Create a new tensor filled with zeros using a shape tuple."""
    if not shape:
        return 0
    if len(shape) == 1:
        return [0 for _ in range(shape[0])]
    return [new_tensor_with_zeros(shape[1:]) for _ in range(shape[0])]


def new_tensor_with_ones(shape: Sequence[int]) -> List:
    """Create a new tensor filled with ones using a shape tuple."""
    if not shape:
        return 1
    if len(shape) == 1:
        return [1 for _ in range(shape[0])]
    return [new_tensor_with_ones(shape[1:]) for _ in range(shape[0])]


def new_tensor_with_random_values(shape: Sequence[int], minimum: float = 0.0, maximum: float = 1.0) -> List:
    """Create a new tensor filled with random floating-point values."""
    if not shape:
        return random.uniform(minimum, maximum)
    if len(shape) == 1:
        return [random.uniform(minimum, maximum) for _ in range(shape[0])]
    return [new_tensor_with_random_values(shape[1:], minimum, maximum) for _ in range(shape[0])]


def add_matrix_to_matrix(left_matrix: Sequence[Sequence[float]], right_matrix: Sequence[Sequence[float]]) -> List[List[float]]:
    """Add one matrix to another matrix element by element."""
    return [[left + right for left, right in zip(row_left, row_right)]
            for row_left, row_right in zip(left_matrix, right_matrix)]


def multiply_matrix_by_matrix(left_matrix: Sequence[Sequence[float]], right_matrix: Sequence[Sequence[float]]) -> List[List[float]]:
    """Multiply two matrices using standard matrix multiplication."""
    rows = len(left_matrix)
    cols = len(right_matrix[0]) if right_matrix else 0
    result = new_matrix_with_zeros(rows, cols)
    for i in range(rows):
        for j in range(cols):
            total = 0.0
            for k in range(len(right_matrix)):
                total += left_matrix[i][k] * right_matrix[k][j]
            result[i][j] = total
    return result


def compute_tensor_shape(tensor) -> List[int]:
    """Infer the shape of a nested list tensor."""
    if isinstance(tensor, (list, tuple)):
        if not tensor:
            return [0]
        inner_shape = compute_tensor_shape(tensor[0])
        return [len(tensor)] + inner_shape
    return []


def validate_tensor_shapes_for_broadcasting(left_shape: Sequence[int], right_shape: Sequence[int]) -> bool:
    """Check whether two shapes can participate in broadcasting."""
    left = list(left_shape)
    right = list(right_shape)
    while left and right:
        if left[-1] == right[-1] or left[-1] == 1 or right[-1] == 1:
            left.pop()
            right.pop()
            continue
        return False
    return True


def apply_tensor_broadcast_addition(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> List[List[float]]:
    """Add a vector across each row of a matrix with shape validation."""
    matrix_shape = compute_tensor_shape(matrix)
    vector_shape = compute_tensor_shape(vector)
    if not validate_tensor_shapes_for_broadcasting(matrix_shape, vector_shape):
        raise ValueError("Incompatible shapes for broadcasting")
    return [[value + vector[index] for index, value in enumerate(row)] for row in matrix]


def compute_tensor_mean_value(tensor: Iterable) -> float:
    """Compute the mean value of all elements stored inside a tensor."""
    flat_values = []

    def flatten(values):
        if isinstance(values, (list, tuple)):
            for item in values:
                flatten(item)
        else:
            flat_values.append(float(values))

    flatten(tensor)
    return sum(flat_values) / len(flat_values) if flat_values else 0.0
