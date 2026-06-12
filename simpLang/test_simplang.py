"""Regression tests for SimpLang transpilation and the new tensor/matrix module."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from core.transpiler import transpile
from core.codegen import compile_simp_to_py


def test_transpiler_basic_keywords():
    assert transpile('say("Hello")') == 'print("Hello")'
    assert transpile('x = 5') == 'x = 5'
    assert transpile('name = ask("Name: ")') == 'name = input("Name: ")'


def test_transpiler_supports_indexed_assignment():
    assert transpile('w3[0] = 5') == 'w3[0] = 5'


def test_transpiler_supports_logical_symbols():
    assert transpile('if ready && hungry\n  say("go")\nend') == 'if ready and hungry:\n    print("go")\npass'
    assert transpile('if ready || tired\n  say("go")\nend') == 'if ready or tired:\n    print("go")\npass'


def test_compile_simp_to_py_supports_logical_operators_in_both_styles():
    english_code = compile_simp_to_py('if ready and hungry\n  say("go")\nend', '<test>')
    symbol_code = compile_simp_to_py('if ready && hungry\n  say("go")\nend', '<test>')
    symbol_or_code = compile_simp_to_py('if ready || tired\n  say("go")\nend', '<test>')

    assert 'ready and hungry' in english_code
    assert 'ready and hungry' in symbol_code
    assert 'ready or tired' in symbol_or_code


def test_compile_simp_to_py_supports_language_driven_comparisons():
    code = compile_simp_to_py('if guess is bigger than secret\n  say("hi")\nend', '<test>')
    assert 'guess > secret' in code

    code = compile_simp_to_py('if guess bigger than secret\n  say("hi")\nend', '<test>')
    assert 'guess > secret' in code

    code = compile_simp_to_py('if guess is bigger than secret\n  say("hi")\nend', '<test>')
    assert 'guess > secret' in code
    assert 'print("hi")' in code

    code = compile_simp_to_py('if guess is smaller secret\n  say("low")\nend', '<test>')
    assert 'guess < secret' in code

    code = compile_simp_to_py('if guess is bigger or equal to secret\n  say("hi")\nend', '<test>')
    assert 'guess >= secret' in code

    code = compile_simp_to_py('if guess is bigger and equal to secret\n  say("hi")\nend', '<test>')
    assert 'guess >= secret' in code

    code = compile_simp_to_py('if guess is equal to secret\n  say("match")\nend', '<test>')
    assert 'guess == secret' in code

    code = compile_simp_to_py('if guess is not equal to secret\n  say("nope")\nend', '<test>')
    assert 'guess != secret' in code


def test_compile_simp_to_py_rejects_chained_comparison_words():
    try:
        compile_simp_to_py('if x is bigger and smaller y\n  say("bad")\nend', '<test>')
    except Exception as exc:
        assert 'Unexpected token' in str(exc) or 'Expected' in str(exc)
    else:
        assert False, 'Expected invalid chained comparison words to fail'

    try:
        compile_simp_to_py('if x is bigger or smaller y\n  say("bad")\nend', '<test>')
    except Exception as exc:
        assert 'Unexpected token' in str(exc) or 'Expected' in str(exc)
    else:
        assert False, 'Expected chained comparison words to fail'


def test_compile_simp_to_py_bootstrap_includes_tensor_module_paths():
    code = compile_simp_to_py('import tensor_matrix_library', '<test>')
    assert 'sys.path.insert(0, _simp_src)' in code
    assert 'tensor_matrix_library' in code


def test_tensor_matrix_library_exports_verbose_helpers():
    import importlib

    module = importlib.import_module('modules.tensor_matrix_library')

    zeros = module.new_matrix_with_zeros(2, 2)
    ones = module.new_matrix_with_ones(2, 2)
    identity = module.new_matrix_with_identity(2)

    assert zeros == [[0, 0], [0, 0]]
    assert ones == [[1, 1], [1, 1]]
    assert identity == [[1, 0], [0, 1]]

    tensor = module.new_tensor_with_zeros([2, 2])
    assert tensor == [[0, 0], [0, 0]]


def test_custom_simp_module_imports_work_through_loader():
    from modules.loader import load_simp_module

    module = load_simp_module('myutils')

    assert module.double(4) == 8
    assert module.greet('Ada').startswith('Hello, Ada!')


def test_import_path_syntax_compiles_for_custom_modules():
    code = compile_simp_to_py('import /src/myutils.simp', '<test>')

    assert "load_simp_module('/src/myutils.simp')" in code


def test_import_example_executes_module_function():
    import pathlib

    source = pathlib.Path('examples/importtest.simp').read_text(encoding='utf-8')
    code = compile_simp_to_py(source, 'examples/importtest.simp')
    namespace = {}

    exec(compile(code, 'examples/importtest.simp', 'exec'), namespace)

    assert namespace['myutils'].factorial(4) == 24


def test_tensor_shape_and_broadcast_helpers():
    from modules.tensor_matrix_library import (
        apply_tensor_broadcast_addition,
        compute_tensor_shape,
        validate_tensor_shapes_for_broadcasting,
    )

    assert compute_tensor_shape([[1.0, 2.0], [3.0, 4.0]]) == [2, 2]
    assert validate_tensor_shapes_for_broadcasting([2, 2], [2]) is True
    assert apply_tensor_broadcast_addition([[1.0, 2.0], [3.0, 4.0]], [0.5, 0.5]) == [[1.5, 2.5], [3.5, 4.5]]


def test_scaled_dot_product_attention_is_row_wise():
    from modules.advanced_ml_library import create_scaled_dot_product_attention_matrix

    result = create_scaled_dot_product_attention_matrix(
        [[0.0, 0.0], [0.0, 0.0]],
        [[1.0, 0.0], [0.0, 1.0]],
        [[10.0, 0.0], [0.0, 1.0]],
    )

    assert result == [[5.0, 0.5], [5.0, 0.5]]


def test_optimizer_state_and_autograd_helpers_are_stateful():
    from modules.advanced_ml_library import (
        apply_optimizer_step_with_state,
        create_autograd_graph_node,
        create_optimizer_state_object,
    )

    state = create_optimizer_state_object('sgd', {'w': 1.0}, learning_rate=0.1)
    updated, next_state = apply_optimizer_step_with_state([[1.0]], [[0.5]], state)

    assert updated == [[0.95]]
    assert next_state['step'] == 1

    graph = create_autograd_graph_node('multiply', ['w', 'x'], gradient=1.0)
    assert graph['operation'] == 'multiply'
    assert graph['inputs'] == ['w', 'x']
    assert graph['gradient'] == 1.0


def test_tensor_object_and_training_loop_helpers():
    from modules.advanced_ml_library import (
        Tensor,
        create_training_loop_state,
        run_simple_training_loop_with_optimizer,
    )

    tensor = Tensor([[1.0, -2.0], [3.0, 0.0]])
    relu = tensor.relu()
    assert relu.shape == [2, 2]
    assert relu.to_list() == [[1.0, 0.0], [3.0, 0.0]]

    state = create_training_loop_state('demo', 'sgd', {'w': [[1.0]]}, learning_rate=0.1)
    result = run_simple_training_loop_with_optimizer([[1.0]], [[0.5]], state)

    assert result['optimizer_state']['step'] == 1
    assert result['history'][0]['step'] == 1
    assert result['weights'] == [[0.95]]


def test_advanced_ml_library_supports_layers_and_attention_helpers():
    import importlib

    module = importlib.import_module('modules.advanced_ml_library')

    layer = module.create_neural_network_layer_with_random_weights(2, 2)
    assert len(layer) == 2
    assert all(len(row) == 2 for row in layer)

    relu = module.apply_relu_activation_function([[-1.0, 0.0], [2.0, -3.0]])
    assert relu == [[0.0, 0.0], [2.0, 0.0]]

    softmax = module.apply_softmax_activation_function([1.0, 2.0])
    assert abs(sum(softmax) - 1.0) < 1e-9

    scores = module.create_attention_score_matrix([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]])
    assert len(scores) == 2 and len(scores[0]) == 2

    encoding = module.create_transformer_position_encoding(3, 4)
    assert len(encoding) == 3 and len(encoding[0]) == 4

    update = module.create_weight_update_using_error_signal([[1.0, 0.0]], [[0.5, 0.0]], 0.1)
    assert update == [[0.95, 0.0]]

    regularized = module.apply_weight_decay_regularization([[1.0, 2.0]], 0.1)
    assert regularized == [[0.9, 1.8]]

    batch = module.create_batch_of_input_vectors([[1.0, 2.0], [3.0, 4.0]])
    assert batch == [[1.0, 2.0], [3.0, 4.0]]

    state = module.create_tensor_state_object_with_shape_and_values([2, 2], [[1.0, 2.0], [3.0, 4.0]])
    assert state['shape'] == [2, 2]
    assert state['values'] == [[1.0, 2.0], [3.0, 4.0]]

    timestep = module.create_timestep_state_transition([[1.0, 1.0]], [[0.1, 0.1]], 0.5)
    assert timestep == [[1.05, 1.05]]

    broadcast = module.apply_simple_broadcasting_rule_to_matrix([[1.0, 2.0]], [0.5, 0.5])
    assert broadcast == [[1.5, 2.5]]

    node = module.create_computation_graph_node('multiply', ['W', 'X'])
    assert node['operation'] == 'multiply'
    assert node['inputs'] == ['W', 'X']

    gradient = module.create_simple_autograd_gradient_trace('multiply', 2.0)
    assert gradient['operation'] == 'multiply'
    assert gradient['gradient'] == 2.0

    module_state = module.create_reusable_model_module_container('demo_model', ['layer1'])
    assert module_state['model_name'] == 'demo_model'
    assert module_state['layers'] == ['layer1']