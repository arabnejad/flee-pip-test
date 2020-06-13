import os
import sys
import subprocess


def test_with_fabflee():
    run_test("mali",50)


@fixture
def run_test(config,simulation_period):
    config_path = "%s/FabFlee/config_files/%s" % (
	    os.environ['TRAVIS_BUILD_DIR'], config)
    current_dir = os.getcwd()
    os.chdir(config_path)
    cmd = ["python3",
	"run.py",
	"input_csv",
	"source_data",
	simulation_period,
	"simsetting.csv",
	"> out.csv"
	]
    print(cmd)

    assert(subprocess.call(cmd) == 0)
    try:
        output = subprocess.check_output(cmd).decode("utf-8")
    except subprocess.CalledProcessError as e:
        assert("Command '%s' return non-zero exit status: %s" % (" ".join(cmd), e.returncode))
    #assert(output.find('success') >= 0)
    os.chdir(config_path)
