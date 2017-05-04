ReFrame provides an easy and flexible way to configure new systems and new programming environments.
It is shipped by default with a local and the Cray Swan systems configured.
As soon as you have configured a new system with its programming environments, adapting an existing regression test could be as easy as just adding the system's name in the `valid_systems` list and its associated programming environments in the `valid_prog_environs` list.

# The Configuration file

The configuration of systems and programming environments is performed by a special Python dictionary called `site_configuration` defined inside the file `<install-dir>/reframe/settings.py`.

Here is an example of how the configuration for Piz Daint at CSCS looks like:

```python
site_configuration = ReadOnlyField({
    'systems' : {
        'daint' : {
            'descr' : 'Piz Daint',
            'hostnames' : [ 'daint' ],
            'outputdir' : '$APPS/UES/jenkins/regression/maintenance',
            'logdir'    : '$APPS/UES/jenkins/regression/maintenance/logs',
            'stagedir'  : '$SCRATCH/regression/stage',
            'partitions' : {
                'login' : {
                    'scheduler' : 'local',
                    'modules'   : [],
                    'access'    : [],
                    'environs'  : [ 'PrgEnv-cray', 'PrgEnv-gnu',
                                    'PrgEnv-intel', 'PrgEnv-pgi' ],
                    'descr'     : 'Login nodes'
                },
                'gpu' : {
                    'scheduler' : 'nativeslurm',
                    'modules'   : [ 'daint-gpu' ],
                    'access'    : [ '--constraint=gpu' ],
                    'environs'  : [ 'PrgEnv-cray', 'PrgEnv-gnu',
                                    'PrgEnv-intel', 'PrgEnv-pgi' ],
                    'descr'     : 'Hybrid nodes (Haswell/P100)',
                },
                'mc' : {
                    'scheduler' : 'nativeslurm',
                    'modules'   : [ 'daint-mc' ],
                    'access'    : [ '--constraint=mc' ],
                    'environs'  : [ 'PrgEnv-cray', 'PrgEnv-gnu',
                                    'PrgEnv-intel', 'PrgEnv-pgi' ],
                    'descr'     : 'Multicore nodes (Broadwell)',
                }
            }
        }
    },

    'environments' : {
        'kesch' : {
            'PrgEnv-gnu' : {
                'type' : 'ProgEnvironment',
                'modules' : [ 'PrgEnv-gnu' ],
                'cc'      : 'mpicc',
                'cxx'     : 'mpicxx',
                'ftn'     : 'mpif90',
            },
        },
        '*' : {
            'PrgEnv-cray' : {
                'type' : 'ProgEnvironment',
                'modules' : [ 'PrgEnv-cray' ],
            },
            'PrgEnv-gnu' : {
                'type' : 'ProgEnvironment',
                'modules' : [ 'PrgEnv-gnu' ],
            },
            'PrgEnv-intel' : {
                'type' : 'ProgEnvironment',
                'modules' : [ 'PrgEnv-intel' ],
            },
            'PrgEnv-pgi' : {
                'type' : 'ProgEnvironment',
                'modules' : [ 'PrgEnv-pgi' ],
            }
        }
    }
})
```

# New System configuration
The list of supported systems is defined as a set of key/value pairs under the global configuration key `systems`.
Each system is a key/value pair, with the key being the name of the system and the value being another set of key/value pairs defining its attributes.
The valid attributes of a system are the following:

* `descr`: A detailed description of the system (default is the system name).
* `hostnames`: This is a list of hostname patterns that will be used by the regression when it tries to [auto-detect](#system-auto-detection) the system it runs on (default `[]`).
* `prefix`: Default regression prefix for this system (default `.`).
* `stagedir`: Default stage directory for this system (default `None`).
* `outputdir`: Default output directory for this system (default `None`).
* `logdir`: Default log directory for this system (default `None`).
* `partitions`: A set of key/value pairs defining the partitions of this system and their properties (default `{}`).
  See [next section](#partition-configuration) on how to define system partitions.


## System auto-detection
When the regression is launched, it tries to auto-detect the system it runs on based on its site configuration.
The auto-detection process is as follows:

The regression first tries to obtain the hostname from `/etc/xthostname`, which provides the unqualified "machine name" in Cray systems.
If this cannot be found the hostname will be obtained from the standard `hostname` command.
Having retrieved the hostname, the regression goes through all the systems in its configuration and tries to match the hostname against any of the patterns in the `hostnames` attribute.
The detection process stops at the first match found, and the system it belongs to is considered as the current system.
If the system cannot be auto-detected, regression will fail with an error message.
You can override completely the auto-detection process by specifying a system or a system partition with the `--system` option (e.g., `--system daint` or `--system daint:gpu`).


# Partition configuration
From the regression's point of view each system consists of a set of logical partitions.
These partitions need not necessarily correspond to real scheduler partitions.
For example, Piz Daint comprises three logical partitions: the login nodes (named `login`), the hybrid nodes (named `gpu`) and the multicore nodes (named `mc`), but these do not correspond to actual Slurm partitions.

The partitions of a system are defined similarly as a set of key/value pairs with the key being the partition name and the value being another set of key/value pairs defining the partition's attributes.
The available partition attributes are the following:
* `descr`: A detailed description of the partition (default is the partition name).
* `scheduler`: The job scheduler to use for launching jobs on this partition.
   Available values are the following:
   * `local`: Jobs on this partition will be launched locally as OS processes.
   When a job is launched locally, the regression will create a wrapper shell script for running the check on the current node.
   This is default scheduler if none is specified.
   * `nativeslurm`: Jobs on this partition will be launched using Slurm and the `srun` command for creating MPI processes.
   * `slurm+alps`: Jobs on this partition will be launched using Slurm and the `aprun` command for creating MPI processes (this scheduler is not thoroughly tested, due to lack of support on CSCS' systems).
* `access`: A list of scheduler options that will be passed to the generated job script for gaining access to that logical partition (default `[]`).
  You can see that for the Daint logical partitions we use the `--constraint` feature of Slurm to get access, since the logical partitions do not actually correspond to Slurm partitions.
* `environs`: A list of environments that the regression will try to use for running each check (default `[]`).
  The environment names must be resolved inside the `environments` section of the `site_configuration` dictionary (see [Environment configuration](#environment-configuration) for more information).
* `modules`: A list of modules to be loaded each time before running a regression check on that partition (default `[]`).
* `variables`: A set of environment variables to be set each time before running a regression check on that partition (default `{}`).
  This is how you can set environment variables (notice that both the variable name and its value are strings):

```python
'variables' : {
    'MYVAR' : '3',
    'OTHER' : 'foo'
}
```

* `resources`: A set of custom resource specifications and how these can be requested from the partition's scheduler (default `{}`).
  This variable is a set of key/value pairs with the key being the resource name and the value being a list of options to be passed to the partition's job scheduler.
  The option strings can contain "references" to the resource being required using the syntax `{resource_name}`.
  In such cases, the `{resource_name}` will be replaced by the value of that resource defined in the regression check that is being run.
  For example, here is how the resources are specified on Kesch, a system with 16 GPUs per node, for requesting a number of GPUs:

```python
'resources' : {
    'num_gpus_per_node' : [
        '--gres=gpu:{num_gpus_per_node}'
    ]
}
```
When the regression runs a check that defines `num_gpus_per_node = 8`, the generated job script for that check will have in its preamble the following line:
```bash
#SBATCH --gres=gpu:8
```
therefore requesting from the resource scheduler to allocate it 8 GPUs.


# Environment configuration

The environments available for testing to the different systems are defined under the `environments` key of the top-level `site_configuration` dictionary.
The `environments` of the `site_configuration` is a special dictionary that defines scopes for looking up an environment.
The `*` denotes the global scope and all environments defined there can be used by any system.
You can define a dictionary only for a specific system by placing it under an entry keyed with the name of that system, e.g., `daint`, or even for a specific partition, e.g., `daint:gpu`.
When an environment is used in the `environs` attribute of a system partition (see [Partition configuration](#partition-configuration)), it is looked up first in the entry of that partition, e.g., `daint:gpu`.
If no such entry exists, it is looked up in the entry of the system, e.g., `daint`.
If not found there yet, it is looked up in the global scope denoted by the `*` key.
If it cannot be found even there, then an error will be issued.
This look up mechanism allows you to redefine an environment for a specific system or partition.
In the example shown above, the `PrgEnv-gnu` is redefined for the system `kesch` (any partition), so as to use different compiler wrappers.

An environment is defined as key/value pair with the key being its name and the value being a dictionary of its attributes.
The possible attributes of an environment are the following:
* `type`: The type of the environment to create. There are two available environment types (note that names are case sensitive):
  * `Environment`: A simple environment.
  * `ProgEnvironment`: A programming environment.
* `modules`: A list of modules to be loaded when this environment is loaded (default `[]`, valid for all types)
* `variables`: A set of variables to be set when this environment is loaded (default `{}`, valid for all types)
* `cc`: The C compiler (default `cc`, valid for `ProgEnvironment` only).
* `cxx`: The C++ compiler (default `CC`, valid for `ProgEnvironment` only).
* `ftn`: The Fortran compiler (default `ftn`, valid for `ProgEnvironment` only).
* `cppflags`: The default preprocessor flags (default `''`, valid for `ProgEnvironment` only).
* `cflags`: The default C compiler flags (default `''`, valid for `ProgEnvironment` only).
* `cxxflags`: The default C++ compiler flags (default `''`, valid for `ProgEnvironment` only).
* `fflags`: The default Fortran compiler flags (default `''`, valid for `ProgEnvironment` only).
* `ldflags`: The default linker flags (default `''`, valid for `ProgEnvironment` only).
