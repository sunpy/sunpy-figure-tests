import json
import os
import pathlib
import urllib.request

import pytest

from sunpy.tests import hash


hashfile = 'https://raw.githubusercontent.com/sunpy/sunpy/master/sunpy/tests/figure_hashes_py36.json'
hashfile = urllib.request.urlopen(hashfile)
hashes = json.load(hashfile)


figpath = pathlib.Path(os.path.abspath(__file__)) / '..' / '..' / 'figures'
figpath = figpath.resolve()
figure_paths = [x for x in figpath.iterdir() if x.suffix == '.png']
ids = [figure_path.name for figure_path in figure_paths]


@pytest.mark.parametrize('fig_path', figure_paths, ids=ids)
def test_hash(fig_path):
    with open(fig_path, 'rb') as f:
        fhash = hash._hash_file(f)
    assert hashes[fig_path.stem] == fhash


def test_missing_figures():
    stems = [p.stem for p in figure_paths]
    missing = []
    for key in hashes:
        if key not in stems:
            missing.append(key)

    if len(missing):
        missing = '\n'.join(missing)
        raise RuntimeError(f'The following figure tests are missing an image:\n{missing}')
