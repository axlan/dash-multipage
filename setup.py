import io
from collections import OrderedDict

from setuptools import setup, find_packages

main_ns = {}
exec(open('dash_multipage/version.py').read(),
     main_ns)  # pylint: disable=exec-used

setup(
    name='dash_multipage',
    version=main_ns['__version__'],
    author='Jonathan Diamond',
    maintainer='Jonathan Diamond',
    packages=find_packages(exclude=['example*']),
    description=('A framework to simplify some of the challenges in setting up multipage dash pages.'),
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/axlan/dash-multipage',
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/axlan/dash-multipage'),
        ('Code', 'https://github.com/axlan/dash-multipage'),
        ('Issue tracker', 'https://github.com/axlan/dash-multipage/issues'),
    )),
    install_requires=[
        'dash',
        'dash-html-components',
        'dash-core-components'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)
