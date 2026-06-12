"""An expansive, verbose ML helper library for SimpLang.

This module is intentionally designed to feel approachable like PyTorch,
while keeping every function name explicit and easy to read.
"""

import math
import random
from copy import deepcopy

from modules.tensor_matrix_library import (
    apply_tensor_broadcast_addition,
    compute_tensor_shape,
    new_matrix_with_ones,
    new_matrix_with_random_values,
    new_matrix_with_zeros,
    new_tensor_with_random_values,
    multiply_matrix_by_matrix,
    validate_tensor_shapes_for_broadcasting,
)


class Tensor:
    """Minimal tensor wrapper that carries shape metadata, values, and optional grad state."""

    def __init__(self, data, name: str = 'tensor', grad=None):
        self.data = deepcopy(data)
        self.shape = compute_tensor_shape(self.data)
        self.name = name
        self.grad = grad
        self.history = []

    def to_list(self):
        return deepcopy(self.data)

    def relu(self):
        return Tensor([[0.0 if value < 0.0 else value for value in row] for row in self.data], name=f'{self.name}.relu')

    def matmul(self, other):
        if not isinstance(other, Tensor):
            other = Tensor(other)
        result = [[sum(left * right for left, right in zip(row_left, row_right))
                   for row_right in zip(*other.data)]
                  for row_left in self.data]
        return Tensor(result, name=f'{self.name}.matmul')

    def softmax(self):
        flat = [value for row in self.data for value in row] if self.shape and len(self.shape) == 2 else [float(v) for v in self.data]
        max_value = max(flat)
        exponentials = [math.exp(value - max_value) for value in flat]
        total = sum(exponentials) or 1.0
        values = [value / total for value in exponentials]
        if self.shape and len(self.shape) == 2:
            return Tensor([values[index:index + self.shape[1]] for index in range(0, len(values), self.shape[1])], name=f'{self.name}.softmax')
        return Tensor(values, name=f'{self.name}.softmax')


def create_neural_network_layer_with_random_weights(rows: int, columns: int):
    """Create a new neural network layer matrix filled with random weights."""
    return new_matrix_with_random_values(rows, columns, -0.1, 0.1)


def create_neural_network_layer_with_zeros(rows: int, columns: int):
    """Create a new neural network layer matrix filled with zeros."""
    return new_matrix_with_zeros(rows, columns)


def create_neural_network_layer_with_ones(rows: int, columns: int):
    """Create a new neural network layer matrix filled with ones."""
    return new_matrix_with_ones(rows, columns)


def apply_relu_activation_function(matrix):
    """Apply the ReLU activation function element by element."""
    return [[0.0 if value < 0.0 else value for value in row] for row in matrix]


def apply_sigmoid_activation_function(matrix):
    """Apply the sigmoid activation function element by element."""
    result = []
    for row in matrix:
        result_row = []
        for value in row:
            exponent = math.exp(-value)
            result_row.append(1.0 / (1.0 + exponent))
        result.append(result_row)
    return result


def apply_softmax_activation_function(vector):
    """Apply the softmax activation function to a vector."""
    max_value = max(vector)
    exponentials = [math.exp(value - max_value) for value in vector]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def create_attention_score_matrix(query_matrix, key_matrix):
    """Create a simple attention score matrix from query and key matrices."""
    return multiply_matrix_by_matrix(query_matrix, key_matrix)


def create_transformer_position_encoding(sequence_length: int, embedding_size: int):
    """Create a simple sinusoidal positional encoding matrix for transformers."""
    encoding = new_matrix_with_zeros(sequence_length, embedding_size)
    for position in range(sequence_length):
        for dimension in range(embedding_size):
            if dimension % 2 == 0:
                encoding[position][dimension] = math.sin(position / (10000 ** (dimension / embedding_size)))
            else:
                encoding[position][dimension] = math.cos(position / (10000 ** ((dimension - 1) / embedding_size)))
    return encoding


def create_simple_snn_neuron_output(input_values):
    """Create a simple spiking neural network neuron output from input values."""
    return [1.0 if value > 0.0 else 0.0 for value in input_values]


def create_simple_transformer_feed_forward_layer(input_vector):
    """Create a simple feed-forward transform for transformer-style layers."""
    return [value * 2.0 for value in input_vector]


def create_simple_language_model_token_embedding(vocabulary_size: int, embedding_size: int):
    """Create a simple token embedding matrix for language model experiments."""
    return new_matrix_with_random_values(vocabulary_size, embedding_size, -0.05, 0.05)


def create_neural_network_bias_vector(size: int):
    """Create a new bias vector filled with zeros for a neural network layer."""
    return [0.0 for _ in range(size)]


def apply_tanh_activation_function(matrix):
    """Apply the hyperbolic tangent activation function element by element."""
    result = []
    for row in matrix:
        result.append([math.tanh(value) for value in row])
    return result


def apply_leaky_relu_activation_function(matrix, negative_slope: float = 0.01):
    """Apply the leaky ReLU activation function element by element."""
    return [[value if value >= 0.0 else negative_slope * value for value in row] for row in matrix]


def compute_mean_squared_error(predicted_matrix, target_matrix):
    """Compute the mean squared error between predicted values and target values."""
    total = 0.0
    count = 0
    for row_pred, row_target in zip(predicted_matrix, target_matrix):
        for value_pred, value_target in zip(row_pred, row_target):
            total += (value_pred - value_target) ** 2
            count += 1
    return total / count if count else 0.0


def compute_binary_cross_entropy_loss(predicted_matrix, target_matrix):
    """Compute the binary cross entropy loss for probability-style predictions."""
    total = 0.0
    count = 0
    for row_pred, row_target in zip(predicted_matrix, target_matrix):
        for value_pred, value_target in zip(row_pred, row_target):
            eps = 1e-7
            clipped = min(max(value_pred, eps), 1.0 - eps)
            total += -(value_target * math.log(clipped) + (1.0 - value_target) * math.log(1.0 - clipped))
            count += 1
    return total / count if count else 0.0


def apply_layer_normalization_vector(vector):
    """Apply a simple layer normalization step to a vector of values."""
    mean_value = sum(vector) / len(vector) if vector else 0.0
    variance = sum((value - mean_value) ** 2 for value in vector) / len(vector) if vector else 0.0
    std_value = math.sqrt(variance)
    return [(value - mean_value) / (std_value + 1e-6) for value in vector]


def create_dropout_mask_vector(vector, dropout_rate: float = 0.1):
    """Create a binary dropout mask for a vector of values."""
    return [0.0 if random.random() < dropout_rate else 1.0 for _ in vector]


def create_residual_connection_matrix(primary_matrix, residual_matrix):
    """Create a residual connection by adding a primary pathway to its residual pathway."""
    return [[left + right for left, right in zip(left_row, right_row)]
            for left_row, right_row in zip(primary_matrix, residual_matrix)]


def create_scaled_dot_product_attention_matrix(query_matrix, key_matrix, value_matrix):
    """Create row-wise scaled dot-product attention using real query/key/value semantics."""
    query_shape = compute_tensor_shape(query_matrix)
    key_shape = compute_tensor_shape(key_matrix)
    value_shape = compute_tensor_shape(value_matrix)

    if len(query_shape) != 2 or len(key_shape) != 2 or len(value_shape) != 2:
        raise ValueError("Attention inputs must be 2D matrices")
    if query_shape[1] != key_shape[0]:
        raise ValueError("Query and key dimensions are incompatible")
    if key_shape[0] != value_shape[0]:
        raise ValueError("Key and value sequence lengths must match")

    scores = []
    for query_row in query_matrix:
        row_scores = []
        for key_row in key_matrix:
            score = sum(q * k for q, k in zip(query_row, key_row))
            row_scores.append(score)
        scores.append(row_scores)

    scale_factor = 1.0 / math.sqrt(len(query_matrix[0]) if query_matrix else 1)
    scaled_scores = [[value * scale_factor for value in row] for row in scores]

    attention_rows = []
    for row in scaled_scores:
        weights = apply_softmax_activation_function(row)
        weighted_values = [sum(weight * value for weight, value in zip(weights, column_values))
                           for column_values in zip(*value_matrix)]
        attention_rows.append(weighted_values)

    return attention_rows


def create_simple_transformer_block_output(input_matrix):
    """Create a simple transformer-style block output from an input matrix."""
    return [[value * 1.1 for value in row] for row in input_matrix]


def create_spiking_neuron_threshold_output(input_values, threshold: float = 0.5):
    """Create a spiking neural network output by thresholding input values."""
    return [1.0 if value >= threshold else 0.0 for value in input_values]


def create_simple_language_model_context_window(token_ids, window_size: int):
    """Create a simple context window slice for language model experiments."""
    return token_ids[:window_size]


def create_weight_update_using_error_signal(weights, targets, learning_rate: float = 0.01):
    """Create a simple weight update using an error signal and learning rate."""
    return [[weight - learning_rate * (weight - target) for weight, target in zip(row_weights, row_targets)]
            for row_weights, row_targets in zip(weights, targets)]


def apply_weight_decay_regularization(weights, decay_rate: float = 0.01):
    """Apply weight decay regularization to reduce large parameter values."""
    return [[value * (1.0 - decay_rate) for value in row] for row in weights]


def create_batch_of_input_vectors(batch_input_vectors):
    """Create a batch of input vectors for mini-batch style processing."""
    return [list(row) for row in batch_input_vectors]


def apply_value_clipping_to_matrix(matrix, lower_bound: float = -10.0, upper_bound: float = 10.0):
    """Clip all values in a matrix to safe numeric bounds."""
    return [[max(lower_bound, min(upper_bound, value)) for value in row] for row in matrix]


def apply_safe_division_operation(numerator, denominator, epsilon: float = 1e-8):
    """Perform safe division by guarding against zero denominators."""
    return numerator / (denominator + epsilon)


def create_hebbian_learning_update(matrix, activation_vector):
    """Create a simple Hebbian learning update using a correlation-style rule."""
    return [[value * activation for activation in activation_vector] for value in matrix]


def create_gradient_descent_optimization_step(weights, gradients, learning_rate: float = 0.01):
    """Create a simple gradient descent optimization step for parameter updates."""
    return [[weight - learning_rate * gradient for weight, gradient in zip(row_weights, row_gradients)]
            for row_weights, row_gradients in zip(weights, gradients)]


def create_momentum_optimization_step(weights, gradients, velocity, learning_rate: float = 0.01, momentum_rate: float = 0.9):
    """Create a simple momentum-based optimization step for smoother training."""
    updated_velocity = [[momentum_rate * vel + learning_rate * grad for vel, grad in zip(row_velocity, row_gradients)]
                        for row_velocity, row_gradients in zip(velocity, gradients)]
    updated_weights = [[weight - step for weight, step in zip(row_weights, row_velocity)]
                       for row_weights, row_velocity in zip(weights, updated_velocity)]
    return updated_weights, updated_velocity


def create_simple_model_state_dictionary(model_name: str, parameter_count: int):
    """Create a simple dictionary-like model state object for a named model."""
    return {"model_name": model_name, "parameter_count": parameter_count, "ready": True}


def create_tensor_state_object_with_shape_and_values(shape, values):
    """Create a persistent tensor state object that tracks shape and current values."""
    return {"shape": list(shape), "values": [list(row) for row in values], "persistent": True}


def create_timestep_state_transition(current_state, delta_state, timestep_factor: float = 1.0):
    """Create a simple timestep-based state transition using current state and deltas."""
    return [[value + timestep_factor * delta for value, delta in zip(row_values, row_deltas)]
            for row_values, row_deltas in zip(current_state, delta_state)]


def apply_simple_broadcasting_rule_to_matrix(matrix, vector):
    """Apply a simple broadcasting rule by adding a vector across each row of a matrix."""
    return apply_tensor_broadcast_addition(matrix, vector)


def create_computation_graph_node(operation_name: str, input_names):
    """Create a simple computation graph node that records an operation and its inputs."""
    return {"operation": operation_name, "inputs": list(input_names), "output": None}


def create_simple_autograd_gradient_trace(operation_name: str, gradient_value: float):
    """Create a simple autograd-style gradient trace record for a computation step."""
    return {"operation": operation_name, "gradient": gradient_value}


def create_autograd_graph_node(operation_name: str, input_names, gradient: float = None):
    """Create an autograd-style graph node with dependency metadata and gradient state."""
    return {"operation": operation_name, "inputs": list(input_names), "gradient": gradient, "backward": False}


def record_tensor_operation_in_graph(operation_name: str, inputs, output_tensor):
    """Record a simple graph edge for tensor operations so the graph becomes automatic."""
    return create_autograd_graph_node(operation_name, list(inputs), gradient=getattr(output_tensor, 'grad', None))


def create_reusable_model_module_container(model_name: str, layers):
    """Create a reusable model module container that groups model layers under one name."""
    return {"model_name": model_name, "layers": list(layers), "composition": True}


def create_optimizer_state_object(optimizer_name: str, parameters, learning_rate: float = 0.01):
    """Create a stateful optimizer object for training loops."""
    return {
        "optimizer": optimizer_name,
        "parameters": dict(parameters),
        "learning_rate": learning_rate,
        "velocity": {},
        "step": 0,
    }


def apply_optimizer_step_with_state(weights, gradients, optimizer_state):
    """Apply a simple SGD update and return the new weights plus updated optimizer state."""
    updated_weights = [[weight - optimizer_state['learning_rate'] * gradient
                        for weight, gradient in zip(row_weights, row_gradients)]
                       for row_weights, row_gradients in zip(weights, gradients)]
    optimizer_state = dict(optimizer_state)
    optimizer_state['step'] = optimizer_state.get('step', 0) + 1
    optimizer_state['parameters'] = {'w': updated_weights}
    optimizer_state['history'] = optimizer_state.get('history', []) + [{'step': optimizer_state['step'], 'weights': updated_weights}]
    return updated_weights, optimizer_state


def create_training_loop_state(model_name: str, optimizer_name: str, parameters, learning_rate: float = 0.01):
    """Create a simple training-loop state object with optimizer metadata and history."""
    return {
        'model_name': model_name,
        'optimizer_name': optimizer_name,
        'optimizer_state': create_optimizer_state_object(optimizer_name, parameters, learning_rate),
        'history': [],
    }


def run_simple_training_loop_with_optimizer(weights, gradients, training_state):
    """Run one simple training step through the optimizer abstraction and record the history."""
    updated_weights, optimizer_state = apply_optimizer_step_with_state(weights, gradients, training_state['optimizer_state'])
    training_state = dict(training_state)
    training_state['optimizer_state'] = optimizer_state
    training_state['history'] = training_state.get('history', []) + [{'step': optimizer_state['step'], 'weights': updated_weights}]
    training_state['weights'] = updated_weights
    return training_state

