from unittest.mock import MagicMock

from expenditure_handlers import handler_amount, AMOUNT, DESCRIPTION, CURRENT_EXPENDITURES

TEST_USERNAME = "test"


def setup_module():
    CURRENT_EXPENDITURES["test"] = {}


def test_expenditure_handler_happy_path_numbers():
    # el handler_amount devuelve el próximo paso de la conversación
    # si no hay errores devuelve DESCRIPTION
    # si hay errores devuelve AMOUNT
    assert handler_amount(_get_update_with_string_amount("10"), None) == DESCRIPTION
    assert handler_amount(_get_update_with_string_amount("10,5"), None) == DESCRIPTION
    assert handler_amount(_get_update_with_string_amount("0,53"), None) == DESCRIPTION
    assert handler_amount(_get_update_with_string_amount("-10,53"), None) == DESCRIPTION
    assert handler_amount(_get_update_with_string_amount("-10,5"), None) == DESCRIPTION
    assert handler_amount(_get_update_with_string_amount("-10.5"), None) == DESCRIPTION
    assert handler_amount(_get_update_with_string_amount("10.5"), None) == DESCRIPTION
    assert handler_amount(_get_update_with_string_amount("0.5"), None) == DESCRIPTION


def test_expenditure_handler_non_numbers():
    # el handler_amount devuelve el próximo paso de la conversación
    # si no hay errores devuelve DESCRIPTION
    # si hay errores devuelve AMOUNT
    assert handler_amount(_get_update_with_string_amount("aa"), None) == AMOUNT
    assert handler_amount(_get_update_with_string_amount("10,5,5"), None) == AMOUNT
    assert handler_amount(_get_update_with_string_amount("0,ddd53"), None) == AMOUNT
    assert handler_amount(_get_update_with_string_amount("-11..4"), None) == AMOUNT
    assert handler_amount(_get_update_with_string_amount("-10%1"), None) == AMOUNT


def _get_update_with_string_amount(amount):
    update = MagicMock()
    effective_user = MagicMock()
    effective_user.username = TEST_USERNAME
    update.effective_user = effective_user
    message = MagicMock()
    message.text = amount
    update.message = message
    return update
