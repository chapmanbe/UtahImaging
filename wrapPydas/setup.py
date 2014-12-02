from distutils.core import setup

setup(name="wrapPydas",
        version="0.1.2",
        author="Brian Chapman",
        author_email="brian.chapman@utah.edu",
        package_dir={'wrapPydas':'src'},
        install_requires="pydas",
        packages=['wrapPydas'],
    )
