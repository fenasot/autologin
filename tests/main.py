import pytest
import defaults.defaults as DF
from defaults.defaults import Readini


ini = Readini()
test_type = ini.get('commons', 'test_tpye')
test_case = ini.get('commons', 'test_case')
test_case_path = f'{DF.PATH_TESTS}\\{test_type}\\{test_case}'


def start():
    pytest.main([test_case_path])


start()
