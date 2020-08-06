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
file.load_context() # load and dump the file in a context.

# api for directory
directory.create() and directory.ensure_created()
directory.create_file()
directory.iter_items()
directory.list_items()
directory.get_fileinfo() and directory.get_dirinfo()
directory.has_file() and directory.has_directory()
```

## Api

### File

You can use `fsoopify.FileInfo(...)` to create a `FileInfo` object and use file api.

#### Prop Api

- `size` - a `int` value with override `__str__`.

#### Test Api

- `is_exists()`
- `is_file()`

#### Open Api

- `open()` - alias for builtin `open`
- `open_for_read_bytes()`
- `open_for_read_text()`

#### Read and Write Api

- `write()`
- `write_text()`
- `write_bytes()`
- `write_from_stream()`
- `read()`
- `read_text()`
- `read_bytes()`
- `read_into_stream()`

And you can use `+=` for append data:

``` py
fi = FileInfo(...)
fi += 'data'
fi += b'data'
fi += FileInfo(other_file)
fi += io.BytesIO(b'data')
...
```

#### Serialize Api

- `load()`
- `dump()`
- `load_context()`

The easiest way to dump a json:

``` py
FileInfo('a.json').dump(the_obj_to_dump)
```

Or load:

``` py
obj = FileInfo('a.json').load()
```

The format can auto detect by extension name.

Another way to load and dump a file is `load_context()`:

``` py
with FileInfo('a.json').load_context() as ctx:
    ctx.data = the_obj_to_dump
```

With `load_context(lock=True)`, you can lock the file in the context.

#### Hash Api

To compute hash for a file:

``` py
crc32, md5, sha1 = FileInfo('a.json').get_file_hash('crc32', 'md5', 'sha1')
```

### Directory

You can use `fsoopify.DirectoryInfo(...)` to create a `DirectoryInfo` object and use directory api.

#### Tree Api

The easiest way to batch read files:

``` py
DirectoryInfo(...).get_tree()
# {
#      filename: b'file content',
#      sub_dirname: {
#           ...
#      }
# }

# to prevent load all file into memory:
DirectoryInfo(...).get_tree(as_stream=True)
```

Or batch write files:

``` py
tree = {
    'a.txt': b'abc',
    'b.txt': b'cde',
    'sub_dir': {
        'e.txt': b'ddd'
    }
}
DirectoryInfo(...).make_tree(tree)
```

## Optional packages

- `json5` - load or dump json5 file
- `pyyaml` - load or dump yaml file
- `toml` - load or dump toml file
- `pipfile` - load pipfile
