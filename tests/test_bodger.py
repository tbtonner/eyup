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

class Test_Run_Bodger:
    def test_bodger(self):
        res, error = bodgers.Gaffer.run('eyup TrigMath')
        result = get_values_in_python(res)
        current_bodger = bodgers.CURRENT_BODGER

        assert current_bodger == bodgers.TrigMath
        assert result is None
        assert error is None

    def test_create_bodger_circle(self):
        res, error = bodgers.Gaffer.run('bodger Circle')
        result = get_values_in_python(res)
        assert result is None
        assert error is None

        res, error = bodgers.Gaffer.run('eyup Circle')
        result = get_values_in_python(res)
        assert result is None
        assert error is None
        current_bodger = bodgers.CURRENT_BODGER
        assert current_bodger.name == "Circle"

        res, error = current_bodger.run('summat r := 2')
        result = get_values_in_python(res)
        assert result == [2]
        assert error is None
        
        res, error = bodgers.Gaffer.run('Circle.r')
        result = get_values_in_python(res)
        assert result == [2]
        assert error is None