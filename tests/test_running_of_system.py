# imports
import src.bodgers as bodgers
import src.values as values
from src.errors import FlummoxedError
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

class Test_Run_Basic:
    # summat
    def test_run_summat(self):
        gaffer_context = bodgers.Context("Gaffer")
        gaffer_context.symbol_table = bodgers.SymbolTable(bodgers.global_symbol_table.copySymbols())
        newGaffer = bodgers.Bodger("Gaffer", gaffer_context)

        newGaffer.run("summat x := 2")
        res, error = newGaffer.run("x")
        result = get_values_in_python(res)

        assert result == [2]
        assert error is None

    def test_run_summat_val(self):
        gaffer_context = bodgers.Context("Gaffer")
        gaffer_context.symbol_table = bodgers.SymbolTable(bodgers.global_symbol_table.copySymbols())
        newGaffer = bodgers.Bodger("Gaffer", gaffer_context)

        newGaffer.run("summat x := 2")
        res, error = newGaffer.run("x + 2")
        result = get_values_in_python(res)

        assert result == [4]
        assert error is None

        res, error = newGaffer.run("forget x")
        res, error = newGaffer.run("x")
        result = get_values_in_python(res)
        assert result is None
        assert type(error) is FlummoxedError

    # nowt
    def test_run_nowt(self):
        res, error = bodgers.Gaffer.run("nowt")
        result = get_values_in_python(res)

        assert result == ["nowt"]
        assert error is None

    # number
    def test_run_number(self):
        res, error = bodgers.Gaffer.run("1+1")
        result = get_values_in_python(res)

        assert result == [2]
        assert error is None

    # answer
    def test_run_answer_aye(self):
        res, error = bodgers.Gaffer.run("aye")
        result = get_values_in_python(res)

        assert result == ["aye"]
        assert error is None

    def test_run_answer_nay(self):
        res, error = bodgers.Gaffer.run("nay")
        result = get_values_in_python(res)

        assert result == ["nay"]
        assert error is None

    def test_run_answer_aye_expr(self):
        res, error = bodgers.Gaffer.run("1=1")
        result = get_values_in_python(res)

        assert result == ["aye"]
        assert error is None

    def test_run_answer_nay_expr(self):
        res, error = bodgers.Gaffer.run("1=2")
        result = get_values_in_python(res)

        assert result == ["nay"]
        assert error is None

    # script
    def test_run_script(self):
        res, error = bodgers.Gaffer.run('"TEST"')
        result = get_values_in_python(res)

        assert result == ["TEST"]
        assert error is None

    # letter
    def test_run_letter(self):
        res, error = bodgers.Gaffer.run('"T"')
        result = get_values_in_python(res)

        assert result == ["T"]
        assert error is None

    # list
    def test_run_letter(self):
        res, error = bodgers.Gaffer.run('[1,2,3]')
        result = get_values_in_python(res)

        assert result == [[1,2,3]]
        assert error is None

    # allus
    def test_run_allus(self):
        gaffer_context = bodgers.Context("Gaffer")
        gaffer_context.symbol_table = bodgers.SymbolTable(bodgers.global_symbol_table.copySymbols())
        newGaffer = bodgers.Bodger("Gaffer", gaffer_context)

        res, error = newGaffer.run('summat x := allus 123')
        result = res.elements[0].token.value

        assert result == 123
        assert error is None

    # sithee
    def test_run_sithee_trig(self):
        bodgers.CURRENT_BODGER = bodgers.TrigMath
        res, error = bodgers.TrigMath.run("sithee")
        result = res.elements[0]

        assert result is None
        assert error is None

    # missen
    def test_run_missen_gaffer(self):
        res, error = bodgers.Gaffer.run("missen")
        result = get_values_in_python(res)

        assert result == [bodgers.Gaffer]
        assert error is None

    def test_run_missen_trig(self):
        bodgers.CURRENT_BODGER = bodgers.TrigMath
        res, error = bodgers.TrigMath.run("missen")
        result = get_values_in_python(res)

        assert result == [bodgers.TrigMath]
        assert error is None

    # gander
    def test_run_gander(self):
        res, error = bodgers.Gaffer.run("gander")
        result = get_values_in_python(res)

        assert result is None
        assert error is None

    def test_run_unknown_gander(self):
        res, error = bodgers.Gaffer.run("gander waffer")
        result = get_values_in_python(res)

        assert result is None
        assert type(error) is FlummoxedError

    # wang
    def test_run_wang_aye(self):
        res, error = bodgers.Gaffer.run("wang 1=1")
        result = get_values_in_python(res)

        assert result is None
        assert type(error) is FlummoxedError

    def test_run_wang_aye(self):
        res, error = bodgers.Gaffer.run("wang 1=2")
        result = get_values_in_python(res)

        assert result is None
        assert error is None

    def test_run_wang_answer(self):
        res, error = bodgers.Gaffer.run("wang nay")
        result = get_values_in_python(res)

        assert result is None
        assert error is None

    # unary op
    def test_run_simple_minus(self):
        res, error = bodgers.Gaffer.run("-1")
        result = get_values_in_python(res)

        assert result == [-1]
        assert error is None

    def test_unary_op_node_not_num(self):
        res, error = bodgers.Gaffer.run("-test")
        result = get_values_in_python(res)

        assert result is None
        assert type(error) is FlummoxedError


    def test_run_unary_not(self):
        res, error = bodgers.Gaffer.run("not aye")
        result = get_values_in_python(res)

        assert result == ["nay"]
        assert error is None
