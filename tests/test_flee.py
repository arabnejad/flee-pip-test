import os
import sys
import subprocess


def test_fabflee_mali():
    config_path = "%s/FabFlee/config_files/%s" % (
	    os.environ['TRAVIS_BUILD_DIR'], "mali")
    current_dir = os.getcwd()
    os.chdir(config_path)
    cmd = ["python3",
	"run.py",
	"input_csv",
	"source_data",
	"50",
	"simsetting.csv",
	"> out.csv"
	]
    print(cmd)

    assert(subprocess.call(cmd) == 0)
    output = subprocess.check_output(cmd).decode("utf-8")
    except subprocess.CalledProcessError as e:
        assert("Command '%s' return non-zero exit status: %s" % (" ".join(cmd), e.returncode))
    #assert(output.find('success') >= 0)
    os.chdir(config_path)
