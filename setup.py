import os
from glob import glob
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='oh-greenhouse',
    version='0.1',
    packages=['greenhouse'],
    include_package_data=True,
    license='Apache License 2.0',
    description='Track your contributors',
    long_description=README,
    url='https://github.com/openhatch/oh-greenhouse.com/',
    author='David Lu',
    author_email='daveeloo@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        ],
    install_requires=[
        'Django >= 1.3',
        'psycopg2',
        'south',
        'launchpadlib',
        'django-openid-auth',
        'python-openid',
        'distro-info',
        ],
    data_files=[
        ('', ["EXTERNALS", "INSTALL", "LICENSE", "README.rst"]),
        ('greenhouse/data', glob('greenhouse/data/*')),
        ('greenhouse/templates/greenhouse', glob('greenhouse/templates/greenhouse/*')),
        ('greenhouse/static/greenhouse/css', glob('greenhouse/static/greenhouse/css/*')),
        ('greenhouse/static/greenhouse/img', glob('greenhouse/static/greenhouse/img/*')),
        ('greenhouse/static/greenhouse/js', glob('greenhouse/static/greenhouse/js/*')),
        ],
    zip_safe=False,
)
