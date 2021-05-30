# imports
import src.bodgers as bodgers
import src.values as values
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

class Test_Run_Fettle:
    def test_nowt_fettle(self):
        res, error = bodgers.Gaffer.run('fettle doNowt gioer')
        result = get_values_in_python(res)
        assert type(result[0]) is values.Nowt
        assert error is None

        res, error = bodgers.Gaffer.run('doNowt')
        result = get_values_in_python(res)
        assert result == ["nowt"]
        assert error is None

    def test_normal_fettle(self):
        res, error = bodgers.Gaffer.run('fettle addUp(a, b : Number) : Number giz \n addUp := a + b \n oer')
        result = get_values_in_python(res)
        assert type(result[0]) is values.Nowt
        assert error is None

        res, error = bodgers.Gaffer.run('addUp(1,2)')
        result = get_values_in_python(res)
        assert result == [3]
        assert error is None

class Test_Built_In_Fettles:
    def test_run_built_in_fettles_gaffer(self):
        # - write()
        res, error = bodgers.Gaffer.run('write("eyup")')
        result = get_values_in_python(res)
        assert result == ["nowt"]
        assert error is None

        # -isNumber()
        res, error = bodgers.Gaffer.run('isNumber(2)')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('isNumber("2")')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        # -isScript()
        res, error = bodgers.Gaffer.run('isScript("test")')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('isScript(2)')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        # -isList()
        res, error = bodgers.Gaffer.run('isList([1,2,3])')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('isList(2)')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        # -isFettle()
        res, error = bodgers.Gaffer.run('isFettle(isLetter)')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('isFettle(2)')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        # -isLetter()
        res, error = bodgers.Gaffer.run('isLetter("t")')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('isLetter(2)')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        # -isBodger()
        res, error = bodgers.Gaffer.run('isBodger(missen)')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('isBodger(2)')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        # -isAnswer()
        res, error = bodgers.Gaffer.run('isAnswer(aye)')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('isAnswer(2)')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        # -toNumber(Script)
        res, error = bodgers.Gaffer.run('toNumber("2")')
        result = get_values_in_python(res)
        assert result == [2]
        assert error is None

        # -toScript(Number)
        res, error = bodgers.Gaffer.run('toScript(2)')
        result = get_values_in_python(res)
        assert result == ["2"]
        assert error is None

    def test_run_built_in_fettles_lists(self):
        # -add()
        res, error = bodgers.Gaffer.run('add([1,2,3], 4)')
        result = get_values_in_python(res)
        assert result == [[1,2,3,4]]
        assert error is None

        # -take()
        res, error = bodgers.Gaffer.run('take([1,2,3], 0)')
        result = get_values_in_python(res)
        assert result == [1]
        assert error is None

        # -has()
        res, error = bodgers.Gaffer.run('has([1,2,3], 0)')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        res, error = bodgers.Gaffer.run('has([1,2,3], 1)')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        # -hasOwt()
        res, error = bodgers.Gaffer.run('hasOwt([1,2,3])')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        res, error = bodgers.Gaffer.run('hasOwt([])')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None


        # -hasNowt()
        res, error = bodgers.Gaffer.run('hasNowt([1,2,3])')
        result = get_values_in_python(res)
        assert result == ["nay"]
        assert error is None

        res, error = bodgers.Gaffer.run('hasNowt([])')
        result = get_values_in_python(res)
        assert result == ["aye"]
        assert error is None

        # -addAll()
        res, error = bodgers.Gaffer.run('addAll([1,2,3], [4,5])')
        result = get_values_in_python(res)
        assert result == [[1,2,3,4,5]]
        assert error is None

        # -takeAll()
        res, error = bodgers.Gaffer.run('takeAll([1,2,3], [0,1])')
        result = get_values_in_python(res)
        assert result == [[1,2]]
        assert error is None

class Test_TrigMath:
    def test_trig_constants(self):
        # -pi
        res, error = bodgers.Gaffer.run('TrigMath.pi')
        result = get_values_in_python(res)
        assert result == [3.1415926535]
        assert error is None

        # -sin()
        res, error = bodgers.Gaffer.run('TrigMath.sin(0)')
        result = get_values_in_python(res)
        assert result == [0]
        assert error is None

        # -cos()
        res, error = bodgers.Gaffer.run('TrigMath.cos(0)')
        result = get_values_in_python(res)
        assert result == [1]
        assert error is None

        # -tan()
        res, error = bodgers.Gaffer.run('TrigMath.tan(0)')
        result = get_values_in_python(res)
        assert result == [0]
        assert error is None

        # -hypot()
        res, error = bodgers.Gaffer.run('TrigMath.hypot(3,4)')
        result = get_values_in_python(res)
        assert result == [5]
        assert error is None

        # -degrees()
        res, error = bodgers.Gaffer.run('TrigMath.degrees(0)')
        result = get_values_in_python(res)
        assert result == [0]
        assert error is None

        # -radians()
        res, error = bodgers.Gaffer.run('TrigMath.radians(0)')
        result = get_values_in_python(res)
        assert result == [0]
        assert error is None

        # -asin()
        res, error = bodgers.Gaffer.run('TrigMath.asin(0)')
        result = get_values_in_python(res)
        assert result == [0]
        assert error is None

        # -acos()
        res, error = bodgers.Gaffer.run('TrigMath.acos(0)')
        result = get_values_in_python(res)
        assert result == [1.5707963267948966]
        assert error is None

        # -atan()
        res, error = bodgers.Gaffer.run('TrigMath.atan(0)')
        result = get_values_in_python(res)
        assert result == [0]
        assert error is None

class Test_LogMath:
    def test_log_constants(self):
        # -e
        res, error = bodgers.Gaffer.run('LogMath.e')
        result = get_values_in_python(res)
        assert result == [2.7182818284]
        assert error is None

        # -log()
        res, error = bodgers.Gaffer.run('LogMath.log(LogMath.e)')
        result = get_values_in_python(res)
        assert result == [0.9999999999782784]
        assert error is None

        # -log2()
        res, error = bodgers.Gaffer.run('LogMath.log2(2)')
        result = get_values_in_python(res)
        assert result == [1]
        assert error is None

        # -log10()
        res, error = bodgers.Gaffer.run('LogMath.log10(10)')
        result = get_values_in_python(res)
        assert result == [1]
        assert error is None

        # -logBase()
        res, error = bodgers.Gaffer.run('LogMath.logBase(3,3)')
        result = get_values_in_python(res)
        assert result == [1]
        assert error is None

class Test_PolyMath:
     def test_poly_constants(self):
        # -sqrt()
        res, error = bodgers.Gaffer.run('PolyMath.sqrt(9)')
        result = get_values_in_python(res)
        assert result == [3]
        assert error is None

        # -pow()
        res, error = bodgers.Gaffer.run('PolyMath.pow(2,3)')
        result = get_values_in_python(res)
        assert result == [8]
        assert error is None

        # -maxiumum()
        res, error = bodgers.Gaffer.run('PolyMath.maximum(45,-9)')
        result = get_values_in_python(res)
        assert result == [45]
        assert error is None

        # -minimum()
        res, error = bodgers.Gaffer.run('PolyMath.minimum(-5, 4)')
        result = get_values_in_python(res)
        assert result == [-5]
        assert error is None
