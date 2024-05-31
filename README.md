# Ninam

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ninam)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ninam)


Ninam is a steganography tool to encode or decode a payload in a text file by replacing white space character.
I created this programme because I remembered when I was younger that I liked to send people secret messages by hiding them in a text message.

## How it works ? 

All spaces in the text are recovered and replaced by other [unicode space characters](https://en.wikipedia.org/wiki/Whitespace_character). If there is not enough space available, additional spaces will be added at the end. 
You can use 1-bit, 2-bit or 4-bit encoding. This means using 2, 4 or 16 white spaces. The larger the bitsize, the larger your payload can be, but at the risk of having slightly suspicious white spaces.


## Installation 

There is no dependencies and should work with all version of python>3.x

```bash
pip install ninam
```

## Usage 

``` bash  
    # By default, it used 2 bits
    ninam encode -i input.txt -p iloveyou > output.txt
    ninam decode -i output.txt 

    # Alternative bitsize
    ninam encode -b 4 -i input.txt -p iloveyou > output.txt
    ninam decode -b 4 -i output.txt  
    
```

## From git 

```
git clone git@github.com:dridk/ninam.git
python -m ninam 
```


