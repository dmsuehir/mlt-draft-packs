#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

import logging
import os
import pdb
import sys
import traceback

"""
This Kubernetes debug wrapper is copied to the app directory when a template is
initialized.  Debugging a failure is enabled when the DEBUG_ON_FAIL environment
variable is set to true.  If enabled and an unhandled exception is caught, a
pdb breakpoint is set allowing the user to attach to the pod and debug.
"""

# Setup logging for this debug wrapper
logger = logging.getLogger("kubernetes_debug_wrapper")
logging.basicConfig()
logger.setLevel(logging.INFO)


def _get_debug_on_fail():
    """ Returns true of debug_on_fail is enabled """
    return os.environ.get("DEBUG_ON_FAIL", "false").lower() == "true"


def _run_command():
    """ Get the command to execute and the rest of the command line args """
    file_index = sys.argv.index(__file__)
    new_command = sys.argv[(file_index + 1):]
    logger.info("Attempting to run: {}".format(" ".join(new_command)))

    with open(new_command[0], "r") as script:
        code = compile(script.read(), new_command[0], 'exec')
        exec(code, globals())


def _start_debug():
    """ Start debug when a failure is encountered """
    traceback.print_exc()

    # Print a message noting how to attach to the pod for debug
    hostname = os.environ.get("HOSTNAME", "")
    if hostname:
        print("\nDebug failure using the following command:")
        print("kubectl attach -it {}\n".format(hostname))

    pdb.post_mortem()
    sys.exit(1)


def setup_debug_wrapper():
    debug_on_fail = _get_debug_on_fail()
    logger.info("debug_on_fail set to {}".format(debug_on_fail))

    if debug_on_fail:
        logger.info("Pod will enter the pdb debugger if an error "
                    "is encountered.")

    try:
        _run_command()
    except KeyboardInterrupt:
        # Script was intentionally stopped, so let it error
        raise
    except Exception:
        if debug_on_fail:
            # Script stopped unexpectedly, so let's debug
            _start_debug()
        else:
            # DEBUG_ON_FAIL is not set, so just raise the Exception
            raise


if __name__ == "__main__":
    setup_debug_wrapper()
