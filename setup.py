from setuptools import find_packages, setup

VERSION = "3.0.0"
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

+-----------------+-----+-----+-----+
| Django / Python | 3.6 | 3.7 | 3.8 |
+=================+=====+=====+=====+
|  2.2            |  *  |  *  |  *  |
+-----------------+-----+-----+-----+
|  3.0            |  *  |  *  |  *  |
+-----------------+-----+-----+-----+
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
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
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=2.2",
    ],
    tests_require=[
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
