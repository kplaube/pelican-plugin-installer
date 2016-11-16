# pelican-plugin-installer

A simple command line tool to help you installing Pelican plugins.

## Installing

The project is still alpha, so we haven't published it to [PyPI](https://pypi.python.org/pypi) yet. To start using it right now, the proper way is through `git clone`:

```
$ git clone git@github.com:kplaube/pelican-plugin-installer.git
$ cd pelican-plugin-installer/
$ python setup.py install
```

Soon we'll publish the package, so the installation will be done through `pip install` :)

## Using

`pelican-plugin-installer` is just a set of `git` commands that gets a plugin from [https://github.com/getpelican/pelican-plugins](https://github.com/getpelican/pelican-plugins) and copy it to your Pelican project.

Install operations can be done using the `-i` option. Example:

```
$ cd ~/my-pelican-site/
$ pelican-plugin-installer -i pin_to_top
```

It will install the plugin into the first folder listed in your `PLUGINS_PATH`. You can explicitly specify the pelican configuration file:

```
$ pelican-plugin-installer -i pin_to_top -c ~/my-pelican-site/pelicanconf.py
```
