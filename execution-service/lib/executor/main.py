import os
from tempfile import TemporaryDirectory
from glob import glob

BASE_DIR = os.path.dirname(__file__)


def get_result(out: str, dirname: str) -> str:
    with open(dirname + "/error") as f:
        errors = f.read()

    with open(dirname + "/output") as f:
        output = f.read()

    with open(out) as f:
        expected = f.read()

    output = output.strip()

    if len(errors.strip()) == 0 and len(output) == 0:
        return 'TIMEOUT'
    elif output == expected:
        return 'PASS'
    elif len(errors.strip()) > 0:
        print(errors)
        return 'ERROR'
    else:
        return 'FAIL'


def run_test(in_file: str, out_file: str, script: str, language: str = 'PYTHON') -> str:
    with TemporaryDirectory() as dirname:
        if language == 'PYTHON':
            os.system(
                'cat "{0}" | timeout 7 python3 "{1}" > {2}/output 2> {2}/error'.format(in_file, script, dirname))
        elif language == 'C':
            os.system(
                'cat "{0}" | timeout 7 "{1}" > {2}/output 2> {2}/error'.format(in_file, script, dirname))
        return get_result(out_file, dirname)


def run_test_suite(tests_path: str, script: str, language: str = 'PYTHON') -> dict:
    results = {}
    with TemporaryDirectory() as temp_dir:
        if language == 'C':
            os.system(
                'gcc -x c "{0}" -o {1}/program_output'.format(script, temp_dir))
            script = temp_dir + '/program_output'

        for test in glob(tests_path + '/input/*'):
            out_file = test.replace('input', 'output')
            results[os.path.basename(test)] = run_test(
                test, out_file, script, language)

    return results
