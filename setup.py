from setuptools import setup


install_requires = [
    'aiohttp',
    'pymorphy2',
]

setup(name='Search Engine',
      version='0.1',
      description='Service gives the categories list in json, matching the user request',
      author='Gubin Alexey',
      author_email='gubinlex@gmail.com',
      packages=['searchengine'],
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False)