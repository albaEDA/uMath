[![Build Status][travis-img]][travis-repo] [![Coverage Status][coveralls-img]][coveralls-repo]
[travis-img]:  https://travis-ci.org/AaronKel/uMath.svg?branch=master
[travis-repo]: https://travis-ci.org/AaronKel/uMath
[coveralls-img]:  https://coveralls.io/repos/AaronKel/uMath/badge.svg?branch=master
[coveralls-repo]: https://coveralls.io/r/AaronKel/uMath?branch=master

<p align="center">
  <a href="https://github.com/AaronKel/uMath/wiki">Wiki</a> |
  <a href="https://github.com/AaronKel/uMath/issues">Issues</a> |
  <a href="#">Documentation</a>
  <br><br>
  <img src="https://github.com/AaronKel/uMath/blob/master/uMath-logo.png" data-canonical-src="https://github.com/AaronKel/uMath/blob/master/uMath-logo.png" width="200" />
</p>

This project aims to bring a feature rich computer algebra system (CAS) to the microcontroller world and provide a platform for an open source graphing calculator.

## Installation

Currently source is being tested on a custom Unix version of the micropython project that needs atleast 120Kb of RAM to run. When the project is more fleshed out and is ported fully from Python.

## Usage

Using μMath will be farmilliar to anyone using other CAS systems on python
```
>from umath import *
>x = symbols('x')
>(x*x).simplify()
x**2
```

## Contributing

See <a href="https://github.com/AaronKel/uMath/wiki">Wiki</a> on contributing guidelines

## History

Based on the Symath project by Brandon Niemczyk, 2012 for Python 2.
It was then ported to Python 3 by Aaron Kelly, 2017 and currently
work is undergoing to allow it to run on some of the cheaper STM or
ESP8266 modules with MicroPython, hence renaming it to uMath(MicroMath).

## Authours

Brandon Niemczyk

Aaron Kelly

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
