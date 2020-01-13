from setuptools import find_packages, setup

VERSION = "2.0.3"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-badges.svg
    :target: https://pypi.python.org/pypi/pinax-badges/

============
Pinax Badges
============

.. image:: https://img.shields.io/pypi/v/pinax-badges.svg
    :target: https://pypi.python.org/pypi/pinax-badges/

\ 

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-badges.svg
    :target: https://circleci.com/gh/pinax/pinax-badges
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-badges.svg
    :target: https://codecov.io/gh/pinax/pinax-badges
.. image:: https://img.shields.io/github/contributors/pinax/pinax-badges.svg
    :target: https://github.com/pinax/pinax-badges/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-badges.svg
    :target: https://github.com/pinax/pinax-badges/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-badges.svg
    :target: https://github.com/pinax/pinax-badges/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/

\ 

``pinax-badges`` is a a reusable Django badges application.
 
Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+-----+-----+
| Django / Python | 2.7 | 3.4 | 3.5 | 3.6 | 3.7 |
+=================+=====+=====+=====+=====+=====+
|  1.11           |  *  |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+-----+
|  2.0            |     |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+-----+
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxprojects.com",
    description="a reusable Django badges application",
    name="pinax-badges",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-badges/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "badges": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',	
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
    ],
    tests_require=[
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
