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
