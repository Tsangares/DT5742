### Description
Utilities that I wrote while working with the caen digitizers. These utilites are meant to be used with the files produced from Caen's wavedump software.


The files at this time include one main utility file called `caen.py`. The other files are all command line utilites that are used for quick analysis of the data.
The command line utilities include a binary or ascii to json writer, `writer.py`, a quick plotter called `plotter.py` and a square wave counter called `counter.py`.

To use the library clone the repo. Later I will make a pip package.

# Examples

Using `plotter.py`:

    python plotter.py -o 1000 -t 10000 wave_0.dat

Using `writer.py`:

    python writer.py -t 5 wave_0.dat output.json

Using `counter.py`:

    python3 counter.py wave_0.txt 