# Change Log

## Version 0.7.0

### Highlights

This release exports all functions in `matplotlib.pyplot` to `latexplotlib`. This means you can use `lpl` as a drop-in replacement for `plt`and you don't have to import `matplotlib.pyplot` if you import latexplotlib. Also, there is finally a changelog 🎉

### Code
- export `plt` functions in latexplotlib
- test new behavior and test that no functions beside `plt.subplots` are overridden

### Readme
- update to reflect `plt->lpl` changes
- add changelog
- updated example code to reflect new changes

## Version 0.8.0

- support for python 3.12
- deprecate python 3.7 support
- decrease all font sizes by 2. With the previous style, the labels where far to big compared to the surrounding text.

## Version 0.8.1

- improve docstring of `lpl.suplots`
- improve logic of `lpl.subplots`
- improve tooling:
    - add yaml formatting to pre-commit
    - add other minor pre-commit hooks
    - fix ruff config
    - add dependabot for github workflows
    - add mypy-lsp config
- fix previously unnoticed ruff errors
- update badges

## Version 0.8.2

- update `lpl.subplots` docstring
- typing: allow both floats and ints as widths and height

### Development
- remove unused packages from environment.yml
- add requirements.txt

## Version 0.8.3

- bugfix: fix bug introduced in 0.8.1, where 'width_ratios' and 'height_ratios' were silently overwritten


## Version 0.9.0

- deprecated python 3.8 support
- deprecate `fraction` and `ratio` argument of `lpl.subplots`

### Development
- add tests for bugfix introduced in 0.8.3
