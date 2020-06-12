import os
import sys
import subprocess


def test_fabflee_mali():
    config_path = "%s/FabFlee/config_files/%s" % (
	    os.environ['TRAVIS_BUILD_DIR'], "mali")
    cmd = ["python3",
	"run.py",
	"input_csv",
	"source_data",
	"50",
	"simsetting.csv"
	]
    print(cmd)

    assert(subprocess.call(cmd,shell=True, cwd=config_path) == 0)
    output = subprocess.check_output(cmd,shell=True, cwd=config_path).decode("utf-8")
    assert(output.find('success') >= 0)
