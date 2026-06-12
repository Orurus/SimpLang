# Tensor and Matrix Library for SimpLang ML Workflows

This library adds a small, readable tensor and matrix toolkit to SimpLang so experiments can start without depending on NumPy.

## Available helpers

- `new_matrix_with_zeros(rows, columns)`
- `new_matrix_with_ones(rows, columns)`
- `new_matrix_with_identity(size)`
- `new_matrix_with_random_values(rows, columns, minimum, maximum)`
- `new_tensor_with_zeros(shape)`
- `new_tensor_with_ones(shape)`
- `new_tensor_with_random_values(shape, minimum, maximum)`
- `add_matrix_to_matrix(left_matrix, right_matrix)`
- `multiply_matrix_by_matrix(left_matrix, right_matrix)`
- `compute_tensor_mean_value(tensor)`

## Example usage

```python
import tensor_matrix_library

weights = tensor_matrix_library.new_matrix_with_ones(2, 3)
identity = tensor_matrix_library.new_matrix_with_identity(3)
shape = [2, 2, 2]
features = tensor_matrix_library.new_tensor_with_zeros(shape)
```

## Design notes

The naming is intentionally extremely verbose so each function describes its behavior directly and remains easy to discover in larger ML scripts.