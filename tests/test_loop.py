# imports
import src.bodgers as bodgers
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

class Test_Run_Loops:
    def test_run_while(self):
        res, error = bodgers.Gaffer.run('summat x := 2')
        res, error = bodgers.Gaffer.run('while x > 2 gowon \n x := x + 1 \n oer')
        result = get_values_in_python(res)
        assert result == None
        assert error is None

        res, error = bodgers.Gaffer.run('x')
        result = get_values_in_python(res)
        assert result == [3]
        assert error is None

    def test_run_gowon(self):
        res, error = bodgers.Gaffer.run('summat x := 2')
        res, error = bodgers.Gaffer.run('gowon x := x + 1 while x > 2 oer')
        result = get_values_in_python(res)
        assert result == None
        assert error is None

        res, error = bodgers.Gaffer.run('x')
        result = get_values_in_python(res)
        assert result == [3]
        assert error is None