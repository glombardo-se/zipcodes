import setuptools

with open("ReadMe.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name='zipcodes',
    version='1.0.0',
    author="Giovanni Lombardo",
    author_email="g.lombardo@pm.me",
    packages=['.'],
    description="Retrieval of world's zipcodes",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/gituser/test-tackage",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'greenlet==2.0.1',
        'numpy==1.24.1',
        'pandas==1.5.3',
        'python-dateutil==2.8.2',
        'pytz==2022.7.1',
        'six==1.16.0',
        'SQLAlchemy==1.4.46',
    ]
)