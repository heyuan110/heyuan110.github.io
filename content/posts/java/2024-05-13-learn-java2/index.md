+++
date = '2024-05-13T15:13:10+08:00'
title = 'Java Tutorial Part 2: Arrays Utility, Lambda Expressions, Regex, and Sorting Algorithms'
description = 'A hands-on Java tutorial covering the Arrays utility class, Lambda expressions, method references, regular expressions, exception handling, and classic sorting and searching algorithms with code examples.'
toc = true
tags = ['Java', 'Arrays', 'Collections', 'IO', 'Tutorial']
categories = ['Java']
keywords = ['Java Arrays class', 'Java Lambda expressions', 'Java regex', 'Java sorting algorithms', 'binary search Java', 'method reference Java']
+++
![image](java-logo.webp)

[Continued from Part 1: Java Tutorial (Part 1)](../2024-05-05-learn-java)



## 7. Collections & I/O Fundamentals

### 1. The Arrays Utility Class

The `java.util.Arrays` class is a utility class designed to make common array operations -- traversal, copying, sorting -- simple and convenient.

![Arrays utility class overview](image-20240513154259542.webp)

```java
/**
 * Demonstrating commonly used methods in the Arrays class
 */
public class ArraysTest1 {
    public static void main(String[] args) {
        // 1. Arrays.toString() - Returns a string representation of the array
        int[] arr = {10, 20, 30, 40, 50, 60};
        System.out.println(Arrays.toString(arr));

        // 2. Arrays.copyOfRange() - Copies a range of elements (inclusive start, exclusive end)
        int[] arr2 = Arrays.copyOfRange(arr, 1, 4);
        System.out.println(Arrays.toString(arr2));

        // 3. Arrays.copyOf() - Copies array with a specified new length
        int[] arr3 = Arrays.copyOf(arr, 10);
        System.out.println(Arrays.toString(arr3));

        // 4. Arrays.setAll() - Transforms each element using a generator function
        double[] prices = {99.8, 128, 100};
        // Apply a 20% discount to every price
        Arrays.setAll(prices, new IntToDoubleFunction() {
            @Override
            public double applyAsDouble(int value) {
                return prices[value] * 0.8;
            }
        });
        System.out.println(Arrays.toString(prices));

        // 5. Arrays.sort() - Sorts the array in ascending order by default
        Arrays.sort(prices);
        System.out.println(Arrays.toString(prices));
    }
}
```

#### Sorting Arrays of Custom Objects

What if the array contains custom objects instead of primitives? There are two approaches.

First, prepare a `Student` class:

![Student class definition](image-20240513201707503.webp)

And a test class:

![Test class setup](image-20240513201726944.webp)

![Test class continued](image-20240513201741499.webp)

**Approach 1: Implement `Comparable`**

Have the `Student` class implement the `Comparable` interface and override `compareTo`. Under the hood, `Arrays.sort()` uses the return value of `compareTo` (positive, negative, or zero) to determine ordering.

![Comparable implementation](image-20240513201935902.webp)

**Approach 2: Pass a `Comparator`**

Call `Arrays.sort(array, comparator)` and pass a `Comparator` object as the second argument. The sort method uses the `compare` method's return value to determine element ordering.

![Comparator implementation](image-20240513201953518.webp)

### 2. Lambda Expressions

Lambda expressions provide a concise way to write anonymous inner classes. The basic syntax is:

```
(parameter list) -> {
    method body;
}
```

**Important**: Lambda expressions only work with *functional interfaces* -- interfaces that have exactly one abstract method. They cannot be used with abstract classes.

Here is a functional interface example:

![Functional interface example](image-20240514164413431.webp)

Using a `Swimming` functional interface, let's compare anonymous inner class syntax with Lambda:

```java
public class LambdaTest1 {
    public static void main(String[] args) {
        // 1. Traditional anonymous inner class
        Swimming s = new Swimming(){
             @Override
             public void swim() {
                 System.out.println("Student swims happily~~~~");
             }
         };
         s.swim();

        // 2. Simplified with Lambda expression
        Swimming s1 = () -> {
              System.out.println("Student swims happily~~~~");
        };
        s1.swim();
    }
}
```

#### Lambda Shorthand Forms

```
1. Standard form
    (Type1 param1, Type2 param2) -> {
        ...method body...
        return value;
    }

2. Omit parameter types (type inference)
    (param1, param2) -> {
        ...method body...
        return value;
    }

3. Single-statement body: omit braces, return keyword, and semicolon
    (param1, param2) -> expression

4. Single parameter: omit parentheses
    param -> expression
```

```java
public class LambdaTest2 {
    public static void main(String[] args) {
        double[] prices = {99.8, 128, 100};

        // 1. Anonymous inner class
        Arrays.setAll(prices, new IntToDoubleFunction() {
            @Override
            public double applyAsDouble(int value) {
                return prices[value] * 0.8;
            }
        });

        // 2. Lambda - standard form
        Arrays.setAll(prices, (int value) -> {
                return prices[value] * 0.8;
        });

        // 3. Lambda - omit parameter type
        Arrays.setAll(prices, (value) -> {
            return prices[value] * 0.8;
        });

        // 4. Lambda - omit parentheses (single parameter)
        Arrays.setAll(prices, value -> {
            return prices[value] * 0.8;
        });

        // 5. Lambda - omit braces (single expression)
        Arrays.setAll(prices, value -> prices[value] * 0.8 );

        System.out.println(Arrays.toString(prices));

        System.out.println("------------------------------------

        Student[] students = new Student[4];
        students[0] = new Student("Spider", 169.5, 23);
        students[1] = new Student("Alice", 163.8, 26);
        students[2] = new Student("Alice", 163.8, 26);
        students[3] = new Student("Bob", 167.5, 24);

        // 1. Anonymous inner class
        Arrays.sort(students, new Comparator<Student>() {
            @Override
            public int compare(Student o1, Student o2) {
                return Double.compare(o1.getHeight(), o2.getHeight()); // ascending
            }
        });

        // 2. Lambda - standard form
        Arrays.sort(students, (Student o1, Student o2) -> {
                return Double.compare(o1.getHeight(), o2.getHeight());
        });

        // 3. Lambda - omit parameter types
        Arrays.sort(students, ( o1,  o2) -> {
            return Double.compare(o1.getHeight(), o2.getHeight());
        });

        // 4. Lambda - single expression, omit braces
        Arrays.sort(students, ( o1,  o2) -> Double.compare(o1.getHeight(), o2.getHeight()));

        System.out.println(Arrays.toString(students));
    }
}
```

### 3. Static Method References

Start with this setup code:

![Setup code](image-20240514190954442.webp)

Replace the Lambda body with a static method call:

![Lambda with method call](image-20240514191015332.webp)

Create a helper class `CompareByData` to encapsulate the comparison logic:

![CompareByData class](image-20240514191034312.webp)

Now the Lambda body delegates to the static method:

![Delegating to static method](image-20240514191057872.webp)

Java allows you to simplify this further using a **static method reference**:

![Static method reference](image-20240514191126054.webp)

The syntax is `ClassName::methodName` -- you reference the method by name and let Java figure out the parameters. That is the essence of a static method reference.

### 4. Instance Method References

Add an instance method to `CompareByData` that encapsulates the Lambda body:

![Instance method in CompareByData](image-20240514191314555.webp)

Call it through an object instance:

![Calling through an object](image-20240514191350761.webp)

Simplify with an instance method reference:

![Instance method reference](image-20240514191406033.webp)

The syntax is `object::methodName`. This is an **instance method reference** -- the parameters are inferred automatically.

### 5. Particular-Type Method References

```
Java convention:
    When a Lambda expression calls an instance method where the first parameter
    serves as the method's caller and all remaining parameters are passed as
    arguments, you can use a particular-type method reference.

Syntax:
    Type::methodName
```

This is purely a syntactic convenience -- there is no deep underlying principle. When you encounter this pattern, just apply the shorthand.

![Particular-type method reference example](image-20240514191803903.webp)

### 6. Regular Expressions

Regular expressions (regex) are patterns built from special characters that define matching rules.

![Regex syntax overview](image-20240514202320880.webp)

In Java, the `String.matches(String regex)` method checks whether a string matches a given regex pattern.

![matches method API](image-20240514202357334.webp)

Here is a comprehensive demonstration of regex rules in Java:

```java
/**
 * Demonstrating Java regular expression rules
 */
public class RegexTest2 {
    public static void main(String[] args) {
        // 1. Character classes (match a single character)
        System.out.println("a".matches("[abc]"));    // [abc] matches only a, b, or c
        System.out.println("e".matches("[abcd]")); // false

        System.out.println("d".matches("[^abc]"));   // [^abc] matches anything except a, b, c
        System.out.println("a".matches("[^abc]"));  // false

        System.out.println("b".matches("[a-zA-Z]")); // [a-zA-Z] matches any letter
        System.out.println("2".matches("[a-zA-Z]")); // false

        System.out.println("k".matches("[a-z&&[^bc]]")); // a-z excluding b and c
        System.out.println("b".matches("[a-z&&[^bc]]")); // false

        System.out.println("ab".matches("[a-zA-Z0-9]")); // false - character classes match only ONE character

        // 2. Predefined character classes (match a single character): .  \d  \D  \s  \S  \w  \W
        System.out.println("X".matches(".")); // . matches any single character
        System.out.println("XX".matches(".")); // false

        System.out.println("\"");
        System.out.println("3".matches("\\d"));  // \d matches a digit [0-9]
        System.out.println("a".matches("\\d"));  // false

        System.out.println(" ".matches("\\s"));   // \s matches a whitespace character
        System.out.println("a".matches("\s")); // false

        System.out.println("a".matches("\\S"));  // \S matches a non-whitespace character
        System.out.println(" ".matches("\\S")); // false

        System.out.println("a".matches("\\w"));  // \w matches [a-zA-Z_0-9]
        System.out.println("_".matches("\\w")); // true
        System.out.println("!".matches("\\w")); // false

        System.out.println("!".matches("\\W"));  // \W matches [^\w]
        System.out.println("a".matches("\\W"));  // false

        System.out.println("23232".matches("\\d")); // false - predefined classes match only ONE character

        // 3. Quantifiers: ?  *  +  {n}  {n,}  {n,m}
        System.out.println("a".matches("\\w?"));   // ? means 0 or 1 time
        System.out.println("".matches("\\w?"));    // true
        System.out.println("abc".matches("\\w?")); // false

        System.out.println("abc12".matches("\\w*"));   // * means 0 or more times
        System.out.println("".matches("\\w*"));        // true
        System.out.println("abc12!".matches("\\w*")); // false

        System.out.println("abc12".matches("\\w+"));   // + means 1 or more times
        System.out.println("".matches("\\w+"));       // false
        System.out.println("abc12!".matches("\\w+")); // false

        System.out.println("a3c".matches("\\w{3}"));   // {3} means exactly 3 times
        System.out.println("abcd".matches("\\w{3}"));  // false
        System.out.println("abcd".matches("\\w{3,}"));     // {3,} means 3 or more
        System.out.println("ab".matches("\\w{3,}"));     // false
        System.out.println("abcde!".matches("\\w{3,}"));     // false
        System.out.println("abc232d".matches("\\w{3,9}"));   // {3,9} means 3 to 9 times

        // 4. Other useful constructs: (?i) case-insensitive, | alternation, () grouping
        System.out.println("abc".matches("(?i)abc")); // true
        System.out.println("ABC".matches("(?i)abc")); // true
        System.out.println("aBc".matches("a((?i)b)c")); // true
        System.out.println("ABc".matches("a((?i)b)c")); // false

        // Match either 3 lowercase letters or 3 digits
        System.out.println("abc".matches("[a-z]{3}|\\d{3}")); // true
        System.out.println("ABC".matches("[a-z]{3}|\\d{3}")); // false
        System.out.println("123".matches("[a-z]{3}|\\d{3}")); // true
        System.out.println("A12".matches("[a-z]{3}|\\d{3}")); // false

        // Grouping example with repeating groups
        System.out.println("ILoveCodeCode666666".matches("ILove(Code)+(666)+"));
        System.out.println("ILoveCodeCode66666".matches("ILove(Code)+(666)+"));
    }
}
```

- Validating phone numbers with regex

![Phone number validation](image-20240514202514681.webp)

- Validating email addresses with regex

![Email validation](image-20240514202529625.webp)

- Extracting information (web scraping patterns)

![Information extraction](image-20240514202600438.webp)

- Search and replace

The `String` class provides methods for replacement and splitting using regex:

![String replace and split methods](image-20240514202716011.webp)

![Search and replace example](image-20240514202732454.webp)

### 7. Exception Handling

Java provides a rich hierarchy of exception classes to describe problems that arise at runtime. These classes share common characteristics, which is why they form an inheritance hierarchy.

![Exception hierarchy diagram](image-20240514203208158.webp)

There are two main approaches to handling exceptions:

![Exception handling approaches](image-20240514203420725.webp)



## 8. Algorithms

An algorithm is a step-by-step process for solving a specific problem. When learning algorithms, first understand the logic, then work out the implementation.

### 1. Bubble Sort

Bubble sort works by repeatedly stepping through the list, comparing adjacent elements, and swapping them if they are in the wrong order. Each pass "bubbles" the largest unsorted element to its correct position.

![Bubble sort flow diagram](image-20240514192750063.webp)

![Bubble sort code](image-20240514192759413.webp)

### 2. Selection Sort

Selection sort divides the array into a sorted and unsorted region. In each round, it selects the smallest (or largest) element from the unsorted region and moves it to the end of the sorted region.

![Selection sort flow diagram](image-20240514194325731.webp)

![Selection sort basic code](image-20240514194348476.webp)

The code above can be optimized. Instead of swapping array values multiple times inside the inner loop, track only the index of the minimum element, then perform a single swap after the inner loop completes. This reduces the number of swaps and improves performance:

![Optimized selection sort](image-20240514194701660.webp)

### 3. Search Algorithms

**Linear Search**: The simplest approach -- iterate from index 0 and check each element one by one. If the target element is near the end of a large array, this becomes very slow.

![Linear search illustration](image-20240514194821983.webp)

**Binary Search**: A far more efficient approach that eliminates half the remaining elements with each comparison. **However, binary search requires the array to be sorted beforehand.**

The core algorithm:

```
Step 1: Define two variables: left (start index) and right (end index)
Step 2: Calculate the middle index: mid = (left + right) / 2
Step 3: Compare the element at mid with the target key:
    - If arr[mid] < key: everything before mid is also smaller
        => set left = mid + 1
    - If arr[mid] > key: everything after mid is also larger
        => set right = mid - 1
    - If arr[mid] == key: found it!
        => return mid

Repeat steps 1-3 until left > right. If the target is never found, return -1.
```

![Binary search flow diagram](image-20240514195008357.webp)

![Binary search code](image-20240514195540022.webp)

## 9. Network Programming & Multithreading

*(Coming soon)*

## 10. JDK Features & Advanced Fundamentals

*(Coming soon)*

## 11. Java Web

*(Coming soon)*

---
## *References*

[Java Developer Learning Path](https://yun.itheima.com/subject/javamap/index.html)

[Java Fundamentals Video Tutorial (Bilibili)](https://www.bilibili.com/video/BV1Cv411372m/?spm_id_from=333.999.0.0)

[Java Tutorial (YouTube)](https://www.youtube.com/watch?v=VqfGCmjQt10)

[JavaWeb Development Tutorial (Bilibili)](https://www.bilibili.com/video/BV1m84y1w7Tb/?vd_source=4d819443886ce5506c7c6b65b4a7ad93)
