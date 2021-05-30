# imports
import src.bodgers as bodgers
from src.errors import FlummoxedError, VexedError
import src.values as values

def get_values_in_python(list_vals):
    if not list_vals: return None

    new_list = []
    for element in list_vals.elements: 
        if isinstance(element, values.List):
            inner_list = []
            for elem in element.elements:
                inner_list.append(elem.value)
            new_list.append(inner_list)
        elif isinstance(element, values.BodgerVal):
            new_list.append(element.bodger)
        else:
            if not element: 
                return None
            else:
                new_list.append(element.value)

    return new_list

class Test_Run_Error:
    # parsing error 
    def test_run_vexed(self):
        res, error = bodgers.Gaffer.run('if x > 2')
        result = get_values_in_python(res)

        assert result is None
        assert type(error) is VexedError

        assert error.as_string() == "\nVexed: Weerz 'then'?\nproblem in Circle, line 1:\n\nif x > 2\n        ^"

    # token error 
    def test_run_token(self):
        res, error = bodgers.Gaffer.run('!')
        result = get_values_in_python(res)
        error.as_string()

        assert result is None
        assert type(error) is VexedError

    # interpreted error 
    def test_run_intertpreted(self):
        res, error = bodgers.Gaffer.run('x')
        result = get_values_in_python(res)
        error.as_string()

        assert result is None
        assert type(error) is FlummoxedError