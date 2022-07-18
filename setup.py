from setuptools import setup

setup(
    name='munchkin',
    version='1.0',
    packages=['munchkin'],
    url='https://github.com/Mathieu-Beliveau/munchkin',
    license='Apache 2',
    author='mbeliveau',
    author_email='mathieu.beliveau.1@gmail.com',
    description='Bluetooth automated screen locker',
    install_requires=['pybluez', 'PyQt5'],
    entry_points={"console_scripts": ["realpython=Munchkin.__main__:main"]},
)
