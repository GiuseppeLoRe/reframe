#
# CSCS ReFrame settings
#

class ReframeSettings:
    reframe_module = 'reframe'
    job_poll_intervals = [1, 2, 3]
    job_submit_timeout = 60
    checks_path = ['checks/']
    checks_path_recurse = True
    site_configuration = {
        'systems': {
            'kesch': {
                'descr': 'Kesch MCH TDS',
                'hostnames': ['keschcn-0012','keschln-\d+'],
                'modules_system': 'tmod',
                'resourcesdir': '/apps/common/UES/reframe/resources',
                'partitions': {
                    'login': {
                        'scheduler': 'local',
                        'environs': ['PrgEnv-cray', 'PrgEnv-cray-nompi',
                                     'PrgEnv-pgi', 'PrgEnv-pgi-nompi',
                                     'PrgEnv-gnu', 'PrgEnv-gnu-nompi'],
                        'descr': 'Kesch login nodes',
                    },
                    'cn': {
                        'scheduler': 'nativeslurm',
                        'access': ['--partition=test'],
                        'environs': ['PrgEnv-cray-c2sm',
                                     'PrgEnv-gnu-c2sm',
                                     'PrgEnv-cray-c2sm-gpu',
                                     'PrgEnv-gnu-c2sm-gpu'],
                        'descr': 'Kesch compute nodes',
                        'resources': {
                            '_rfm_gpu': ['--gres=gpu:{num_gpus_per_node}'],
                        }
                    }
                }
            },

            'generic': {
                'descr': 'Generic example system',
                'partitions': {
                    'login': {
                        'scheduler': 'local',
                        'modules': [],
                        'access': [],
                        'environs': ['builtin-gcc'],
                        'descr': 'Login nodes'
                    }
                }
            }
        },

        'environments': {
            'kesch': {
                'PrgEnv-pgi-nompi': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-pgi/18.10'],
                    'cc': 'pgcc',
                    'cxx': 'pgc++',
                    'ftn': 'pgf90',
                },
                'PrgEnv-pgi': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-pgi/18.10'],
                    'cc': 'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpif90',
                },
                'PrgEnv-cray': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-cray/1.0.2_gdr'],
                },
                'PrgEnv-cray-nompi': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-cray'],
                },
                'PrgEnv-gnu': {
                    'type': 'ProgEnvironment',
                    'modules': ['gmvapich2/17.02_cuda_8.0_gdr'],
                    'variables': {
                        'LD_PRELOAD': '$(pkg-config --variable=libdir mvapich2-gdr)/libmpi.so'
                    },
                    'cc': 'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpif90',
                },
                'PrgEnv-gnu-nompi': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-gnu'],
                    'cc': 'gcc',
                    'cxx': 'g++',
                    'ftn': 'gfortran',
                },
                'PrgEnv-cray-c2sm': {
                    'type': 'ProgEnvironment',
                    'modules': ['c2sm-rcm','c2sm/cray-env/base'],
                },
                'PrgEnv-cray-c2sm-gpu': {
                    'type': 'ProgEnvironment',
                    'modules': ['c2sm-rcm','c2sm/cray-env/gpu'],
                },
                'PrgEnv-pgi-c2sm': {
                    'type': 'ProgEnvironment',
                    'modules': ['c2sm-rcm','c2sm/pgi-env/base'],
                    'cc': 'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpif90',
                },
                'PrgEnv-pgi-c2sm-gpu': {
                    'type': 'ProgEnvironment',
                    'modules': ['c2sm-rcm','c2sm/pgi-env/gpu'],
                    'cc': 'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpif90',
                },
                'PrgEnv-gnu-c2sm': {
                    'type': 'ProgEnvironment',
                    'modules': ['c2sm-rcm','c2sm/gnu-env/base'],
                    'cc': 'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpif90',
                },
                'PrgEnv-gnu-c2sm-gpu': {
                    'type': 'ProgEnvironment',
                    'modules': ['c2sm-rcm','c2sm/gnu-env/gpu'],
                    'cc': 'mpicc',
                    'cxx': 'mpicxx',
                    'ftn': 'mpif90',
                },
            },
            '*': {
                'PrgEnv-cray': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-cray'],
                },

                'PrgEnv-gnu': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-gnu'],
                },

                'PrgEnv-intel': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-intel'],
                },

                'PrgEnv-pgi': {
                    'type': 'ProgEnvironment',
                    'modules': ['PrgEnv-pgi'],
                },

                'builtin': {
                    'type': 'ProgEnvironment',
                    'cc':  'cc',
                    'cxx': '',
                    'ftn': '',
                },

                'builtin-gcc': {
                    'type': 'ProgEnvironment',
                    'cc':  'gcc',
                    'cxx': 'g++',
                    'ftn': 'gfortran',
                }
            }
        },

        'modes': {
            '*': {
                'maintenance': [
                    '--exec-policy=async',
                    '--strict',
                    '--output=$APPS/UES/$USER/regression/maintenance',
                    '--perflogdir=$APPS/UES/$USER/regression/maintenance/logs',
                    '--stage=$SCRATCH/regression/maintenance/stage',
                    '--reservation=maintenance',
                    '--save-log-files',
                    '--tag=maintenance',
                    '--timestamp=%F_%H-%M-%S'
                ],
                'production': [
                    '--exec-policy=async',
                    '--strict',
                    '--output=$APPS/UES/$USER/regression/production',
                    '--perflogdir=$APPS/UES/$USER/regression/production/logs',
                    '--stage=$SCRATCH/regression/production/stage',
                    '--save-log-files',
                    '--tag=production',
                    '--timestamp=%F_%H-%M-%S'
                ]
            }
        }
    }

    logging_config = {
        'level': 'DEBUG',
        'handlers': [
            {
                'type': 'file',
                'name': 'reframe.log',
                'level': 'DEBUG',
                'format': '[%(asctime)s] %(levelname)s: '
                          '%(check_info)s: %(message)s',
                'append': False,
            },

            # Output handling
            {
                'type': 'stream',
                'name': 'stdout',
                'level': 'INFO',
                'format': '%(message)s'
            },
            {
                'type': 'file',
                'name': 'reframe.out',
                'level': 'INFO',
                'format': '%(message)s',
                'append': False,
            }
        ]
    }

    perf_logging_config = {
        'level': 'DEBUG',
        'handlers': [
            #@ {
            #@     'type': 'graylog',
            #@     'host': 'your-server-here',
            #@     'port': 12345,
            #@     'level': 'INFO',
            #@     'format': '%(message)s',
            #@     'extras': {
            #@         'facility': 'reframe',
            #@         'data-version': '1.0',
            #@     }
            #@ },
            {
                'type': 'filelog',
                'prefix': '%(check_system)s/%(check_partition)s',
                'level': 'INFO',
                'format': (
                    '%(asctime)s|reframe %(version)s|'
                    '%(check_info)s|jobid=%(check_jobid)s|'
                    '%(check_perf_var)s=%(check_perf_value)s|'
                    'ref=%(check_perf_ref)s '
                    '(l=%(check_perf_lower_thres)s, '
                    'u=%(check_perf_upper_thres)s)'
                ),
                'append': True
            }
        ]
    }

settings = ReframeSettings()
