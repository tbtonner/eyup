# imports
import src.bodgers as bodgers
from src.errors import FlummoxedError, VexedError
import src.values as values

class Test_Run_Error:
    # parsing error 
    def test_run_vexed(self):
        res, error = bodgers.Gaffer.run('if x > 2')

        assert res is None
        assert type(error) is VexedError

        assert error.as_string() == "\nVexed: Weerz 'then'?\nproblem in Circle, line 1:\n\nif x > 2\n        ^"

    # token error 
    def test_run_token(self):
        res, error = bodgers.Gaffer.run('!')
        error.as_string()

        assert res is None
        assert type(error) is VexedError

    # interpreted error 
    def test_run_intertpreted(self):
        res, error = bodgers.Gaffer.run('x')
        error.as_string()

        assert res is None
        assert type(error) is FlummoxedError