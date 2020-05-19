from setuptools import setup

setup(name='python-intercom2',
      version='0.1',
      description='Python Intercom 2.0 API interface',
      url='https://github.com/millarm/python-intercom2',
      author='Matt Millar',
      author_email='matt@emillar.com',
      license='MIT',
      packages=['intercom'],
      install_requires=[
          'requests',
          'python-dateutil'
      ],
      tests_require=['pytest'],
      zip_safe=False)
