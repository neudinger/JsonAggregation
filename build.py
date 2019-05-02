import sys
import os
from pybuilder.core import task
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")


name = "metrics"
version = "0.0.1"

default_task = ['install_dependencies', 'verify', 'publish']
    
@init
def depend(project):
    project.build_depends_on('mockito')
    # project.depends_on("elasticsearch")
    pass 