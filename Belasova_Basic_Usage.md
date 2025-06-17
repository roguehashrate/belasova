# Belasova Language Basic Usage

## Overview

Belasova is a simple, statically typed language designed to be friendly and easy to read. It focuses on clear syntax with no fuss, making it great for learning programming fundamentals and experimenting with ideas.

Currently, Belasova supports:

- Variable declarations with explicit types  
- Basic arithmetic and string operations  
- Function declarations and calls (with type signatures)  
- Input and output via `getLine` and `puts`  
- Control flow via `if`, `else`, and the brand-new `check`-`when` expressions  
- Blocks that **always** end with `end` — consistency is king here!

---

## Variables

Declare variables using `let` with explicit types:

```belasova
let name :: String <- getLine      -- assign from input
let age :: Int = 30                -- assign directly
let height :: Double = 1.75
```

- Use `<-` when assigning from input or expressions that return values (like `getLine`)  
- Use `=` when assigning directly from expressions  

---

## Input and Output

- Use `getLine` to read a line of user input (always a `String`).  
- Use `puts` to print text or values to the console.

Example:

```belasova
puts "Enter your name:"
let name :: String <- getLine
puts "Hello, " ++ name ++ "!"
```

---

## Functions

Functions are declared with `fn` and a detailed type signature. Function bodies **must** be ended with `end` (we like consistency!).

```belasova
fn add x y :: Int -> Int ->> Int
add x y = x + y
end
```

- The signature syntax: `fn <name> <param1> <param2> :: -> <Type1> -> <Type2> ->> <ReturnType>`  
- The function body repeats the name and parameters, then an `=` followed by the expression  
- Functions are called like: `let result :: Int = add 5 10`

---

## Operators

- Arithmetic: `+`, `-`, `*`, `/`  
- String concatenation: `++`

Example:

```belasova
let fullName :: String = firstName ++ " " ++ lastName
```

---

## Control Flow

Belasova’s main control structures currently use `if`, `else`, and `end`. For now, no `else if` or `elif` — just multiple `if`s and a final `else` for simplicity.

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

### Bonus: `check` with `when`

Inspired by pattern matching, `check` lets you test a value against multiple `when` cases with an optional `else` fallback:

```belasova
check mood:
    when 1:
        puts "Happy"
    when 2:
        puts "Sad"
    else:
        puts "Meh"
end
```

---

## Sample Program: BMI Calculator (Freedom Units)

```belasova
puts "Welcome to Belasova BMI Calculator!"

puts "What is your name?"
let name :: String <- getLine

puts "Enter your weight in pounds (LBs)"
let weight :: Double <- getLine

puts "Enter your height (ft)"
let feet :: Int <- getLine

puts "Enter extra inches (Ex. 6ft 2in, 5ft 3in)"
let inches :: Int <- getLine

let heightInches :: Int = (feet * 12) + inches

fn calculateBMI weight heightInches :: Double -> Int ->> Double
calculateBMI weight heightInches = (weight * 703) / (heightInches * heightInches)
end

let bmi :: Double = calculateBMI weight heightInches

puts "Hello, " ++ name ++ "!"
puts "Your BMI is: " ++ bmi ++ "."
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

## Sample Program: Basic Calculator

```belasova
fn add x y :: Int -> Int ->> Int
add x y = x + y
end

fn sub x y :: Int -> Int ->> Int
sub x y = x - y
end

fn multiply x y :: Int -> Int ->> Int
multiply x y = x * y
end

fn divide x y :: Int -> Int ->> Int
divide x y = x / y
end

puts "Please enter your first number: "
let numOne :: Int <- getLine

puts "Please enter your operation (+, -, *, /): "
let userOp :: String <- getLine

puts "Please enter your second number: "
let numTwo :: Int <- getLine

if userOp == "+" then:
    puts add numOne numTwo
if userOp == "-" then:
    puts sub numOne numTwo
if userOp == "*" then:
    puts multiply numOne numTwo
if userOp == "/" then:
    puts divide numOne numTwo
else:
    puts "You entered something wrong, be sure to enter (+, -, * or /)"
end
```

---

If you’ve read this far — congrats! 🎉 Belasova is growing bit by bit, so keep an eye out for new features, and happy coding!

---
