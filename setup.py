from distutils.core import setup, Extension

module1 = Extension('bbspi',
                    sources = ['bbspi.c'],
                    libraries = ['pigpio'])

setup (name = 'PackageName',
       version = '1.0',
       description = 'This is a bitbang SPI interface',
       author = 'Dave Astels',
       author_email = 'dastels@daveastels.com',
       ext_modules = [module1])
