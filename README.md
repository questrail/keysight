# keysight

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[keysight][] is a Python (2.6+/3.3+) package providing modules and helpers to
work with data files from [Keysight Technologies][key] (formerly
Agilent/HP) test equipment.

## Dependencies

### Runtime Dependencies

- [numpy][]

### Development Dependencies

- [invoke][]
- [nose][]
- [unipath][]

## Support Keysight Equipment

### Spectrum Analyzers
Below are the modules available in the keysight package and the
compatible equipment for each module:

- n9340: N9340 spectrum analyzer
- e4411b: E4411B, E4402B spectrum analyzers

## Contributing

### Sample CSV and other data files

Currently, the only sample files tested are the CSV files from a N9340B
and E4411B spectrum analyzer. If you have other data files saved from a
Keysight/Agilent/HP piece of test equipment and are willing to share it,
please open an issue or submit a pull request to let us know.

### Submitting Pull Requests

[keysight][] is developed using [Scott Chacon][]'s [GitHub Flow][]. To
contribute, fork [keysight][], create a feature branch, and then submit
a pull request.  [GitHub Flow][] is summarized as:

- Anything in the `master` branch is deployable
- To work on something new, create a descriptively named branch off of
  `master` (e.g., `new-oauth2-scopes`)
- Commit to that branch locally and regularly push your work to the same
  named branch on the server
- When you need feedback or help, or you think the brnach is ready for
  merging, open a [pull request][].
- After someone else has reviewed and signed off on the feature, you can
  merge it into master.
- Once it is merged and pushed to `master`, you can and *should* deploy
  immediately.

## Testing

## License

[keysight] is released under the MIT license. Please see the
[LICENSE.txt] file for more information.

[key]: http://www.keysight.com/
[keysight]: https://github.com/questrail/keysight
[coveralls image]: http://img.shields.io/coveralls/questrail/keysight/master.svg
[coveralls link]: https://coveralls.io/r/questrail/keysight
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[invoke]: http://www.pyinvoke.org
[LICENSE.txt]: https://github.com/questrail/keysight/blob/develop/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/keysight.svg
[nose]: http://nose.readthedocs.io/en/latest/
[numpy]: http://www.numpy.org
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: http://img.shields.io/pypi/v/keysight.svg
[pypi ver link]: https://pypi.python.org/pypi/keysight
[python standard library]: https://docs.python.org/2/library/
[scott chacon]: http://scottchacon.com/about.html
[siganalysis]: https://github.com/questrail/siganalysis
[travis image]: http://img.shields.io/travis/questrail/keysight/master.svg
[travis link]: https://travis-ci.org/questrail/keysight
[unipath]: https://github.com/mikeorr/Unipath
