from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

# Setting up
setup(
        name="panduza", 
        version='0.0.1',
        author="Panduza Team",
        author_email="panduza.team@gmail.com",
        description='Wrapper for Panduza MQTT Calls',
        long_description='This library provides simple wrapper to help implementing tests through panduza interfaces',
        packages=find_packages(),
        cmdclass={'install': CustomInstallCommand},

        install_requires=['paho-mqtt', 'python-magic', 'colorama', 'robotframework-pythonlibcore'],

        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            'Operating System :: POSIX',
        ]
)

