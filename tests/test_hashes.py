import json
import os
import pathlib
import urllib.request

import pytest

from pytest_mpl import plugin


envs = {'py37-figure-devdeps': 'mpl_dev_ft_261_astropy_dev.json',
        'py38-figure': 'mpl_332_ft_261_astropy_401post1.json'}


def get_hashes(env):
    hashfile = f'https://raw.githubusercontent.com/sunpy/sunpy/master/sunpy/tests/figure_hashes_{envs[env]}'
    print(hashfile)
    hashfile = urllib.request.urlopen(hashfile)
    hashes = json.load(hashfile)
    return hashes


def get_figpaths(env):
    figpath = pathlib.Path(os.path.abspath(__file__)) / '..' / '..' / 'figures' / env
    figpath = figpath.resolve()
    figure_paths = [x for x in figpath.iterdir() if x.suffix == '.png']
    return figure_paths


envs = {env: {'hashes': get_hashes(env), 'fig_paths': get_figpaths(env)} for env in envs}


@pytest.mark.parametrize('env', envs)
def test_hashes(env):
    hash_list = envs[env]['hashes']
    # Check each figure has a hash that matches
    for fig_path in envs[env]['fig_paths']:
        with open(fig_path, 'rb') as f:
            fhash = plugin._hash_file(f)
        fname = fig_path.stem
        if fname in hash_list:
            assert hash_list[fname] == fhash
        else:
            raise RuntimeError(f'The following figure does not have an associated hash: {fname}')
    # Check each hash has a figure
    stems = [p.stem for p in envs[env]['fig_paths']]
    missing = []
    for key in envs[env]['hashes']:
        if key not in stems:
            missing.append(key)

    if len(missing):
        missing = '\n'.join(missing)
        raise RuntimeError(f'The following figure tests are missing an image:\n{missing}')
