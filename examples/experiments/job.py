#!/usr/bin/env python3
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

from lib.exp import Client
import json
import kubernetes
import logging
import os
import random
import time


def main():
    ns = os.getenv('EXPERIMENT_NAMESPACE')
    job_name = os.getenv('JOB_NAME')
    log = logging.getLogger(__name__)

    if not ns or not job_name:
        raise Exception('Missing EXPERIMENT_NAMESPACE or JOB_NAME')

    c = Client(ns)
    exp = c.current_experiment()

    log.info('Starting job {} for experiment {}'.format(job_name, exp.name))

    try:
        result = c.create_result(exp.result(c.get_job(job_name)))
    except kubernetes.client.rest.ApiException as e:
        body = json.loads(e.body)
        if body['reason'] != 'AlreadyExists':
            raise e
        result = c.get_result(job_name)

    # result.record_values({'environment': os.environ})
    # result = c.update_result(result)

    for i in range(0, 201, 10):
        values = {
            'step-{}'.format(i): {
                'loss': random.random(),
                'accuracy': random.random()
            }
        }
        log.info('publishing results: {}'.format(
            json.dumps(values, sort_keys=True)))
        result.record_values(values)
        time.sleep(1)
        result = c.update_result(result)


if __name__ == '__main__':
    main()
