# Movie Night
Simple server that syncs video playback for clients using Movie Night.

## Requirements

* Python 3.7

Virtual environment should be created before installing or bundling the application.
```shell script
python -m venv venv
venv\Scripts\activate
```

## Install in editable mode

`-e` allows editing the application without having to reinstall it.
```shell script
pip install -e .
movienightserver
```

## Codestyle

This project uses [Black](https://github.com/psf/black) for code formatting.

```shell script
pip install black
black .
```
