from setuptools import setup

setup(
    name='pyfdtd',
    version='0.1.0',
    description='2D FDTD using numpy',
    long_description='pyfdtd is a 2D electromagnetic fieldsolver in time-domain using numpy.',
    author=', '.join((
        'Patrik Gebhardt <grosser.knuff@googlemail.com',
    )),
    author_email='grosser.knuff@googlemail.com',
    url='http://schansge.github.com/pyfdtd/',
    download_url='http://github.com/schansge/pyfdtd/downloads',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
	"Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    packages=['pyfdtd', 'pyfdtd.field', 'pyfdtd.pml', 'pyfdtd.constants', 'pyfdtd.material', 'pyfdtd.port', 'pyfdtd.solver'],
)
