from setuptools import setup, find_packages


setup(name='cachegrab',
      version='0.1.0',
      description='Caching tool ',
      url='https://github.com/xkortex/CacheGrab.git',
      author='Michael McDermott',
      author_email='',
      license='Private',
      packages=find_packages(exclude=["*.testing", "testing.*", "testing", "*.tests", "*.tests.*", "tests.*", "tests"]),
      install_requires=[
          'requests',
          'pandas>=0.18.1',
      ],
      zip_safe=False)
