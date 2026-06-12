# Advanced ML Library for SimpLang

This document describes the next major upgrade for the SimpLang ML toolkit. The goal is to move from simple imperative calculations toward a richer AI-style computation model that is still readable and intentionally verbose.

## Current upgrade status

The ML helper library now includes real upgrades beyond the original toy helpers:

- tensor shape inference and broadcast compatibility checks
- safe broadcasted addition for matrix/vector style operations
- row-wise scaled dot-product attention with query/key/value semantics
- stateful optimizer objects and SGD step updates
- autograd-style graph nodes with gradient metadata
- reusable model containers and tensor state objects
- clipping, safe division, normalization, residual, loss, and batch helpers

These changes move the library from "matrix utilities" toward a more tensor-aware and training-oriented toolkit.

---

## Remaining roadmap items still to build

The following pieces are still future work beyond the current upgrade:

1. A true autograd engine with real backward propagation and dependency graphs
2. A real tensor class with slicing, full broadcasting, and dtype/shape enforcement
3. A full training loop with learning-rate scheduling and parameter binding
4. A true SNN time model with decay, event spikes, and continuous accumulation
5. A deeper transformer and LLM module system that behaves like a real model stack
6. First-class batch execution and model composition inside the language runtime

---

## Function reference for the implemented advanced ML helpers

The current advanced ML helper module contains the following explicit functions:

### Layer and parameter creation helpers
- `create_neural_network_layer_with_random_weights(rows, columns)` creates a weight matrix filled with small random values for a neural layer.
- `create_neural_network_layer_with_zeros(rows, columns)` creates a weight matrix filled with zeros for stable initialization.
- `create_neural_network_layer_with_ones(rows, columns)` creates a weight matrix filled with ones for simple prototype experiments.
- `create_neural_network_bias_vector(size)` creates a bias vector initialized to zero.
- `create_simple_model_state_dictionary(model_name, parameter_count)` creates a simple dictionary-style model state object for a named model.

### Activation helpers
- `apply_relu_activation_function(matrix)` applies the ReLU activation function element by element.
- `apply_sigmoid_activation_function(matrix)` applies the sigmoid activation function element by element.
- `apply_tanh_activation_function(matrix)` applies the hyperbolic tangent activation function.
- `apply_leaky_relu_activation_function(matrix, negative_slope)` applies the leaky ReLU activation function with a small negative slope.
- `apply_softmax_activation_function(vector)` converts a vector into a probability distribution using the softmax rule.

### Attention and transformer helpers
- `create_attention_score_matrix(query_matrix, key_matrix)` creates a basic attention score matrix using matrix multiplication.
- `create_scaled_dot_product_attention_matrix(query_matrix, key_matrix, value_matrix)` creates row-wise scaled dot-product attention using real query/key/value semantics.
- `create_transformer_position_encoding(sequence_length, embedding_size)` creates sinusoidal positional encodings for transformer-style input sequences.
- `create_simple_transformer_feed_forward_layer(input_vector)` applies a simple feed-forward scaling transform.
- `create_simple_transformer_block_output(input_matrix)` produces a simple transformer-like block output by scaling values.

### SNN and time-based helpers
- `create_simple_snn_neuron_output(input_values)` converts inputs into a simple binary spiking output signal.
- `create_spiking_neuron_threshold_output(input_values, threshold)` creates a threshold-based spike output for spiking neural network experiments.

### Loss and learning helpers
- `compute_mean_squared_error(predicted_matrix, target_matrix)` computes the average squared difference between predictions and targets.
- `compute_binary_cross_entropy_loss(predicted_matrix, target_matrix)` computes a stable binary cross-entropy loss for probability-like outputs.
- `create_weight_update_using_error_signal(weights, targets, learning_rate)` creates a simple error-driven weight update.
- `apply_weight_decay_regularization(weights, decay_rate)` applies weight decay to reduce large parameter values.
- `create_hebbian_learning_update(matrix, activation_vector)` creates a simple correlation-based Hebbian update.
- `create_gradient_descent_optimization_step(weights, gradients, learning_rate)` creates a simple gradient descent update.
- `create_momentum_optimization_step(weights, gradients, velocity, learning_rate, momentum_rate)` creates a momentum-based optimizer step.
- `create_optimizer_state_object(optimizer_name, parameters, learning_rate)` creates a stateful optimizer object for training loops.
- `apply_optimizer_step_with_state(weights, gradients, optimizer_state)` applies an SGD-style update and returns the updated weights plus optimizer state.

### Stability and numerical helpers
- `apply_value_clipping_to_matrix(matrix, lower_bound, upper_bound)` clips matrix values into safe numeric bounds.
- `apply_safe_division_operation(numerator, denominator, epsilon)` performs safe division while guarding against division by zero.
- `apply_layer_normalization_vector(vector)` normalizes a vector by subtracting its mean and dividing by its standard deviation.

### Batch and composition helpers
- `create_batch_of_input_vectors(batch_input_vectors)` creates a batch of vectors for mini-batch style processing.
- `create_dropout_mask_vector(vector, dropout_rate)` creates a binary mask for dropout-style regularization.
- `create_residual_connection_matrix(primary_matrix, residual_matrix)` creates a residual connection by adding the main pathway and the shortcut pathway.
- `create_scaled_dot_product_attention_matrix(query_matrix, key_matrix, value_matrix)` creates a scaled attention result matrix using the query, key, and value pathways.
- `create_simple_language_model_token_embedding(vocabulary_size, embedding_size)` creates a simple token embedding matrix for language model experiments.
- `create_simple_language_model_context_window(token_ids, window_size)` creates a simple context window slice for token sequence experiments.
- `create_tensor_state_object_with_shape_and_values(shape, values)` creates a persistent tensor state object with explicit shape and value tracking.
- `create_timestep_state_transition(current_state, delta_state, timestep_factor)` creates a timestep-based state evolution rule for dynamic models.
- `apply_simple_broadcasting_rule_to_matrix(matrix, vector)` applies a broadcast-compatible matrix/vector addition.
- `compute_tensor_shape(tensor)` infers the tensor shape of a nested structure.
- `validate_tensor_shapes_for_broadcasting(left_shape, right_shape)` checks whether two shapes are broadcast-compatible.
- `apply_tensor_broadcast_addition(matrix, vector)` safely adds a vector across each row of a matrix using shape validation.
- `create_computation_graph_node(operation_name, input_names)` records a computation graph node with its operation and inputs.
- `create_autograd_graph_node(operation_name, input_names, gradient)` creates an autograd-style graph node with gradient metadata.
- `create_simple_autograd_gradient_trace(operation_name, gradient_value)` records a simple autograd-style gradient trace.
- `create_reusable_model_module_container(model_name, layers)` groups reusable model layers into a single module container.

## Summary

The current vision is:
- tensors with real shape inference and broadcast validation
- matrix and tensor primitives as core operations
- learning rules, optimizer state, and loss functions
- graph tracking and autograd-style gradient metadata
- time-aware SNN behavior
- reusable modules and model objects

This gives SimpLang a more credible, readable ML foundation while still keeping the system approachable for educational and experimental use.

This gives SimpLang a real path toward readable, understandable AI and ML systems without losing its simple style.
