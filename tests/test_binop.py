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

class Test_Run_BinaryOp:
    def test_run_simple_add(self):
        res, error = bodgers.Gaffer.run("1+1")
        result = get_values_in_python(res)
        
        assert result == [2]
        assert error is None

    def test_run_simple_minus(self):
        res, error = bodgers.Gaffer.run("1-1")
        result = get_values_in_python(res)
        
        assert result == [0]
        assert error is None

    def test_run_simple_mul(self):
        res, error = bodgers.Gaffer.run("2*2")
        result = get_values_in_python(res)
        
        assert result == [4]
        assert error is None

    def test_run_simple_div(self):
        res, error = bodgers.Gaffer.run("4/2")
        result = get_values_in_python(res)
        
        assert result == [2]
        assert error is None

    def test_run_simple_mod(self):
        res, error = bodgers.Gaffer.run("6%5")
        result = get_values_in_python(res)
        
        assert result == [1]
        assert error is None

    def test_run_simple_less_than(self):
        res, error = bodgers.Gaffer.run("1<1")
        result = get_values_in_python(res)
        
        assert result == ["nay"]
        assert error is None

    def test_run_simple_gt(self):
        res, error = bodgers.Gaffer.run("1>1")
        result = get_values_in_python(res)
        
        assert result == ["nay"]
        assert error is None

    def test_run_simple_less_than_eq(self):
        res, error = bodgers.Gaffer.run("1<=1")
        result = get_values_in_python(res)
        
        assert result == ["aye"]
        assert error is None

    def test_run_simple_gt_eq(self):
        res, error = bodgers.Gaffer.run("1>=1")
        result = get_values_in_python(res)
        
        assert result == ["aye"]
        assert error is None

    def test_run_simple_concat(self):
        res, error = bodgers.Gaffer.run('"TES" $ "T"')
        result = get_values_in_python(res)
        
        assert result == ["TEST"]
        assert error is None

        res, error = bodgers.Gaffer.run('"TES" $ "TT"')
        result = get_values_in_python(res)
        
        assert result == ["TESTT"]
        assert error is None

    def test_run_mul_concat(self):
        res, error = bodgers.Gaffer.run('"TEST"*2')
        result = get_values_in_python(res)
        
        assert result == ["TESTTEST"]
        assert error is None
    
    def test_run_list(self):
        res, error = bodgers.Gaffer.run('[1,2,3] + 4')
        result = get_values_in_python(res)
        
        assert result == [[1,2,3,4]]
        assert error is None

        res, error = bodgers.Gaffer.run('[1,2,3] - 0')
        result = get_values_in_python(res)
        
        assert result == [[2,3]]
        assert error is None

        res, error = bodgers.Gaffer.run('[1,2,3] * [1,2,3]')
        result = get_values_in_python(res)
        
        assert result == [[1,2,3,1,2,3]]
        assert error is None