from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='undefinedcuriosity',
      version='0.1',
      description='Undefined Curiosity Data Toolbox',
      url='https://github.com/UndefinedCuriosity/undefinedcuriosity.git',
      author='MJ',
      author_email='UndefinedCuriosity@gmail.com',
      license='MIT',
      packages=['undefinedcuriosity'],
      install_requires=[
          'pandas'
          ,'fuzzywuzzy'
      ],
      zip_safe=False)
