from examples.basic import controller as basic_controller
from examples.basic_against_interface import controller as basic_against_interface_controller
from examples.decorator import my_handler
from examples.enforced_parameters import controller as enforced_parameters_controller


def test_basic():
    assert basic_controller.handler(1) == 2


def test_basic():
    assert basic_against_interface_controller.handler(1) == 2


def test_enforced_parameters():
    assert enforced_parameters_controller.handler(1) == 2


def test_decorator():
    assert my_handler(1) == 2
