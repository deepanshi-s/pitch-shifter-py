# Python Pitch Shifter
> Take an input .wav file and shift the pitch at the mentioned time interval without
> changing the speed or length of the input file.

## Install

Require: Python 3.7+

```
$ git clone https://github.com/cwoodall/pitch-shifter-py.git
$ cd pitch-shifter-py
```


## Usage


```
$ python pitchshifter/pitchshifter.py -s ./samples/sample1.wav -o out.wav -p 0.4 -b 1 -st 0.5 -et 1.5
```

```

## Basic Algorithm Flow

```
Input --> Phase Vocoder (Stretch or compress by 2^(n/12)) --> resample by 2^(n/12)
```

