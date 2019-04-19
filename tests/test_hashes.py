import json
import os
import pathlib
import urllib.request

import pytest

from sunpy.tests import hash


@pytest.fixture()
def hashes():
    hashfile = 'https://raw.githubusercontent.com/sunpy/sunpy/master/sunpy/tests/figure_hashes_py36.json'
    hashfile = urllib.request.urlopen(hashfile)
    return json.load(hashfile)


def test_hashes(hashes):
    figpath = pathlib.Path(os.path.abspath(__file__)) / '..' / '..' / 'figures'
    figpath = figpath.resolve()
    figs = [x for x in figpath.iterdir() if x.suffix == '.png']
    for fig in figs:
        with open(fig, 'rb') as f:
            fhash = hash._hash_file(f)
        assert hashes[fig.stem] == fhash
