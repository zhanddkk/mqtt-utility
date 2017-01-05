from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, chdir

here = path.abspath(path.dirname(__file__))
chdir(here)
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def __get_version():
    import sys
    sys.path.append(here + '/src')
    from ddclient import __version__
    return __version__
    pass


setup(name='ddclient',
      version=__get_version(),
      description='The data dictionary access client',
      long_description=long_description,
      author='Lei Zhan',
      author_email='lei.zhan@schneider-electric.com',
      license='MIT',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'],
      keywords='client',
      package_dir={'': 'src'},
      packages=find_packages(where='src', include=['ddclient']),
      install_requires=['namedlist', 'paho-mqtt'])
