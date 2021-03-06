# pelican-plugin-installer

[![Build Status](https://travis-ci.org/kplaube/pelican-plugin-installer.svg?branch=master)](https://travis-ci.org/kplaube/pelican-plugin-installer)

A simple command line tool to help you installing Pelican plugins.

## Installing

It's possible to install the package through `pip`:

```
$ pip install pelican-plugin-installer
```

But if you like to live on the edge, just `git clone` this repository:

```
$ git clone git@github.com:kplaube/pelican-plugin-installer.git
$ cd pelican-plugin-installer/
$ python setup.py install
```

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

Deleting a plugin uses the same principle as install operation. Just inform the plugin name, with the `-d` option:

```
$ pelican-plugin-installer -d pin_to_top -c ~/my-pelican-site/pelicanconf.py
```

In order to update an already installed plugin, you can use the `-u` option:

```
$ pelican-plugin-installer -u pin_to_top -c ~/my-pelican-site/pelicanconf.py
```

You can always ask for help using the `--help` option:

```
$ pelican-plugin-installer --help
```

### Installing unofficial plugins

Sometimes you need to use some plugins that aren't inside the Pelican plugins repository. In that case, just use the Github URL as a parameter, during the installation process:

```
$ pelican-plugin-installer -i https://github.com/kplaube/extended_meta -c ~/my-pelican-site/pelicanconf.py
```

## Contributing

Contributions are very welcome!

We are using `py.test` and `tox` to ensure the application is working properly.
It's possible to execute tests through `Makefile` tasks:

```
$ make test
```

It'll run tests against some Python versions, and ensure the PEP8 is being followed strictly.
