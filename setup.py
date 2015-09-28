from distutils.core import setup

setup(
    name='chimera-webadmin',
    version='0.0.1',
    packages=['chimera_webadmin', 'chimera_webadmin.controllers'],
    scripts=[],
    install_requires=['CherryPy'],
    package_data={'': ['jquery-1.11.3.min.js', 'webadmin.html']},
    url='http://github.com/astroufsc/chimera-webadmin',
    license='GPL v2',
    author='William Schoenell',
    author_email='william@iaa.es',
    description='A simple Chimera controller plugin to start/stop a telescope via web'
)
