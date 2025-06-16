# Belasova Language Basic Usage

## Overview

Belasova is a simple, statically typed language designed for ease of use with a focus on clear syntax. It supports:

* Variable declarations with explicit types
* Basic arithmetic and string operations
* Function declarations and calls
* Input and output with `getLine` and `puts`
* Basic control flow (More to come!)

---

## Variables

Declare variables using `let`, with explicit type annotations:

```belasova
let name :: String <- getLine
let age :: Int = 30
let height :: Double = 1.75
```

* Use `<-` to assign from input or expressions returning values.
* Use `=` for direct assignment of expressions.

---

## Input and Output

* Use `getLine` to read a line of input as a string.
* Use `puts` to output to the console.

Example:

```belasova
puts "Enter your name:"
let name :: String <- getLine
puts "Hello, " ++ name ++ "!"
```

---

## Functions

Define functions with the `fn` keyword:

```belasova
fn add x y -> Int -> Int ->> Int
add x y = x + y
```

* The function signature syntax: `fn <name> <param1> <param2> ... -> <Type1> -> <Type2> ->> <ReturnType>`
* Function body follows with `<name> <params> = <expression>`
* Functions can be called like: `let result :: Int = add 5 10`

---

## Operators

* Arithmetic: `+`, `-`, `*`, `/`
* String concatenation: `++`

Example:

```belasova
let fullName :: String = firstName ++ " " ++ lastName
```

---

## Control Flow

As of writing this document, there is only one real way to do control flow, which is `(if, else, end)`.

```belasova
puts "Enter a number:"
let num :: Int <- getLine

if num == 1 then:
    puts "You entered one."

if num == 2 then:
    puts "You entered two."

if num == 3 then:
    puts "You entered three."

else:
    puts "Number other than 1, 2 or 3"
end
```

There is no `else if` or `elif` in Belasova, only `if` and `else`. This is a decision made for the sake of simplification.

---

## Sample Program: BMI Calculator (Freedom Units)

```belasova
puts "Welcome to Belasova BMI Calculator!"

puts "What is your name?"
let name :: String <- getLine

puts "Enter your weight in pounds:"
let weight :: Double <- getLine

puts "Enter your height (feet):"
let feet :: Int <- getLine

puts "Enter your height (inches):"
let inches :: Int <- getLine

let heightInches :: Int = (feet * 12) + inches

fn calculateBMI weight heightInches :: Double -> Int ->> Double
calculateBMI weight heightInches = (weight * 703) / (heightInches * heightInches)

let bmi :: Double = calculateBMI weight heightInches

puts "Hello, " ++ name ++ "!"
puts "Your BMI is " ++ bmi ++ "."

```

---

## Sample Program: BMI Calculator (Metric Units)

```belasova
puts "Welcome to Belasova BMI Calculator!"

puts "What is your name?"
let name :: String <- getLine

puts "Enter your weight in kilograms:"
let weight :: Double <- getLine

puts "Enter your height in meters:"
let height :: Double <- getLine

let bmi :: Double = weight / (height * height)

puts "Hello, " ++ name ++ "!"
puts "Your BMI is " ++ bmi ++ "."
```

---

If you read all the way to the end, awesome — happy you found it interesting! I plan to continue updating this as much as I can, adding more functionality and making it more usable.
