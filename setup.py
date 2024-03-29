from setuptools import setup, find_packages


setup(
    name='transport_challenge',
    version="0.3.7",
    description='Transport Challenge API. Extends the Magnebot API and the TDW API.',
    long_description='Transport Challenge API. Extends the Magnebot API and the TDW API.',
    url='https://github.com/alters-mit/transport_challenge',
    author='Seth Alter',
    author_email="alters@mit.edu",
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='unity simulation tdw magnebot',
    packages=find_packages(),
    install_requires=['ikpy==3.1', 'magnebot==1.1.1', 'numpy', 'tdw==1.8.7.0', 'scipy']
)
