# μSyMath

This project aims to bring a feature rich computer algebra system (CAS) to the microcontroller world and provide a platform for an open source graphing calculator.

## Installation

Currently source works on a custom Unix version of the micropython project that needs atleast 120Kb of RAM to run. When the project is more fleshed out and is ported fully from Python.

## Usage

Using μSymath will be farmilliar to anyone using other CAS systems on python
```
>from Symath import *
>x = symbols('x')
>(x*x).simplify()
x**2
```

## Contributing

See Wiki on contributing guidelines

## History

Based on the Symath project by Brandon Niemczyk, 2012 for Python 2.
It was then ported to Python 3 by Aaron Kelly, 2017 and currently
work is undergoing to allow it to run on some of the cheaper STM or
ESP8266 modules.

## Credits

Brandon Niemczyk
Aaron Kelly

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
