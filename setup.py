# -*- coding: utf-8 -*-

import setuptools

from inventree_kicad_plugin.version import KICAD_PLUGIN_VERSION

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="inventree-kicad-plugin",

    version=PLUGIN_VERSION,

    author="Andre F. K. Iwers",

    author_email="iwers11@gmail.com",

    description="KiCad EDA conform API endpoint for KiCad's parts library tool",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="inventree kicad rest api",

    url="https://github.com/afkiwers/inventree-kicad-plugin",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
    ],

    setup_requires=[
        "wheel",
        "twine",
    ],

    python_requires=">=3.6",

    entry_points={
        "inventree_plugins": [
            "InvenTreeKiCadPlugin = inventree_kicad_plugin.KiCadLibraryPlugin:KiCadLibraryPlugin"
        ]
    },
    
    include_package_data=True,
)
