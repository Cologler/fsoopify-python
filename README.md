# fsoopify

![GitHub](https://img.shields.io/github/license/Cologler/fsoopify-python.svg)
[![Build Status](https://travis-ci.com/Cologler/fsoopify-python.svg?branch=master)](https://travis-ci.com/Cologler/fsoopify-python)
[![PyPI](https://img.shields.io/pypi/v/fsoopify.svg)](https://pypi.org/project/fsoopify/)

Just make file system oopify.

## install

``` cmd
pip install fsoopify
```

## usage

``` py
import fsoopify

[file|directory] = fsoopify.NodeInfo.from_path(...)

# api for both file and directory
file.rename()
file.get_parent()
file.is_exists()
file.is_directory()
file.is_file()
file.delete()
file.create_hardlink()

# api for file
file.open()
file.size
file.read() and file.write()
file.read_text() and file.write_text()
file.read_bytes() and file.write_bytes()
file.copy_to()
file.load() and file.dump() # I love this API

# api for directory
directory.create() and directory.ensure_created()
directory.create_file()
directory.iter_items()
directory.list_items()
directory.get_fileinfo() and directory.get_dirinfo()
directory.has_file() and directory.has_directory()
```
