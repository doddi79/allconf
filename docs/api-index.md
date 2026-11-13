# allconf Public API Index

- Distribution: `allconf` (PyPI) — Import: `allconf`
- Covers: version **4.0.2** (the public API is unchanged since 4.0.0)
- Depends on: `batutils >=2,<3` (see its [API index](https://github.com/doddi79/batutils/blob/main/docs/api-index.md)), `PyYAML`. Optional extra `allconf[fidelius]` for secret lookup.
- Longer feature walkthrough (may be dated, still says "alviss" in places): [_OLD_README.md](../_OLD_README.md)
- Console scripts: `allconf-render`, `allconf-stubber` (see [CLI](#cli))

`allconf` reads JSON/YAML config files with includes, inheritance, `${...}`
references, env-var and Python-value injection, and returns an attribute-access
object that never raises on missing keys.

## Find it by task

| I want to… | Use | Section |
|------------|-----|---------|
| Load a YAML/JSON config into a dot-accessible object | `quickloader.autoload(path)` | [Loading](#loading) |
| Read config values that may not exist without `KeyError` | `BaseConfig` attribute access, returns `Empty` | [Config objects](#config-objects) |
| Share one config across a whole app (global config) | `SingletonConfig` | [Config objects](#config-objects) |
| Build a config object from a dict/kwargs, reload or patch it | `BaseConfig(**kw)`, `.load()`, `.update()` | [Config objects](#config-objects) |
| Print or dump config without leaking passwords/tokens | `cfg.as_dict()`, `as_json()`, `as_yaml()`, `str(cfg)` (masked) | [Config objects](#config-objects) |
| Inherit from a base config file / merge in extra files | `__extends__`, `__include__` keys | [File syntax](#config-file-syntax) |
| Reference another value, env var, Python attribute or secret | `${a.b}`, `${__ENV__:X}`, `${__PY__:mod.attr}`, `${__FID__:...}` | [File syntax](#config-file-syntax) |
| Require an env var to be set | `${__ENV__:NAME!=}` | [File syntax](#config-file-syntax) |
| Get the resolved config as one flat file (e.g. for Kubernetes manifests) | `render_load`, `SimpleStaticRenderer`, `allconf-render` | [Rendering](#rendering) |
| Debug what the file parses to, as a plain dict | `raw_load(path)` | [Loading](#loading) |
| Generate typed Python stub classes for IDE autocompletion | `SimpleStubMaker`, `allconf-stubber` | [Stub generation](#stub-generation) |
| Control secret lookup (Fidelius) behavior | `FideliusMode`, `ALVISS_FIDELIUS_MODE` env var, `__fidelius__` key | [Fidelius](#fidelius-secrets) |
| Catch config errors | `AllConfError` hierarchy | [Errors](#errors) |
| Handle config keys that are Python keywords (`class`, `in`) | `escape_keyword`, `unescape_keyword`, `is_keyword` | [Utils](#utils) |

---

## Loading

Import: `from allconf import quickloader` (or `from allconf.loaders import ...`).
`allconf.quickloader` re-exports everything from `allconf.structs` and `allconf.loaders`,
so `quickloader.BaseConfig`, `quickloader.autoload`, etc. all work.

| Signature | Result / behavior |
|-----------|-------------------|
| `autoload(file_name: str, encoding='utf-8') -> BaseConfig` | Loads and fully resolves a `.json`, `.yaml` or `.yml` file (extends, includes, references, env, Fidelius, py-inject). Always returns a plain `BaseConfig`, even if you wanted a `SingletonConfig`: call `.load(**cfg.as_dict(unmaksed=True))` on a singleton to transfer |
| `raw_load(file_name, skip_env_loading=False, skip_fidelius=False, skip_py_inject=False, encoding='utf-8') -> dict` | Same parsing, returns the plain dict (unmasked) |
| `render_load(file_name, skip_env_loading=True, skip_fidelius=True, skip_py_inject=True, encoding='utf-8') -> str` | Resolved config re-serialized in the **same format as the source file**. Note the defaults are inverted: env, Fidelius and `__PY__` expressions are **left unresolved** in the output |
| `guess_loader_class(file_name) -> Type[IAllConfLoader]` | Chooses the loader by extension. Raises `AllConfUnknownFileTypeError` for anything but `.json`, `.yaml`, `.yml` |

Loader classes (rarely needed directly): `JsonFileConfigLoader`, `YamlFileConfigLoader`
(`BaseLoader` subclasses implementing `IAllConfLoader`): `load_file(file_name, no_resolve=False, no_extend=False, no_includes=False, no_env_load=False, no_fidelius=False, no_py_inject=False, encoding='utf-8')`,
`load_raw(raw_data: str, ...same flags)`, `.data -> dict`, `.rendered -> str`,
`set_fidelius_mode(mode)`, `get_fidelius_mode()`. `JsonFileConfigLoader.load(file_name)` is a legacy static method.
Source: [loaders](../allconf/loaders), tests [test_parsing.py](../tests/basic/test_parsing.py), [test_rendering.py](../tests/basic/test_rendering.py).

## Config objects

Import: `from allconf.structs import BaseConfig, SingletonConfig` (also `Empty` etc. via `from allconf.structs import *`).

```python
cfg = quickloader.autoload('my_cfg.yaml')
cfg.app.name                  # value
cfg.app.nothing.deeper        # Empty (falsy), never raises
cfg.app.timeout or 30         # default idiom
cfg.app.timeout is Empty      # explicit "missing" test
```

| Signature | Behavior |
|-----------|----------|
| `BaseConfig(**kwargs)` | Data wrapped in a dict-like with attribute access. Missing keys at any depth return `Empty`; keys with `None` value also read as `Empty`. Python-keyword keys use the escaped spelling (`in_`) |
| `.load(**kwargs)` | **Replaces** all data |
| `.update(**kwargs)` | Deep-merges into existing data (nested dicts merged, other values overwritten) |
| `cfg.key = value` | Same as `update(key=value)` for names not starting with `_` |
| `.as_dict(unmaksed=False) -> dict`, `.as_json(unmaksed=False) -> str`, `.as_yaml(unmaksed=False) -> str` | Note the parameter's spelling: `unmaksed` (sic). By default values of keys containing `pass`, `secret`, `token` or `key` (string/bytes only) are replaced with `********`. `str(cfg)` / `repr(cfg)` are masked likewise |
| `SingletonConfig(BaseConfig)` | Uses `batutils` `Singleton` metaclass: the first construction fixes the instance; later `SingletonConfig(...)` calls return the same object and ignore new arguments (use `.load` / `.update`). Subclass it to get a separate singleton per subclass (e.g. `class ServerCfg(SingletonConfig)`) |

Source: [baseconfig.py](../allconf/structs/baseconfig.py), [singletonconfig.py](../allconf/structs/singletonconfig.py).
`allconf.structs.cfgstub._BaseCfgStub` is the private base of generated stubs.

## Config file syntax

Supported in `.yaml` / `.json`. Special keys start with `__`. Relative paths resolve against the file that contains them. Examples in [tests/res/rendering/yaml](../tests/res/rendering/yaml).

| Syntax | Meaning |
|--------|---------|
| `__extends__: file.yaml` (or a list) | Load the file(s) as a base for the enclosing map; keys in the current file override. `__extend__` also accepted |
| `__include__: file.yaml` (or a list) | Merge the file's contents into the enclosing map. `__includes__` also accepted. Can be nested in a sub-map or a dotted key: `collapsed.group.__include__: x.yaml` |
| `a.b.c: value` | A dotted key is expanded to nested maps (`a: {b: {c: value}}`) |
| `${other.key}` | Reference another value in the same config by dotted path. Embedded in a larger string it is interpolated as text; a lone reference keeps the target's type |
| `${__ENV__:NAME}` | Environment variable. Unset → left as the literal text |
| `${__ENV__:NAME=default}` | Environment variable with default |
| `${__ENV__:NAME!=}` | **Required** environment variable. If unset/empty, load raises `AllConfSyntaxError` (message "Required variable config value(s) unresolved") |
| `${__PY__:package.module.attr}` | Inject a Python importable value. `${__PY__:mod.attr=default}` falls back to `default` if the import fails |
| `${__FID__:...}` | Fidelius secret reference, see [Fidelius](#fidelius-secrets) |
| `__fidelius__: {ALVISS_FIDELIUS_MODE: ..., kwargs: {...}}` | In-file Fidelius configuration |

Unlisted keys beginning with `__` are ignored (dropped from the data).

## Rendering

Import: `from allconf.renderers import SimpleStaticRenderer` (implements `IStaticRenderer`).

| Signature | Behavior |
|-----------|----------|
| `SimpleStaticRenderer().render_static_config_from_file(file: str) -> str` | `render_load(file)` |
| `.render_static_config_to_file(input_file, output_file, overwrite_existing=False)` | Writes the render; raises `AllConfFileAlreadyExistsError` if the output exists and `overwrite_existing` is false |

## Stub generation

Import: `from allconf import stubber` → `stubber.SimpleStubMaker` (implements `IStubMaker`).
Input is a *type descriptor* YAML where leaf values are type names. Generated classes
subclass `BaseConfig`, so a typed `cfg: AllConfConfigStub = autoload(...)` gets IDE completion.

| Signature | Behavior |
|-----------|----------|
| `SimpleStubMaker().render_stub_classes_from_descriptor_file(file, is_private=True, class_name='AllConfConfigStub') -> str` | Python source text |
| `.render_stub_classes_to_file(input_file, output_file, overwrite_existing=False, is_private=True, class_name='AllConfConfigStub')` | Writes it; raises `AllConfFileAlreadyExistsError` if the file exists and not overwriting. `is_private=False` makes class names public and exports them in `__all__` |

Descriptor grammar (from [tests/res/stubber/simple.yaml](../tests/res/stubber/simple.yaml)):
`foo: str`, `b: INT` (case-insensitive), `x: str | int`, `y: str|none`, `z: list[str]`, `w: Dict[str,str]`, `v: dict`.
A trailing `*` (`bar: float*`) marks the field **required** (non-`Empty` type) and forces its parent chain to be required too. `${str}:` as a key means "map with arbitrary keys". Fields without `*` are typed `Union[<type>, Empty]`.
Python-keyword field names are escaped (`in` → `in_`). Failures raise `AllConfStubberSyntaxError` / `AllConfStubberInvalidTypeName`.
Supporting data classes `StubField`, `StubClass` are exported from `allconf.stubber.stubmaker` for building stubs programmatically.
Tests: [test_stubber.py](../tests/basic/test_stubber.py).

## CLI

| Command | Arguments |
|---------|-----------|
| `allconf-render FILE [-o [OUTPUT]] [-f] [-s \| -v]` | Print (or write with `-o`) the rendered static config. `-f` overwrite output, `-s` silent (errors to stderr), `-v` debug logs. Exit code 3 on `AllConfError` |
| `allconf-stubber FILE [-o [OUTPUT]] [-f] [-n CLASS_NAME] [-x] [-s \| -v]` | Generate stub code. `-n None` skips the final class, `-x` exports all class names publicly. Exit code 3 on `AllConfError` |

## Fidelius (secrets)

Optional integration with the `fidelius` package (`pip install allconf[fidelius]`; marked untested in the fork's README).

`FideliusMode(EnumEx)` — set via env var `ALVISS_FIDELIUS_MODE` (name kept from the original project), a `__fidelius__` key in the file, or `loader.set_fidelius_mode(...)`:

| Mode | Value | Effect |
|------|-------|--------|
| `ON_DEMAND` | 0 (default) | Use Fidelius only if a `${__FID__:...}` tag is found; raises `AllConfFideliusNotInstalledError` if the package is missing |
| `ENABLED` | 1 | Fidelius loaded on startup; `AllConfFideliusNotInstalledError` if missing |
| `DISABLED` | 2 | `__FID__` tags left unresolved |
| `SUBSTITUTE_ENV` | 3 | Replace `${__FID__:a:b}` with env var `a__b` |
| `MOCK` | 4 | Fidelius enabled but using its Mock implementation (testing/dev) |

Tests: [tests/nofidelius](../tests/nofidelius).

## Errors

All in `allconf.structs.errors`, importable from `allconf.structs`:

```
AllConfError
├─ AllConfFileNotFoundError(message, file_name='?')        also FileNotFoundError
├─ AllConfFileAlreadyExistsError(message, file_name='?')   also FileExistsError
├─ AllConfParsingError                                      also ValueError
│  ├─ AllConfSyntaxError          (e.g. unresolved required `!=` variable)
│  ├─ AllConfExpressionResolvingError
│  │  ├─ AllConfFideliusError
│  │  ├─ AllConfFideliusNotInstalledError                    also ImportError
│  │  └─ AllConfFideliusSyntaxError                          also AllConfSyntaxError
│  └─ AllConfUnknownFileTypeError(message, file_name='?')    also NotImplementedError
└─ AllConfStubberError
   └─ AllConfStubberSyntaxError(message, field_name='?')     also ValueError
      └─ AllConfStubberInvalidTypeName(message, field_name='?', type_name='?')  also TypeError
```

Because parsing errors derive from `ValueError`, `except ValueError` also catches a missing required variable.

## Utils

`from allconf.utils import is_keyword, escape_keyword, unescape_keyword`

- `is_keyword(string, include_escaped=False) -> bool` — Python keyword (optionally also the escaped `kw_` form).
- `escape_keyword(string) -> str` / `unescape_keyword(string) -> str` — `in` ↔ `in_`.

## Gaps and cautions

- No deprecated names declared. Some docs and variable names still say "alviss"/"Alviss" (original project).
- `allconf.loaders.base.BaseLoader` and `FideliusMode.MOCK` internals were read from source only; the Fidelius flow is untested in this fork per the README.
- The README only has the TL;DR; configuration-syntax details above were verified by running them against a temp config and the test resources, not from prose docs. `.toml`, `.ini`, `.xml` fixtures in `tests/res/_junk` are **not** supported.
- `SingletonConfig` with `autoload`: not wired together; see the transfer pattern above.
