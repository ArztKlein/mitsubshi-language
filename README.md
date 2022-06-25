# Mitsubishi Language
An [Estoteric Language](https://en.wikipedia.org/wiki/Esoteric_programming_language) consisting of functions named after Mitsubishi Companies.

Mitsubishi Language is designed to be general purpose, however not practical.

## Installation/Running
### Prerequisites
- Python 3 must be installed.
- All the required packages in the requirements.txt
### Installation
To install Mitsubishi Language, clone this repository.  
`git clone https://github.com/ArztKlein/mitsubshi-language.git`

### Running
cd into `mitsubishi_language`.

To open the interpreter, run the following:

#### Windows:  
`py -m mitsubishi_language`

## Usage
Mitsubishi Language Services are what would be called functions in a regular programming language. Services only take one argument, and may return a value.

Values are moved from service to service (piping) using an insert "->" operator.

## Services
### Mitsubishi Electric Printer
Will print the input to the console.

## Hello World Example
In this example, a string is created, and then piped into `mitsubishi electric printer`, which is a service that will print to the console.
```
"Hello, world!"->mitsubishi electric printer
```

## Variables
The Mitsubishi language is weakly typed.
Variables are prefixed with an @ (at) symbol. Unlike services, variables are not allowed to have a space in their name.  
*Put text into a variable, and then print it*
```
"Hello, world"->@variable_name
@variable_name->mitsubishi electric printer
```

Another example that will ask the user for their name, store it into a variable, then print "Your name is: " with the name.
```
"What is your name? "->mitsubishi keyboard->@name
"Your name is: " + @name->mitsubishi electric printer
```
