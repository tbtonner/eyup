# imports
from src.shell import start_multiline, end_multiline

# testing start_multiline() method in shell
class Test_Start_Multiline:
    def test_non_multiline(self):
        assert not start_multiline("Gaffer")

    def test_if_multiline(self):
        assert start_multiline("if")

    def test_giz_multiline(self):
        assert start_multiline("giz")

    def test_giz_multiline(self):
        assert start_multiline("gowon")

    def test_giz_multiline(self):
        assert start_multiline("while")

    def test_if_oer_multiline(self):
        assert not start_multiline("if oer")

    def test_empty(self):
        assert not start_multiline("")

# testing end_multiline() method in shell
class Test_End_Multiline:
    def test_dont_end(self):
        assert not end_multiline("Gaffer")
    
    def test_end(self):
        assert end_multiline("Gaffer oer")

    def test_oer_wrong_pos(self):
        assert not end_multiline("Gaffer oer t")
    
    def test_empty(self):
        assert not end_multiline("")