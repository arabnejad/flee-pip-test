import os
import sys
import subprocess

sys.path.insert(0, '%s/FabSim3/base/' % (os.environ['TRAVIS_BUILD_DIR']))

from deploy.templates import *
from deploy.machines import *
from fabric.contrib.project import *
from base.fab import *


def test_fabflee():
    """
    The main FabSim3 test suite. Every test is captured in an assert statement.
    """
    assert("plugins" in get_plugin_path("FabFlee"))
    assert("FabFlee" in get_plugin_path("FabFlee"))
    assert(len(get_fabsim_git_hash()) > 0)


def test_fabflee_install():
    print(os.environ['TRAVIS_BUILD_DIR'])
    assert(subprocess.call(
        ["fabsim", "localhost", "install_plugin:FabFlee"]) == 0)


def test_fabflee_mali():
    cmd = ["fabsim",
	"localhost",
	"flee:mali,simulation_period=50,,flee_location={0}/flee".format(
	    os.environ['TRAVIS_BUILD_DIR'])
	]
    print(cmd)

    assert(subprocess.call(cmd) == 0)
    output = subprocess.check_output(cmd).decode("utf-8")
    assert(output.find('success') >= 0)
