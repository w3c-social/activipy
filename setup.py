## Activipy --- ActivityStreams 2.0 implementation and testing for Python
## Copyright © 2015  Christopher Allan Webber <cwebber@dustycloud.org>
##
## This file is part of Activipy, which is GPLv3+ or Apache v2, your option
## (see COPYING); since that means effectively Apache v2...
##
## Apache v2 header:
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.

from setuptools import setup, find_packages

setup(
    name="activipy",
    version="0.2.dev",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "PyLD",
    ],
    extras_require={
        "dev": [
            "pytest",
            "sphinx",
        ]
    },
    license="Apache v2",
    author="Christopher Allan Webber",
    author_email="cwebber@dustycloud.org",
    description="ActivityStreams 2.0 implementation and testing for Python",
    long_description="""An ActivityStreams 2.0 implementation for Python.
Provides an easy API for building ActivityStreams 2.0 based applications
as well as a test suite for testing ActivityStreams 2.0 libraries against.""",
    classifiers=[
        # @@: Might need to drop v2
        "License :: OSI Approved :: Apache Software License"])
