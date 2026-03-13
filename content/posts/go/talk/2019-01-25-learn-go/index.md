+++
date = '2019-01-25T21:13:19+08:00'
title = 'Go Language Tutorial: Fundamentals of Golang Syntax and Data Types'
description = 'A beginner-friendly Go (Golang) tutorial covering language features like easy deployment, built-in concurrency, and strong performance. Learn Go program structure, basic syntax, data types, variables, constants, operators, control flow, functions, pointers, structs, slices, maps, interfaces, error handling, goroutines, and channels.'
toc = true
tags = ['Go', 'Golang', '入门教程', '编程语言']
categories = ['Go']
keywords = ['Go tutorial', 'Golang basics', 'Go syntax', 'Go data types', 'Go concurrency', 'goroutines', 'Go channels']
+++
![image](/images/learn-golang/go.webp)

## Introduction

Go (also known as Golang) is an open-source programming language developed by Google in 2007. It was publicly announced on November 10, 2009, and Go 1.0 was released in early 2012. Today, Go development is fully open source with a thriving community behind it.

Go stands out for its **simple deployment, excellent concurrency support, clean language design, and strong runtime performance**.

## 1. Go Program Structure

A Go program is made up of the following building blocks:

- Package declaration
- Import statements
- Functions
- Variables
- Statements and expressions
- Comments

Here is a minimal example:

```go
// Declare the package name
package main

// Import the fmt package
import "fmt"

// Define a function; main is the entry point
func main() {
   /* This is my first simple program */
   fmt.Println("Hello, World!")
}
```

## 2. Basic Syntax

- **Line separator**: Each line represents a complete statement; no semicolons needed
- **Comments**: Single-line with `//`, multi-line with `/* */`
- **Identifiers**: Used to name variables, types, and other entities. Must start with a letter or underscore, not a digit
- **Keywords**: Go has 25 reserved keywords
![](/images/learn-golang/15483971756507.webp)
And 36 predefined identifiers:
![](/images/learn-golang/15483972014339.webp)
- **Whitespace**: Use spaces between declarations and around operators for readability

### 2.1 Data Types

Data types determine how much memory a variable occupies and what operations are allowed on it.

Go organizes its data types into several categories:

- **Boolean** (`bool`)

A boolean can only be `true` or `false`. Example: `var b bool = true`

- **Numeric types**

Integer types (`int`) and floating-point types (`float32`, `float64`).

Integer types include:
![](/images/learn-golang/15483985088545.webp)

Floating-point types:
![](/images/learn-golang/15483985320227.webp)

Other numeric types:
![](/images/learn-golang/15483985582507.webp)

- **String type**

A string is a sequence of bytes connected end to end. In Go, strings are composed of individual bytes using UTF-8 encoding to represent Unicode text.

- **Derived types**
    - Pointer
    - Array
    - Struct
    - Channel
    - Function
    - Slice
    - Interface
    - Map

### 2.2 Variables

Variable names consist of letters, digits, and underscores. The first character cannot be a digit.

There are three ways to declare a variable:

- Specify the type explicitly; if no value is assigned, the zero value is used:

```go
var v_name v_type
v_name = value
```

- Let Go infer the type from the assigned value: `var v_name = value`
- Use the short declaration operator `:=` (the variable on the left must not have been declared previously):

```go
v_name := value
// For example:
x := 10
```

Multiple variable declarations:

```go
var vname1, vname2, vname3 type
vname1, vname2, vname3 = v1, v2, v3

// Type inference (similar to Python)
var vname1, vname2, vname3 = v1, v2, v3

// Short declaration (variables must not already be declared)
vname1, vname2, vname3 := v1, v2, v3

// Factored declaration, commonly used for global variables
var (
    vname1 v_type1
    vname2 v_type2
)
```

Note: A declared local variable that is never used will cause a compile error.

### 2.3 Constants

Constants are identifiers whose values cannot change at runtime. Only boolean, numeric, and string types are allowed.

- Declaration syntax: `const identifier [type] = value`

```go
// Explicit type
const b string = "abc"
// Implicit type (inferred)
const b = "abc"

// Examples
const LENGTH int = 10
const WIDTH = 10
```

- Constants can serve as enumerations:

```go
const (
    Unknown = 0
    Female  = 1
    Male    = 2
)
```

- Constants can be computed using built-in functions such as `len()`, `cap()`, and `unsafe.Sizeof()`:

```go
package main

import "unsafe"
const (
    a = "abc"
    b = len(a)
    c = unsafe.Sizeof(a)
)

func main(){
    println(a, b, c)
}
```

- **The `iota` constant**

`iota` is a special constant that the compiler increments automatically. It resets to 0 whenever the `const` keyword appears, and increases by 1 for each subsequent line within the const block. Think of it as the line index within a `const` block.

Using `iota` for enumerations:

```go
const (
    a = iota // 0
    b = iota // 1
    c = iota // 2
)
// Shorthand (iota is implicit after the first usage)
const (
    a = iota
    b
    c
)
```

### 2.4 Operators

- **Arithmetic operators** (assuming A = 10, B = 20):
![](/images/learn-golang/15484031841274.webp)

- **Relational operators** (assuming A = 10, B = 20):
![](/images/learn-golang/15484032595654.webp)

- **Logical operators** (assuming A = true, B = false):
![](/images/learn-golang/15484033088693.webp)

- **Bitwise operators** (assuming A = 60, B = 13):
![](/images/learn-golang/15484034266782.webp)

Note: Right-shifting by n bits is equivalent to dividing by 2^n, but this does not hold for negative numbers.

Truth table for `&`, `|`, and `^`:
![](/images/learn-golang/15484035756694.webp)

Binary representations of A = 60 and B = 13:
![](/images/learn-golang/15484036026004.webp)

- **Assignment operators**:
![](/images/learn-golang/15484039516433.webp)

- **Other operators** (address-of `&` and dereference `*`):
![](/images/learn-golang/15484039839342.webp)

    ```go
    package main

    import "fmt"

    func main() {
       var a int = 4
       var b int32
       var c float32
       var ptr *int

       fmt.Printf("Line 1 - type of a = %T\n", a)
       fmt.Printf("Line 2 - type of b = %T\n", b)
       fmt.Printf("Line 3 - type of c = %T\n", c)

       ptr = &a    // ptr holds the address of a
       fmt.Printf("Value of a: %d\n", a)
       fmt.Printf("Value of *ptr: %d\n", *ptr)
    }
    ```

- **Operator precedence**

Binary operators are evaluated left to right. The table below lists operators from highest to lowest precedence:

![](/images/learn-golang/15484105551893.webp)

You can use parentheses to override the default precedence.

### 2.5 Conditional Statements

Control flow diagram:
![](/images/learn-golang/15484106537473.webp)

Go provides the following conditional constructs:
![](/images/learn-golang/15484106379972.webp)

Examples with `if...else` and `switch`:

```go
   if a < 20 {
       fmt.Printf("a is less than 20\n")
   } else {
       fmt.Printf("a is not less than 20\n")
   }

   switch {
      case grade == "A":
         fmt.Printf("Excellent!\n")
      case grade == "B", grade == "C":
         fmt.Printf("Good\n")
      case grade == "D":
         fmt.Printf("Pass\n")
      case grade == "F":
         fmt.Printf("Fail\n")
      default:
         fmt.Printf("Poor\n")
   }
```

The `select` statement is a control structure similar to `switch`, but designed for channel communication. Each case must be a send or receive operation. Go randomly picks a runnable case; if none is ready, it blocks until one becomes available. A `default` clause is always runnable.

### 2.6 Loops

Loop flow diagram:
![](/images/learn-golang/15484112508588.webp)

Go's `for` loop comes in three forms:

- `for init; condition; post { }`
- `for condition { }`
- `for { }` (infinite loop)

Where `init` is the initializer, `condition` is the loop condition, and `post` is the post-iteration statement.

The `for...range` form iterates over slices, maps, arrays, and strings:

```
for key, value := range oldMap {
    newMap[key] = value
}
```

Full example:

```go
package main

import "fmt"

func main() {

   var b int = 15
   var a int

   numbers := [6]int{1, 2, 3, 5}

   // Classic for loop
   for a := 0; a < 10; a++ {
      fmt.Printf("Value of a: %d\n", a)
   }

   // While-style loop
   for a < b {
      a++
      fmt.Printf("Value of a: %d\n", a)
   }

   // Range-based loop
   for i, x := range numbers {
      fmt.Printf("Index %d, value = %d\n", i, x)
   }
}
```

### 2.7 Functions

Functions are the basic building blocks of a Go program. Every Go program has at least one function: `main()`.

- **Function definition**:

```
func function_name( [parameter list] ) [return_types] {
   // function body
}
```

`func` introduces the declaration. The function name and parameter list together form the function signature. Parameters act as placeholders for values passed at call time. Return types specify the types of the returned values; they can be omitted if the function returns nothing.

Example:

```go
// Returns the larger of two numbers
func max(num1, num2 int) int {
   var result int

   if num1 > num2 {
      result = num1
   } else {
      result = num2
   }
   return result
}
```

- **Multiple return values**:

```go
package main

import "fmt"

func swap(x, y string) (string, string) {
   return y, x
}

func main() {
   a, b := swap("Mahesh", "Kumar")
   fmt.Println(a, b)
}
```

- **Function parameters**

Go supports two argument-passing mechanisms:

(a) **Pass by value**: The function receives a copy of the argument.

```go
func swap(x, y int) int {
   var temp int
   temp = x
   x = y
   y = temp
   return temp
}
```

(b) **Pass by reference** (using pointers): The function receives a pointer to the original variable.

```go
func swap(x *int, y *int) {
   var temp int
   temp = *x
   *x = *y
   *y = temp
}
```

- **Advanced function usage**

(a) **Functions as values**: Functions can be assigned to variables.

```go
package main

import (
   "fmt"
   "math"
)

func main(){
   getSquareRoot := func(x float64) float64 {
      return math.Sqrt(x)
   }
   fmt.Println(getSquareRoot(9))
}
```

(b) **Closures**: Anonymous functions that capture variables from their enclosing scope.

```go
package main

import "fmt"

func getSequence() func() int {
   i := 0
   return func() int {
      i += 1
      return i
   }
}

func main(){
   nextNumber := getSequence()

   fmt.Println(nextNumber()) // 1
   fmt.Println(nextNumber()) // 2
   fmt.Println(nextNumber()) // 3

   // A new closure with its own state
   nextNumber1 := getSequence()
   fmt.Println(nextNumber1()) // 1
   fmt.Println(nextNumber1()) // 2
}
```

(c) **Methods**: Functions with a receiver argument, attached to a specific type.

Syntax:

```
func (variable_name variable_data_type) function_name() [return_type]{
   // method body
}
```

Example:

```go
package main

import "fmt"

type Circle struct {
  radius float64
}

func main() {
  var c1 Circle
  c1.radius = 10.00
  fmt.Println("Area of circle =", c1.getArea())
}

// This method belongs to the Circle type
func (c Circle) getArea() float64 {
  return 3.14 * c.radius * c.radius
}
```

### 2.8 Variable Scope

Go has three levels of variable scope:

- Local variables (declared inside a function)
- Global variables (declared outside all functions)
- Formal parameters (function arguments)

### 2.9 Arrays

An array is a fixed-length, numbered sequence of elements of a single type. Elements are accessed by index, starting at 0.
![](/images/learn-golang/15487334966945.webp)

- **Declaration**: `var variable_name [SIZE] variable_type`

For example, an array of 10 float32 values: `var balance [10] float32`

- **Initialization**:

The number of elements in `{}` must not exceed the number in `[]`.

```go
var balance = [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
```

You can let Go count the elements automatically:

```go
var balance = [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
```

- **Reading and writing elements**:

```go
package main

import "fmt"

func main() {
   var n [10]int
   var i, j int

   for i = 0; i < 10; i++ {
      n[i] = i + 100
   }

   for j = 0; j < 10; j++ {
      fmt.Printf("Element[%d] = %d\n", j, n[j])
   }
}
```

- **Multidimensional arrays**: `var variable_name [SIZE1][SIZE2]...[SIZEN] variable_type`

Example: `var threedim [5][10][4]int`

Initializing a 2D array:

```go
a = [3][4]int{
 {0, 1, 2, 3},
 {4, 5, 6, 7},
 {8, 9, 10, 11},
}
```

Full example:

```go
package main

import "fmt"

func main() {
   var a = [5][2]int{{0,0}, {1,2}, {2,4}, {3,6}, {4,8}}
   var i, j int

   for i = 0; i < 5; i++ {
      for j = 0; j < 2; j++ {
         fmt.Printf("a[%d][%d] = %d\n", i, j, a[i][j])
      }
   }
}
```

### 2.10 Pointers

- **Definition**

A pointer variable stores the memory address of another variable. Declaration syntax: `var var_name *var-type`

```go
var ip *int        // pointer to int
var fp *float32    // pointer to float32
```

```go
package main

import "fmt"

func main() {
   var a int = 20
   var ip *int

   ip = &a // ip now holds the address of a

   fmt.Printf("Address of a: %x\n", &a)
   fmt.Printf("Address stored in ip: %x\n", ip)
   fmt.Printf("Value at *ip: %d\n", *ip)
}
```

- **Nil pointers**

An uninitialized pointer has the value `nil` (also called a null pointer).

```go
package main

import "fmt"

func main() {
   var ptr *int
   fmt.Printf("Value of ptr: %x\n", ptr)
}
```

Checking for nil:

```go
if ptr != nil { /* ptr is not nil */ }
if ptr == nil { /* ptr is nil */ }
```

- **Arrays of pointers**:

```go
package main

import "fmt"

const MAX int = 3

func main() {
   a := []int{10, 100, 200}
   var i int
   var ptr [MAX]*int

   for i = 0; i < MAX; i++ {
      ptr[i] = &a[i]
   }

   for i = 0; i < MAX; i++ {
      fmt.Printf("a[%d] = %d\n", i, *ptr[i])
   }
}
```

- **Pointer to pointer**

A pointer to a pointer stores the address of another pointer variable.
![](/images/learn-golang/15487422095707.webp)

Declaration: `var ptr **int`

Accessing the value requires double dereferencing:

```go
package main

import "fmt"

func main() {
   var a int
   var ptr *int
   var pptr **int

   a = 3000
   ptr = &a
   pptr = &ptr

   fmt.Printf("Value of a = %d\n", a)
   fmt.Printf("Value at *ptr = %d\n", *ptr)
   fmt.Printf("Value at **pptr = %d\n", **pptr)
}
```

- **Pointers as function arguments**

Pass a pointer to allow the function to modify the original variable:

```go
package main

import "fmt"

func main() {
   var a int = 100
   var b int = 200

   fmt.Printf("Before swap: a = %d\n", a)
   fmt.Printf("Before swap: b = %d\n", b)

   swap(&a, &b)

   fmt.Printf("After swap: a = %d\n", a)
   fmt.Printf("After swap: b = %d\n", b)
}

func swap(x *int, y *int) {
   var temp int
   temp = *x
   *x = *y
   *y = temp
}
```

### 2.11 Structs

A struct is a composite data type that groups together fields of different types.

While arrays store elements of the same type, structs let you define different data types for each field.

- **Defining a struct**:

```go
type struct_variable_type struct {
   member1 type1
   member2 type2
   ...
}
```

The `struct` keyword defines a new data type with one or more members. The `type` keyword assigns a name to it.

- **Using a struct**:

```go
package main

import "fmt"

type Books struct {
   title   string
   author  string
   subject string
   book_id int
}

func main() {
    // Positional initialization
    fmt.Println(Books{"Go Language", "example.com", "Go Tutorial", 6495407})

    // Named field initialization
    fmt.Println(Books{title: "Go Language", author: "example.com", subject: "Go Tutorial", book_id: 6495407})

    // Omitted fields default to zero values
    fmt.Println(Books{title: "Go Language", author: "example.com"})
}
```

- **Accessing struct members** with the `.` operator:

```go
package main

import "fmt"

type Books struct {
   title   string
   author  string
   subject string
   book_id int
}

func main() {
   var Book1 Books
   var Book2 Books

   Book1.title = "Go Language"
   Book1.author = "example.com"
   Book1.subject = "Go Tutorial"
   Book1.book_id = 6495407

   Book2.title = "Python Tutorial"
   Book2.author = "example.com"
   Book2.subject = "Python Guide"
   Book2.book_id = 6495700

   fmt.Printf("Book 1 title: %s\n", Book1.title)
   fmt.Printf("Book 1 author: %s\n", Book1.author)
   fmt.Printf("Book 1 subject: %s\n", Book1.subject)
   fmt.Printf("Book 1 book_id: %d\n", Book1.book_id)

   fmt.Printf("Book 2 title: %s\n", Book2.title)
   fmt.Printf("Book 2 author: %s\n", Book2.author)
   fmt.Printf("Book 2 subject: %s\n", Book2.subject)
   fmt.Printf("Book 2 book_id: %d\n", Book2.book_id)
}
```

- **Structs as function arguments**:

```go
package main

import "fmt"

type Books struct {
   title   string
   author  string
   subject string
   book_id int
}

func main() {
   var Book1 Books
   Book1.title = "Go Language"
   Book1.author = "example.com"
   Book1.subject = "Go Tutorial"
   Book1.book_id = 6495407

   printBook(Book1)
}

func printBook(book Books) {
   fmt.Printf("Book title: %s\n", book.title)
   fmt.Printf("Book author: %s\n", book.author)
   fmt.Printf("Book subject: %s\n", book.subject)
   fmt.Printf("Book book_id: %d\n", book.book_id)
}
```

- **Struct pointers**:

Declare a pointer to a struct: `var struct_pointer *Books`

Get the address with `&`: `struct_pointer = &Book1`

Access members through a pointer using `.` (same as with a value): `struct_pointer.title`

```go
package main

import "fmt"

type Books struct {
   title   string
   author  string
   subject string
   book_id int
}

func main() {
   var Book1 Books
   Book1.title = "Go Language"
   Book1.author = "example.com"
   Book1.subject = "Go Tutorial"
   Book1.book_id = 6495407

   printBook(&Book1)
}

func printBook(book *Books) {
   fmt.Printf("Book title: %s\n", book.title)
   fmt.Printf("Book author: %s\n", book.author)
   fmt.Printf("Book subject: %s\n", book.subject)
   fmt.Printf("Book book_id: %d\n", book.book_id)
}
```

### 2.12 Slices

A slice is an abstraction over arrays. Unlike arrays, slices have a dynamic length and can grow using `append`. Think of them as Go's version of dynamic arrays.

- **Declaring a slice**: `var identifier []type` (no size specified)

Or use `make()`:

```go
var slice1 []type = make([]type, len)
// Shorthand
slice1 := make([]type, len)
```

You can also specify an optional capacity: `make([]T, length, capacity)`

- **Initializing a slice**:

    **a.** Direct initialization: `s := []int{1, 2, 3}` creates a slice with `cap == len == 3`

    **b.** From an array: `s := arr[:]` creates a slice referencing the entire array

    ```
    s := arr[startIndex:endIndex]  // elements from startIndex to endIndex-1
    s := arr[startIndex:]          // from startIndex to end
    s := arr[:endIndex]            // from beginning to endIndex-1
    ```

    **c.** From another slice: `s1 := s[startIndex:endIndex]`

    **d.** Using `make()`: `s := make([]int, len, cap)`

- **Slice operations**:

Use `len()` to get the current length and `cap()` to get the maximum capacity. An uninitialized slice is `nil` with length 0.

```go
package main
import "fmt"

func main() {
   var numbers = make([]int, 3, 5)
   printSlice(numbers)

   var numbers2 []int
   printSlice(numbers2)
   if numbers2 == nil {
      fmt.Printf("slice is nil")
   }
}

func printSlice(x []int){
   fmt.Printf("len=%d cap=%d slice=%v\n", len(x), cap(x), x)
}
```

To grow a slice beyond its capacity, create a new larger slice and copy the contents. Use `append()` to add elements and `copy()` to duplicate a slice:

```go
package main

import "fmt"

func main() {
   var numbers []int
   printSlice(numbers)

   numbers = append(numbers, 0)
   printSlice(numbers)

   numbers = append(numbers, 1)
   printSlice(numbers)

   numbers = append(numbers, 2, 3, 4)
   printSlice(numbers)

   // Create a new slice with double the capacity
   numbers1 := make([]int, len(numbers), cap(numbers)*2)
   copy(numbers1, numbers)
   printSlice(numbers1)
}

func printSlice(x []int){
   fmt.Printf("len=%d cap=%d slice=%v\n", len(x), cap(x), x)
}
```

Sub-slicing with `[lower:upper]`:

```go
package main

import "fmt"

func main() {
   numbers := []int{0,1,2,3,4,5,6,7,8}
   printSlice(numbers)

   fmt.Println("numbers ==", numbers)
   fmt.Println("numbers[1:4] ==", numbers[1:4])
   fmt.Println("numbers[:3] ==", numbers[:3])
   fmt.Println("numbers[4:] ==", numbers[4:])

   numbers1 := make([]int, 0, 5)
   printSlice(numbers1)

   number2 := numbers[:2]
   printSlice(number2)

   number3 := numbers[2:5]
   printSlice(number3)
}

func printSlice(x []int){
   fmt.Printf("len=%d cap=%d slice=%v\n", len(x), cap(x), x)
}
```

### 2.13 Range

The `range` keyword iterates over arrays, slices, channels, or maps in a `for` loop. For arrays and slices, it returns the index and value. For maps, it returns each key-value pair.

```go
package main

import "fmt"

func main() {
    // Sum a slice using range
    nums := []int{2, 3, 4}
    sum := 0
    for _, num := range nums {
        sum += num
    }
    fmt.Println("sum:", sum)

    // Use the index when needed
    for i, num := range nums {
        if num == 3 {
            fmt.Println("index:", i)
        }
    }

    // Range over a map
    kvs := map[string]string{"a": "apple", "b": "banana"}
    for k, v := range kvs {
        fmt.Printf("%s -> %s\n", k, v)
    }

    // Range over a string (yields index and Unicode code point)
    for i, c := range "go" {
        fmt.Println(i, c)
    }
}
```

### 2.14 Maps

A map is an unordered collection of key-value pairs, providing fast lookups by key.

- **Declaring a map**:

```go
// Declare a map variable (nil by default, cannot store data)
var map_variable map[key_data_type]value_data_type

// Create a usable map with make
map_variable := make(map[key_data_type]value_data_type)
```

An uninitialized map is `nil` and cannot be used to store key-value pairs.

Example:

```go
package main

import "fmt"

func main() {
    var countryCapitalMap map[string]string
    countryCapitalMap = make(map[string]string)

    countryCapitalMap["France"] = "Paris"
    countryCapitalMap["Italy"] = "Rome"
    countryCapitalMap["Japan"] = "Tokyo"
    countryCapitalMap["India"] = "New Delhi"

    for country := range countryCapitalMap {
        fmt.Println(country, "capital is", countryCapitalMap[country])
    }

    // Check if a key exists
    capital, ok := countryCapitalMap["United States"]
    if ok {
        fmt.Println("Capital of United States is", capital)
    } else {
        fmt.Println("Capital of United States not found")
    }
}
```

- **The `delete()` function** removes an element from a map:

```go
package main

import "fmt"

func main() {
    countryCapitalMap := map[string]string{
        "France": "Paris",
        "Italy":  "Rome",
        "Japan":  "Tokyo",
        "India":  "New Delhi",
    }

    fmt.Println("Original map:")
    for country := range countryCapitalMap {
        fmt.Println(country, "capital is", countryCapitalMap[country])
    }

    delete(countryCapitalMap, "France")
    fmt.Println("\nAfter deleting France:")
    for country := range countryCapitalMap {
        fmt.Println(country, "capital is", countryCapitalMap[country])
    }
}
```

### 2.15 Interfaces

An interface defines a set of method signatures. Any type that implements all those methods satisfies the interface.

- **Defining an interface**:

```go
type interface_name interface {
   method_name1() return_type
   method_name2() return_type
}
```

Example:

```go
package main

import "fmt"

type Phone interface {
    call()
}

type NokiaPhone struct{}

func (nokiaPhone NokiaPhone) call() {
    fmt.Println("I am Nokia, I can call you!")
}

type IPhone struct{}

func (iPhone IPhone) call() {
    fmt.Println("I am iPhone, I can call you!")
}

func main() {
    var phone Phone

    phone = new(NokiaPhone)
    phone.call()

    phone = new(IPhone)
    phone.call()
}
```

### 2.16 Error Handling

Go provides a simple error-handling mechanism through the built-in `error` interface:

```go
type error interface {
    Error() string
}
```

Functions typically return an error as their last return value. Use `errors.New` to create error values:

```go
func Sqrt(f float64) (float64, error) {
    if f < 0 {
        return 0, errors.New("math: square root of negative number")
    }
    // implementation
}
```

Custom error example:

```go
package main

import "fmt"

type DivideError struct {
    dividee int
    divider int
}

func (de *DivideError) Error() string {
    strFormat := `
    Cannot proceed, the divider is zero.
    dividee: %d
    divider: 0
`
    return fmt.Sprintf(strFormat, de.dividee)
}

func Divide(varDividee int, varDivider int) (result int, errorMsg string) {
    if varDivider == 0 {
        dData := DivideError{
            dividee: varDividee,
            divider: varDivider,
        }
        errorMsg = dData.Error()
        return
    } else {
        return varDividee / varDivider, ""
    }
}

func main() {
    if result, errorMsg := Divide(100, 10); errorMsg == "" {
        fmt.Println("100/10 =", result)
    }
    if _, errorMsg := Divide(100, 0); errorMsg != "" {
        fmt.Println("errorMsg is:", errorMsg)
    }
}
```

### 2.17 Concurrency

Go has built-in concurrency support through goroutines. Simply prefix a function call with the `go` keyword to run it in a new goroutine.

A goroutine is a lightweight thread managed by the Go runtime. All goroutines in a program share the same address space.

Syntax: `go functionName(args)`

```go
package main

import (
        "fmt"
        "time"
)

func say(s string) {
        for i := 0; i < 5; i++ {
                time.Sleep(100 * time.Millisecond)
                fmt.Println(s)
        }
}

func main() {
        go say("world")
        say("hello")
}
```

### 2.18 Channels

A channel is a typed conduit for passing data between goroutines. The `<-` operator specifies the channel direction (send or receive). If no direction is given, the channel is bidirectional.
![](/images/learn-golang/15487532812467.webp)

Declare a channel with the `chan` keyword. Channels must be created before use:
![](/images/learn-golang/15487533241343.webp)

By default, channels are unbuffered: the sender blocks until the receiver is ready, and vice versa.

Example -- summing numbers with two goroutines:

```go
package main

import "fmt"

func sum(s []int, c chan int) {
        sum := 0
        for _, v := range s {
                sum += v
        }
        c <- sum
}

func main() {
        s := []int{7, 2, 8, -9, 4, 0}

        c := make(chan int)
        go sum(s[:len(s)/2], c)
        go sum(s[len(s)/2:], c)
        x, y := <-c, <-c

        fmt.Println(x, y, x+y)
}
```

- **Buffered channels**

You can create a buffered channel by passing a capacity as the second argument to `make`:
![](/images/learn-golang/15487536331518.webp)

Buffered channels decouple the sender and receiver: the sender can write to the buffer without the receiver being immediately ready. However, once the buffer is full, the sender blocks until the receiver drains some values.

**Key rule**: An unbuffered channel blocks the sender until the receiver reads. A buffered channel blocks the sender only when the buffer is full. The receiver always blocks until a value is available.

```go
package main

import "fmt"

func main() {
        // Buffered channel with capacity 2
        ch := make(chan int, 2)

        ch <- 1
        ch <- 2

        fmt.Println(<-ch)
        fmt.Println(<-ch)
}
```

- **Iterating and closing channels**

Use `range` to read from a channel until it is closed:
![](/images/learn-golang/15487543745937.webp)

When no more data will be sent, close the channel with `close()`.

```go
package main

import "fmt"

func fibonacci(n int, c chan int) {
        x, y := 0, 1
        for i := 0; i < n; i++ {
                c <- x
                x, y = y, x+y
        }
        close(c)
}

func main() {
        c := make(chan int, 10)
        go fibonacci(cap(c), c)
        // range reads from c until it is closed
        for i := range c {
                fmt.Println(i)
        }
}
```

## 3. References

[1. Go by Example](https://gobyexample.com)
