# AllConf - the All-Knowing Config Reader

[![PyPI](https://img.shields.io/pypi/v/allconf)](https://pypi.org/project/allconf/)

A configuration file reader for JSON and YAML with a bunch of nifty extras:

- File inclusion and extension
- Internal variable references
- Fault-tolerant access to values that don't exist
- Environment variable embedding (with defaults and "required" markers)
- Python value embedding
- On-demand external secret embedding via Fidelius _(untested in this fork so far)_
- Single-file rendering of a parsed config (via CLI)
- Python stub class generation for IDE completion (via CLI)

This is a fork of [`alviss`](https://github.com/ccpgames/allconf), continued
for development and support. A few names (notably the `ALVISS_FIDELIUS_MODE`
environment variable) still carry the original project's name.

```bash
pip install allconf
pip install allconf[fidelius]   # optional, for secret lookup
```

## TL;DR

Given this `my_cfg.yaml`:

```yaml
app:
  name: MyApp
  environment: dev
  log_level: INFO
```

load and use it like this:

```python
from allconf import quickloader

cfg = quickloader.autoload('my_cfg.yaml')

assert cfg.app.name == 'MyApp'
assert cfg.app.environment == 'dev'
assert cfg.app.log_level == 'INFO'
```

That's basically it!

**Looking for a specific function?** See the
[Public API index](docs/api-index.md).

## Features

### Fault-tolerant access

Any value that isn't in the config reads as `Empty` (falsy), no matter how
deeply nested, so there are no `KeyError`s and no `.get()` chains:

```python
cfg.app.timeout or 30            # 30 if not configured
cfg.does.not.exist.at.all        # Empty
cfg.app.timeout is Empty         # explicit check; `from allconf.structs import Empty`
```

### File extension and inclusion

```yaml
# prod.yaml
__extends__: base.yaml          # start from base.yaml; keys here override it
db:
  host: db.example.com
__include__: [logging.yaml]     # merge other files in
```

Both keys accept a single file or a list, can sit in any nested map, and
resolve paths relative to the file they appear in. A dotted key such as
`a.b.c: 1` expands to nested maps.

### Variable references

```yaml
basics:
  env: dev
name: my-data-${basics.env}     # -> "my-data-dev"
basics_copy: ${basics}          # a lone reference keeps the original type
```

### Environment variables

```yaml
password: ${__ENV__:MY_PASS}                 # left as-is if unset
region: ${__ENV__:AWS_REGION=eu-west-1}      # with a default
api_key: ${__ENV__:API_KEY!=}                # required: loading raises if unset
```

A missing required variable raises `AllConfSyntaxError` (a `ValueError`).

### Python values

```yaml
version: ${__PY__:mypackage.__version__}
fallback: ${__PY__:maybe_missing.attr=1.0.0}   # default if the import fails
```

### Secrets (Fidelius)

`${__FID__:...}` tags fetch secrets through the optional
[`fidelius`](https://pypi.org/project/fidelius/) package. Behavior is chosen
with the `ALVISS_FIDELIUS_MODE` environment variable (`ON_DEMAND` by default,
`ENABLED`, `DISABLED`, `SUBSTITUTE_ENV` or `MOCK`) or a `__fidelius__` key in
the file. See the [Public API index](docs/api-index.md#fidelius-secrets).
This integration has not been re-tested since the fork.

### Safe printing

`print(cfg)` and `cfg.as_dict()` mask string values whose key contains
`pass`, `secret`, `token` or `key`. Pass `unmaksed=True` (sic) to
`as_dict()`, `as_json()` or `as_yaml()` to get the real values.

### Global config

```python
from allconf.structs import SingletonConfig

cfg = SingletonConfig()
cfg.load(**quickloader.autoload('my_cfg.yaml').as_dict(unmaksed=True))
# Anywhere else in the program, SingletonConfig() is the same object
```

Subclass `SingletonConfig` to get a separate singleton per subclass. Use
`.update(...)` to patch values and `.load(...)` to replace everything.

## Command line tools

```bash
# Render a config, with all extends, includes and references resolved, to one file
allconf-render prod.yaml -o rendered.yaml

# Generate typed stub classes from a type descriptor file
allconf-stubber types.yaml -o cfg_stub.py
```

`allconf-render` leaves `__ENV__`, `__FID__` and `__PY__` expressions
unresolved so the output can be resolved later (it was built to generate
Kubernetes manifests). The stubber turns descriptor files such as

```yaml
app:
  name: str*          # trailing * = required
  timeout: int|None
```

into `BaseConfig` subclasses, so that `cfg: AllConfConfigStub = quickloader.autoload(...)`
gets IDE completion. Both tools take `-f` to overwrite output, `-s` for silent
and `-v` for verbose. Details in the [Public API index](docs/api-index.md#cli).

## More documentation

- [Public API index](docs/api-index.md): every public function and class, by task
- [`_OLD_README.md`](_OLD_README.md): the original long-form documentation
  (may be out of date and still says "alviss" in places)
- [Changelog](CHANGELOG.md)

Released under the [MIT License](LICENSE).
