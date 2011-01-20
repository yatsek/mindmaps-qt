from distutils.core import setup
import py2exe

setup(name="Mind Mapping",
      version="0.1",
      author="Wojciech Jurkowlaniec",
      author_email="wojtek.jurkowlaniec@gmail.com",
	 url="http://flickr.com/photos/wojtass",
      license="Private",
      packages=['mindmapping'],
      package_data={"mind": ["ui/*"]},
      scripts=["bin/mindmapping"],
      windows=[{"script": "bin/mindmapping"}],
      options={"py2exe": {"skip_archive": True, "includes": ["sip"]}})
