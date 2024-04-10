# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## Added

- A way to force ENV/FID variables to have some value and raise errors if 
  they are empty/not found (especially FID secrets, where the presence of an 
  empty value indicates problems but we don't want to actually show the 
  value if there is one... i.e. the difference between "wrong password" and 
  "no password"). Something like `${__ENV__:ENVIRONMENT!=}` which makes 
  semantic sense, as in "not equal to blank".
- A way to "cast" certain config values to Python types on-load (e.g. 
  datetime, decimal, bytes, or just some class a.k.a. dependency injection) 
  although this should not be default behaviour (akin to YAML's `load` vs 
  `safe_load`, except we want safe to be the default)
- A way to include/extend URLs (or remote files that is) but again, should 
  not be enabled by default!
- Support for reading INI/TOML/XML config files


## [3.0.0-beta.1] - 2024-04-08

### Added

- Fidelius mode - Alviss now reads the `ALVISS_FIDELIUS_MODE` environment 
  variable to determine one of the four Fidelius modes available:
  - `ON_DEMAND` (**default**): Fidelius is only ever loaded (i.e. an import is 
    attempted) if fidelius expressions (`__FID__`) are encountered when reading 
    a config
  - `ENABLED`: Alviss tries to import fidelius on startup and raises an 
    `ImportError` if it fails
  - `DISABLED`: All fidelius expressions (`__FID__`) are simply ignored and 
    left unparsed
  - `SUBSTITUTE_ENV`: All fidelius expressions (`__FID__`) are treated as if 
    they are environment variable expressions (`__ENV__`)
- Error reporting on the keys that have Fidelius tags in them in case of a 
  Fidelius related error _(like access problems or if fidelius is not installed)_

### Changed

- Migrated the project from our internal repos to Github and Pypi
- Alviss now ships by default without [fidelius](https://pypi.org/project/fidelius/)
  support and runs in `ALVISS_FIDELIUS_MODE=ON_DEMAND` and this only tries 
  to import fidelius if a `__FID__` expression is encountered
  - Installing Alviss with built in fidelius support can still be done via 
    `pip install alviss[fidelius]` plus all the `boto3` stuff and such

### Fixed

- An issue where the default values of environment variables could not 
  contain any whitespaces (like a simple space)


## [2.7.1] - 2021-11-30

### Fixed

- Issue where Fidelius expressions were being evaluated by default when calling `render_load`


## [2.6.0] - 2021-11-29

### Added

- Automatic parsing of Fidelius expressions `{$__FID__:...}`


## [2.5.0] - 2021-08-21

### Changed

- Environment variable injection tags can now have a default value that they 
  get assigned if the environment variable in question was not found 
  - E.g. `app_version: ${__ENV__:APP_VERSION=0.0.0}` where `app_version` 
    will be `0.0.0` if `APP_VERSION` is not found on the system as an 
    environment variable)


## [2.4.0] - 2021-07-29

### Fixed

- A rare but serious error where nested internal referencing with multiple 
  variables would break prematurely in files that extend others with the same 
  keys


## [2.3.0] - 2021-07-27

### Added

- The `raw_load` method that loads a config file and returns the raw 
  `dict` result
  - This is mainly intended to be used for debugging large and complex sets 
    of config files with multiple inclusions and extensions and internal 
    references and such, so that reading in the files and seeing the 
    resulting structure after everything has been included and evaluated can 
    help.
- The `render_load` method that loads a config file and returns the 
  rendered `str` result (JSON or YAML depending on the input file)
  - This is mainly intended to be used for debugging large and complex sets 
    of config files with multiple inclusions and extensions and internal 
    references and such, so that reading in the files and seeing the 
    resulting JSON or YAML after everything has been included and evaluated can 
    help, as if this was just one large file with static values.


## [2.2.0] - 2021-07-27

### Added

- The `unmaksed` param (default=`False`) to the `as_json`, `as_yaml` and 
  `as_dict` methods in order to use `alviss` to load and render config and 
  export as a single "compiled" file e.g. for deployment manifests and such


## [2.1.1] - 2021-07-26

### Fixed

- Issue with resolution order of extended keys with variables
- Issue with resolving variables in entries with nested keys collapsed into 
  one string


## [2.1.0] - 2021-07-26

### Added

- Support for multiple files in `__extends__` keys
- Support for nested `__extends__` keys
- Support for using `__extends__` and `__include__` in collapsed keys
- Aliases:
  - `__extend__` => `__extends__`
  - `__includes__` => `__include__`


## [2.0.0] - 2021-07-26

### Added

 - YAML support _(YAY! Now we can properly document/comment in config files!)_
 - New `quickloader` module
 - Support for extending base files via `__extends__` key
 - Support for including additional files via `__include__` key
 - Better config representation _(e.g. for logs)_ via `as_json()` and 
   `as_yaml()` methods
 - Internal reference variable resolving via `${keys}`
 - Support for collapsing multiple nested keys into a single key with dots 
   like so: `database.connection.host`
 - Support for documentation keys in JSON files via the "comment-like" 
   `__doc__` key
 - Way to "comment-out" any keys in JSON by ignoring any keys starting with 
   a double underscore.
 - Support for including environment variables into any value string, 
   wherever in that string

### Changed

- The format for environment variable inclusion to `${__ENV__:SOME_ENV_VAR}`
- Refactored structure _(just `from alviss.quickloader import *` and go)_

### Removed

- The singleton functionality of `BaseConfig` by default and moved it over to 
  `SingletonConfig`


## [1.3.0] - 2020-11-18

### Changed 

- The CI/CD pipelines


## [1.2.1] - 2019-07-19

### Changed 

- If something in config starts with "_", it's no longer printed


## [1.2.0] - 2019-07-11 

### Changed 

- Requirements and version bump due to bug in dependency


## [1.1.1] - 2019-05-21

### Fixed

- A bug from `typeutils.iters.nested_dict_update` that didn't
  update the nested parts of nested `EmptyDict`


## [1.1.0] - 2019-05-21

### Changed

- The `update` to use `nested_dict_update` from `typeutils` 2.5+ so
 config value updates can be updated safely in a nested way e.g. in
 order to have a base config file and then a much smaller override
 config file
- The `__str__` and `__repr__` and calls so they now mask out secrets and 
  passwords _(any keys with the following words in them: 'pass', 'key', 
  'secret', 'token')_


## [1.0.0] - 2019-02-20

Initial release

### Added

- Everything!
