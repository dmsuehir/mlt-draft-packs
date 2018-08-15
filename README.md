# mlt-draft-packs
This repository contains draft packs that have been created based on
[MLT](https://github.com/IntelAI/mlt) templates.

## Converting MLT Templates to draft packs

1. Create new folder in `mlt-draft-packs/packs` directory with the same
name as the MLT template, then navigate to that directory:

```
mkdir <template_name>
cd <template_name>
```

2. Copy the `Dockerfile` and `requirements.txt` file from the MLT
template to the current directory:

```
cp ~/my-mlt-repo/mlt-templates/<template_name>/Dockerfile .
cp ~/my-mlt-repo/mlt-templates/<template_name>/requirements.txt .
```

3. Create a helm chart, then navigate into the chart's directory:

```
helm create charts
cd charts
```

4.  Make the following updates in the helm chart:
 * In the `templates` directory, remove the default *.yaml files, then
 copy the yaml file(s) from the MLT template to this directory.
```
cd templates
rm deployment.yaml
rm ingress.yaml
rm service.yaml
cp ~/my-mlt-repo/mlt-templates/<template_name>/k8s-templates/job.yaml .
```

 * Update the template's yaml files to change the `$` MLT variable
 substitutions to the helm chart.  For example:

| MLT template yaml    | Draft chart yaml                                           |
|----------------------|------------------------------------------------------------|
| `$app-$run`          | `{{ template "charts.fullname" . }}`                       |
| `$app`               | `{{ .Chart.Name }}`                                        |
| `$image`             | `"{{ .Values.image.repository }}:{{ .Values.image.tag }}"` |
| `$num_workers`       | `{{ .Values.workersCount }}`                               |
| `$num_ps`            | `{{ .Values.psCount }}`                                    |

  * Go back up a directory and update the `values.yaml` file.  This is
  where any template-specific variables will go (things like
  `workersCount`, `psCount`, etc) and we need to clean up things that
  aren't needed here.
    * `replicaCount: 1` can be removed, or replaced with `workersCount`,
    `psCount`, etc if it's a distributed job.
    * Add any other template-specific variables here.
    * In the `image:` section, remove `repository: nginx` and
    `tag: stable`, since the job should get it's image repo/tag from
    the draft run.
    * In the `service:` section, change `type:` to `Job`, `TFJob`, etc.
    and remove the `port:` line since we aren't using it.
    * Ensure that the `ingress:` section has `enabled: False`.
    * We aren't really using any of the other stuff.

  * Update the name and description in the `Charts.yaml`.  I used the
  same name as the MLT template and gave a brief description of the
  chart, for example: "A Helm chart for running distributed TensorFlow
  model training jobs using the TFJob operator".

## Using mlt-draft-packs with draft

I haven't figured out the proper way to do this yet, but for now, I
copied the packs into draft's cache (for me, this was in
`/Users/dmsuehir/.draft`).  If this is done properly, you should see
them in your `draft pack list`.

Draft expects that you are starting out with a project directory that
contains your code files.  For `mlt-draft-packs`, this the code found
in the `mlt-draft-packs/examples` directory.  Here is an example of how
one of the `mlt-draft-packs/examples` would be used with draft:

```
$ cd mlt-draft-packs/examples/tf-dist-mnist

# This directory has our python code files
$ ll
total 56
-rw-r--r--  1 dmsuehir  staff  1775 Aug 14 17:12 data.py
-rw-r--r--  1 dmsuehir  staff  2829 Aug 14 17:09 kubernetes_debug_wrapper.py
-rw-r--r--  1 dmsuehir  staff  8278 Aug 14 16:23 main.py
-rw-r--r--@ 1 dmsuehir  staff  4743 Aug 14 17:12 model.py

$ draft create --pack=tf-dist-mnist
--> Ready to sail

# After calling draft create, we also have the Dockerfile, helm chart, etc.
$ ll
total 80
-rw-r--r--  1 dmsuehir  staff  1513 Aug 15 10:49 Dockerfile
drwxr-xr-x  3 dmsuehir  staff    96 Aug 15 10:49 charts
-rw-r--r--  1 dmsuehir  staff  1775 Aug 14 17:12 data.py
-rw-r--r--  1 dmsuehir  staff   211 Aug 15 10:49 draft.toml
-rw-r--r--  1 dmsuehir  staff  2829 Aug 14 17:09 kubernetes_debug_wrapper.py
-rw-r--r--  1 dmsuehir  staff  8278 Aug 14 16:23 main.py
-rw-r--r--@ 1 dmsuehir  staff  4743 Aug 14 17:12 model.py
-rw-r--r--  1 dmsuehir  staff   108 Aug 15 10:49 requirements.txt

# Update the draft.toml with your namespace
$ vi draft.toml

# Use draft up command for building/deploying the job
$ draft up
Draft Up Started: 'tf-dist-mnist': 01CMZBCG350YMAXFCYS46RCX9S
tf-dist-mnist: Building Docker Image: SUCCESS ⚓  (1.0049s)
tf-dist-mnist: Pushing Docker Image: SUCCESS ⚓  (3.7292s)
tf-dist-mnist: Releasing Application: SUCCESS ⚓  (3.6264s)
Inspect the logs with `draft logs 01CMZBCG350YMAXFCYS46RCX9S`

# kubectl commands can be used to see the running pods
$ kubectl get pods
NAME                                READY     STATUS    RESTARTS   AGE
tf-dist-mnist-ps-rrg5-0-zflqx       1/1       Running   0          12s
tf-dist-mnist-worker-rrg5-0-d64w8   1/1       Running   0          12s
tf-dist-mnist-worker-rrg5-1-6xfgu   1/1       Running   0          12s

# kubectl logs or kubetail can be used to see the logs
$ kubetail tf-dist --since 1m
Will tail 3 logs...
tf-dist-mnist-ps-rrg5-0-zflqx
tf-dist-mnist-worker-rrg5-0-d64w8
tf-dist-mnist-worker-rrg5-1-6xfgu
[tf-dist-mnist-worker-rrg5-0-d64w8] INFO:kubernetes_debug_wrapper:debug_on_fail set to False
[tf-dist-mnist-worker-rrg5-0-d64w8] INFO:kubernetes_debug_wrapper:Attempting to run: main.py
[tf-dist-mnist-worker-rrg5-0-d64w8] INFO:root:TensorFlow version: 1.8.0
[tf-dist-mnist-ps-rrg5-0-zflqx] INFO:kubernetes_debug_wrapper:debug_on_fail set to False
[tf-dist-mnist-worker-rrg5-0-d64w8] INFO:root:TensorFlow git version: b'unknown'
[tf-dist-mnist-ps-rrg5-0-zflqx] INFO:kubernetes_debug_wrapper:Attempting to run: main.py
[tf-dist-mnist-worker-rrg5-0-d64w8] INFO:root:tf_config: {'cluster': {'ps': ['tf-dist-mnist-ps-rrg5-0:2222'], 'worker': ['tf-dist-mnist-worker-rrg5-0:2222', 'tf-dist-mnist-worker-rrg5-1:2222']}, 'task': {'type': 'worker', 'index': 0}, 'environment': 'cloud'}
[tf-dist-mnist-worker-rrg5-1-6xfgu] INFO:kubernetes_debug_wrapper:debug_on_fail set to False
[tf-dist-mnist-ps-rrg5-0-zflqx] INFO:root:TensorFlow version: 1.8.0
[tf-dist-mnist-worker-rrg5-0-d64w8] INFO:root:task: {'type': 'worker', 'index': 0}
[tf-dist-mnist-worker-rrg5-1-6xfgu] INFO:kubernetes_debug_wrapper:Attempting to run: main.py
...

# Once you are done, run draft delete to delete the job
$ draft delete
app 'tf-dist-mnist' deleted

$ kubectl get pods
NAME                                READY     STATUS        RESTARTS   AGE
tf-dist-mnist-ps-rrg5-0-zflqx       1/1       Terminating   0          2m
tf-dist-mnist-worker-rrg5-0-d64w8   1/1       Terminating   0          2m
tf-dist-mnist-worker-rrg5-1-6xfgu   1/1       Terminating   0          2m
```