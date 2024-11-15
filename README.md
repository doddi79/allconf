# AllConf the All-Knowing Config Reader

Generic Configuration file reader/parser with a bunch of nifty extra 
features, most notably:

- File Inclusion & Extension
- Internal variable reference parsing
- Nested fault-tolerant fetching of non-existing values
- Environment variable embedding
- On-demand external secret credential embedding _(untested in this new fork thus far)_
- Python script result embedding
- Single-file rendering of parsed config file (via CLI)
- Python dataclass stub generation (via CLI)
- JSON, YAML & custom support
- ...and more


## Note

This was forked from the [`alviss`](https://github.com/ccpgames/allconf) package
in order to continue development and support. 

## The TL;DR...

Given this `my_cfg.yaml` config file example:

```yaml
app:
  name: MyApp
  environment: dev
  log_level: INFO
```

This is how you load and use it with `allconf`:

```python
from allconf import quickloader

cfg = quickloader.autoload('my_cfg.yaml')

assert cfg.app.name == 'MyApp'
assert cfg.app.environment == 'dev'
assert cfg.app.log_level == 'INFO'
```

And that's basically it really!

Read on for description of more features in order of "quality of life" impact 
for you as a programmer _(as gauged by myself)_ and it goes more or less like this:

1. File Inclusion & Extension
2. Internal variable reference parsing
3. Nested fault-tolerant fetching of non-existing values
4. Environment variable embedding
5. On-demand external secret credential embedding _(untested in this new fork thus far)_
6. Python script result embedding
7. Single-file rendering of parsed config file (via CLI)
8. Python dataclass stub generation (via CLI)
9. JSON, YAML & custom support

...I'll document this later!

Check out the (`_OLD_README.md`)[_OLD_README.md] file for the old documentation (which may or may not be up to date)!
