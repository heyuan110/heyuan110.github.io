+++
date = '2026-01-23T20:07:08+08:00'
draft = false
title = 'TypeScript Complete Guide: From Basics to Advanced Type System Mastery'
description = 'A comprehensive TypeScript tutorial covering basic syntax, advanced types, generics, type gymnastics, utility types, and best practices with real-world code examples.'
toc = true
images = ['cover.webp']
tags = ['TypeScript', 'JavaScript', 'Frontend', 'Type System']
categories = ['AI Guides']
keywords = ['TypeScript', 'TypeScript tutorial', 'TypeScript advanced types', 'TypeScript generics', 'type gymnastics', 'utility types']
+++

![TypeScript Complete Guide: From Basics to Advanced Type System Mastery](cover.webp)

**TypeScript** is a typed superset of JavaScript that adds a static type system to the language. It catches errors at compile time, provides superior IDE support, and makes code significantly easier to maintain. This guide walks through every core concept in TypeScript — from fundamental syntax to advanced type-level programming — so you can go from beginner to expert.

> In 2025, Microsoft announced a rewrite of the TypeScript compiler in Go, delivering a 10x speedup and 50% memory reduction. TypeScript continues to gain ground over plain JavaScript and has become an essential skill for modern frontend development.

---

## 1. TypeScript Fundamentals

### Why TypeScript?

| Feature | JavaScript | TypeScript |
|---------|------------|------------|
| Type checking | Runtime | Compile time |
| IDE support | Basic | Excellent (IntelliSense, refactoring) |
| Maintainability | Lower | High |
| Learning curve | Low | Moderate |
| Large project suitability | Fair | Excellent |

### Installation and Setup

```bash
# Global install
npm install -g typescript

# Project install
npm install typescript --save-dev

# Initialize config file
npx tsc --init

# Compile a single file
tsc hello.ts

# Watch mode
tsc --watch
```

### tsconfig.json Essentials

```json
{
  "compilerOptions": {
    // Target ECMAScript version
    "target": "ES2020",
    // Module system
    "module": "ESNext",
    // Strict mode (strongly recommended)
    "strict": true,
    // Output directory
    "outDir": "./dist",
    // Source directory
    "rootDir": "./src",
    // Generate declaration files
    "declaration": true,
    // Allow importing JSON
    "resolveJsonModule": true,
    // ES module interop
    "esModuleInterop": true,
    // Skip library type checks (faster compilation)
    "skipLibCheck": true,
    // Strict null checks
    "strictNullChecks": true,
    // Disallow implicit any
    "noImplicitAny": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

---

## 2. Primitive and Basic Types

### Primitive Types

```typescript
// String
let name: string = "TypeScript";

// Number (integers and floats are both number)
let age: number = 25;
let price: number = 99.99;

// Boolean
let isDone: boolean = false;

// null and undefined
let n: null = null;
let u: undefined = undefined;

// Symbol
let sym: symbol = Symbol("key");

// BigInt (ES2020)
let big: bigint = 100n;
```

### Array Types

```typescript
// Syntax 1: type[]
let numbers: number[] = [1, 2, 3];
let strings: string[] = ["a", "b", "c"];

// Syntax 2: Array<type> (generic form)
let nums: Array<number> = [1, 2, 3];

// Readonly array
let readonlyArr: readonly number[] = [1, 2, 3];
// readonlyArr.push(4); // Error: cannot modify a readonly array
```

### Tuples

Tuples are arrays with a fixed length and specific types at each position:

```typescript
// Basic tuple
let tuple: [string, number] = ["hello", 42];

// Optional elements
let optionalTuple: [string, number?] = ["hello"];

// Rest elements
let restTuple: [string, ...number[]] = ["hello", 1, 2, 3];

// Readonly tuple
let readonlyTuple: readonly [string, number] = ["hello", 42];

// Named tuples (TypeScript 4.0+)
type NamedTuple = [name: string, age: number];
let person: NamedTuple = ["Alice", 30];
```

### Enums

```typescript
// Numeric enum (defaults start from 0)
enum Direction {
  Up,      // 0
  Down,    // 1
  Left,    // 2
  Right    // 3
}

// Custom starting value
enum Status {
  Pending = 1,
  Active,     // 2
  Inactive    // 3
}

// String enum
enum Color {
  Red = "RED",
  Green = "GREEN",
  Blue = "BLUE"
}

// const enum (inlined at compile time for better performance)
const enum HttpStatus {
  OK = 200,
  NotFound = 404,
  ServerError = 500
}

// Usage
let dir: Direction = Direction.Up;
let status: HttpStatus = HttpStatus.OK; // compiles directly to 200
```

### any, unknown, never, and void

```typescript
// any: disables type checking (avoid when possible)
let anything: any = "hello";
anything = 42;
anything.foo(); // no error, but may crash at runtime

// unknown: safer alternative to any
let unknown1: unknown = "hello";
// unknown1.foo(); // Error: must check the type first
if (typeof unknown1 === "string") {
  console.log(unknown1.toUpperCase()); // OK
}

// void: no return value
function log(msg: string): void {
  console.log(msg);
}

// never: function never returns (throws or infinite loop)
function throwError(msg: string): never {
  throw new Error(msg);
}

function infiniteLoop(): never {
  while (true) {}
}
```

**Key comparison: any vs unknown**

| Property | any | unknown |
|----------|-----|---------|
| Type safety | Unsafe | Safe |
| Assignable to other types | Yes | Requires assertion or type guard |
| Call methods/properties | Yes (no errors) | Must narrow the type first |
| Use case | Quick migration, third-party libs | Accepting values of uncertain type |

---

## 3. Function Types

### Function Declarations

```typescript
// Function declaration
function add(a: number, b: number): number {
  return a + b;
}

// Function expression
const multiply = function(a: number, b: number): number {
  return a * b;
};

// Arrow function
const divide = (a: number, b: number): number => a / b;

// Full function type annotation
const subtract: (a: number, b: number) => number = (a, b) => a - b;
```

### Optional and Default Parameters

```typescript
// Optional parameter (must come after required ones)
function greet(name: string, greeting?: string): string {
  return `${greeting || "Hello"}, ${name}!`;
}

// Default parameter
function greetWithDefault(name: string, greeting: string = "Hello"): string {
  return `${greeting}, ${name}!`;
}

// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}

sum(1, 2, 3, 4, 5); // 15
```

### Function Overloads

When a function returns different types based on its arguments, use overloads:

```typescript
// Overload signatures
function format(value: string): string;
function format(value: number): string;
function format(value: Date): string;

// Implementation signature
function format(value: string | number | Date): string {
  if (typeof value === "string") {
    return value.trim();
  } else if (typeof value === "number") {
    return value.toFixed(2);
  } else {
    return value.toISOString();
  }
}

format("  hello  "); // "hello"
format(3.14159);     // "3.14"
format(new Date());  // "2025-01-23T..."
```

### The this Parameter

```typescript
interface User {
  name: string;
  greet(this: User): void;
}

const user: User = {
  name: "Alice",
  greet() {
    console.log(`Hello, ${this.name}`);
  }
};

user.greet(); // OK
// const greet = user.greet;
// greet(); // Error: incorrect this context
```

---

## 4. Interfaces and Type Aliases

### Interfaces

```typescript
// Basic interface
interface Person {
  name: string;
  age: number;
}

// Optional properties
interface Config {
  host: string;
  port?: number;
}

// Readonly properties
interface Point {
  readonly x: number;
  readonly y: number;
}

// Index signatures
interface StringArray {
  [index: number]: string;
}

interface Dictionary {
  [key: string]: any;
}

// Callable interface
interface SearchFunc {
  (source: string, keyword: string): boolean;
}

const search: SearchFunc = (source, keyword) => {
  return source.includes(keyword);
};
```

### Interface Inheritance

```typescript
interface Animal {
  name: string;
}

interface Dog extends Animal {
  breed: string;
}

// Multiple inheritance
interface Bird extends Animal {
  fly(): void;
}

interface Parrot extends Animal, Bird {
  speak(): void;
}
```

### Type Aliases

```typescript
// Basic type alias
type ID = string | number;
type Name = string;

// Object type
type User = {
  id: ID;
  name: Name;
  email: string;
};

// Union type
type Status = "pending" | "active" | "inactive";

// Intersection type
type Admin = User & {
  role: "admin";
  permissions: string[];
};

// Function type
type Callback = (data: string) => void;

// Generic type alias
type Container<T> = {
  value: T;
};
```

### Interface vs Type: When to Use Which

This is one of the most common questions in TypeScript interviews.

| Feature | interface | type |
|---------|-----------|------|
| Extension | extends | & (intersection) |
| Declaration merging | Supported | Not supported |
| Computed properties | Not supported | Supported |
| Union types | Not supported | Supported |
| Mapped types | Not supported | Supported |

```typescript
// Interface declaration merging
interface User {
  name: string;
}
interface User {
  age: number;
}
// Merged result: { name: string; age: number }

// Type cannot be merged
type Person = { name: string };
// type Person = { age: number }; // Error: duplicate identifier

// Type supports union types
type StringOrNumber = string | number;
// Interface cannot directly define union types
```

**Best practices:**
- Defining object shapes or class contracts: use `interface`
- Defining unions, tuples, or mapped types: use `type`
- Need declaration merging (e.g., extending third-party library types): use `interface`

---

## 5. Classes

### Basic Class Definition

```typescript
class Person {
  // Property declarations
  name: string;
  age: number;

  // Constructor
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  // Method
  greet(): string {
    return `Hello, I'm ${this.name}`;
  }
}

const person = new Person("Alice", 30);
```

### Access Modifiers

```typescript
class Employee {
  public name: string;         // Public (default)
  protected department: string; // Protected (accessible in subclasses)
  private salary: number;      // Private (class-internal only)
  readonly id: number;         // Readonly

  constructor(name: string, department: string, salary: number, id: number) {
    this.name = name;
    this.department = department;
    this.salary = salary;
    this.id = id;
  }
}

// Shorthand with parameter properties
class Employee2 {
  constructor(
    public name: string,
    protected department: string,
    private salary: number,
    readonly id: number
  ) {}
}
```

### Getters and Setters

```typescript
class Circle {
  private _radius: number = 0;

  get radius(): number {
    return this._radius;
  }

  set radius(value: number) {
    if (value < 0) {
      throw new Error("Radius cannot be negative");
    }
    this._radius = value;
  }

  get area(): number {
    return Math.PI * this._radius ** 2;
  }
}

const circle = new Circle();
circle.radius = 5;
console.log(circle.area); // 78.54...
```

### Static Members

```typescript
class MathUtils {
  static PI = 3.14159;

  static square(x: number): number {
    return x * x;
  }

  static cube(x: number): number {
    return x ** 3;
  }
}

console.log(MathUtils.PI);        // 3.14159
console.log(MathUtils.square(4)); // 16
```

### Abstract Classes

```typescript
abstract class Shape {
  abstract area(): number;       // Subclasses must implement
  abstract perimeter(): number;

  // Concrete method (inherited by subclasses)
  describe(): string {
    return `Area: ${this.area()}, Perimeter: ${this.perimeter()}`;
  }
}

class Rectangle extends Shape {
  constructor(private width: number, private height: number) {
    super();
  }

  area(): number {
    return this.width * this.height;
  }

  perimeter(): number {
    return 2 * (this.width + this.height);
  }
}

// const shape = new Shape(); // Error: cannot instantiate an abstract class
const rect = new Rectangle(10, 5);
console.log(rect.describe()); // "Area: 50, Perimeter: 30"
```

### Implementing Interfaces

```typescript
interface Printable {
  print(): void;
}

interface Loggable {
  log(message: string): void;
}

class Document implements Printable, Loggable {
  print(): void {
    console.log("Printing document...");
  }

  log(message: string): void {
    console.log(`[LOG] ${message}`);
  }
}
```

---

## 6. Generics

Generics are one of TypeScript's most powerful features, enabling you to write reusable, type-safe components.

### Generic Functions

```typescript
// Basic generic function
function identity<T>(arg: T): T {
  return arg;
}

// Usage
identity<string>("hello"); // Explicit type argument
identity(42);              // Inferred as number

// Multiple type parameters
function pair<T, U>(first: T, second: U): [T, U] {
  return [first, second];
}

pair("hello", 42); // [string, number]
```

### Generic Constraints

```typescript
// Constraint: T must have a length property
interface Lengthwise {
  length: number;
}

function logLength<T extends Lengthwise>(arg: T): T {
  console.log(arg.length);
  return arg;
}

logLength("hello");     // OK, strings have length
logLength([1, 2, 3]);   // OK, arrays have length
// logLength(123);      // Error: number has no length

// keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const person = { name: "Alice", age: 30 };
getProperty(person, "name"); // "Alice"
// getProperty(person, "email"); // Error: "email" is not a key of person
```

### Generic Interfaces

```typescript
// Generic interface
interface Container<T> {
  value: T;
  getValue(): T;
}

// Generic callable interface
interface GenericFunc<T> {
  (arg: T): T;
}

// Usage
const stringContainer: Container<string> = {
  value: "hello",
  getValue() {
    return this.value;
  }
};
```

### Generic Classes

```typescript
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }
}

const numberStack = new Stack<number>();
numberStack.push(1);
numberStack.push(2);
numberStack.pop(); // 2
```

### Default Type Parameters

```typescript
// Default type argument
interface ApiResponse<T = any> {
  data: T;
  status: number;
  message: string;
}

// Using the default
const response1: ApiResponse = { data: "anything", status: 200, message: "OK" };

// Specifying a type
const response2: ApiResponse<User[]> = {
  data: [{ id: 1, name: "Alice" }],
  status: 200,
  message: "OK"
};
```

---

## 7. Advanced Types

### Union Types

```typescript
// Basic union type
type ID = string | number;

function printId(id: ID): void {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id.toFixed(2));
  }
}

// Literal union types
type Status = "pending" | "success" | "error";
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
```

### Intersection Types

```typescript
interface Name {
  firstName: string;
  lastName: string;
}

interface Contact {
  email: string;
  phone: string;
}

// Intersection type: combines multiple types
type Person = Name & Contact;

const person: Person = {
  firstName: "John",
  lastName: "Doe",
  email: "john@example.com",
  phone: "123-456-7890"
};
```

### Type Guards

```typescript
// typeof type guard
function padLeft(value: string, padding: string | number): string {
  if (typeof padding === "number") {
    return " ".repeat(padding) + value;
  }
  return padding + value;
}

// instanceof type guard
class Cat {
  meow() { console.log("Meow!"); }
}

class Dog {
  bark() { console.log("Woof!"); }
}

function makeSound(animal: Cat | Dog): void {
  if (animal instanceof Cat) {
    animal.meow();
  } else {
    animal.bark();
  }
}

// in type guard
interface Fish {
  swim(): void;
}

interface Bird {
  fly(): void;
}

function move(animal: Fish | Bird): void {
  if ("swim" in animal) {
    animal.swim();
  } else {
    animal.fly();
  }
}

// Custom type guard (type predicate)
function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}

function doSomething(pet: Fish | Bird): void {
  if (isFish(pet)) {
    pet.swim(); // TypeScript knows this is Fish
  } else {
    pet.fly();  // TypeScript knows this is Bird
  }
}
```

### Discriminated Unions

This is one of the most practical patterns in TypeScript:

```typescript
// Define discriminated union
interface Circle {
  kind: "circle";  // Discriminant property
  radius: number;
}

interface Rectangle {
  kind: "rectangle";
  width: number;
  height: number;
}

interface Triangle {
  kind: "triangle";
  base: number;
  height: number;
}

type Shape = Circle | Rectangle | Triangle;

// TypeScript narrows the type based on the kind property
function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      // Exhaustiveness check
      const _exhaustiveCheck: never = shape;
      return _exhaustiveCheck;
  }
}
```

### keyof and typeof

```typescript
// keyof: gets all keys of a type
interface Person {
  name: string;
  age: number;
  email: string;
}

type PersonKeys = keyof Person; // "name" | "age" | "email"

// typeof: gets the type of a value
const config = {
  host: "localhost",
  port: 3000,
  debug: true
};

type Config = typeof config;
// { host: string; port: number; debug: boolean }

// Combining both
type ConfigKeys = keyof typeof config; // "host" | "port" | "debug"
```

### Indexed Access Types

```typescript
interface Person {
  name: string;
  age: number;
  address: {
    city: string;
    country: string;
  };
}

// Access property types
type NameType = Person["name"];      // string
type AgeType = Person["age"];        // number
type AddressType = Person["address"]; // { city: string; country: string }

// Access nested property types
type CityType = Person["address"]["city"]; // string

// Combined with keyof
type PersonValues = Person[keyof Person];
// string | number | { city: string; country: string }
```

---

## 8. Conditional Types

Conditional types are among the most powerful features of TypeScript's type system.

### Basic Conditional Types

```typescript
// Syntax: T extends U ? X : Y
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false

// Practical example
type TypeName<T> =
  T extends string ? "string" :
  T extends number ? "number" :
  T extends boolean ? "boolean" :
  T extends undefined ? "undefined" :
  T extends Function ? "function" :
  "object";

type T1 = TypeName<string>;     // "string"
type T2 = TypeName<() => void>; // "function"
```

### The infer Keyword

`infer` lets you extract types within conditional type expressions:

```typescript
// Extract function return type
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type Func = () => string;
type R1 = MyReturnType<Func>; // string

// Extract function parameter types
type MyParameters<T> = T extends (...args: infer P) => any ? P : never;

type Func2 = (a: string, b: number) => void;
type P1 = MyParameters<Func2>; // [string, number]

// Extract array element type
type ElementType<T> = T extends (infer E)[] ? E : never;

type E1 = ElementType<string[]>;  // string
type E2 = ElementType<number[]>;  // number

// Unwrap Promise
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type P2 = UnwrapPromise<Promise<string>>; // string
type P3 = UnwrapPromise<number>;          // number
```

### Distributive Conditional Types

When a conditional type acts on a union type, it distributes automatically:

```typescript
type ToArray<T> = T extends any ? T[] : never;

type StrArr = ToArray<string>;               // string[]
type NumOrStrArr = ToArray<string | number>; // string[] | number[]

// To prevent distribution, wrap T in a tuple
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;

type Result = ToArrayNonDist<string | number>; // (string | number)[]
```

---

## 9. Mapped Types

Mapped types let you create new types by transforming the properties of existing ones.

### Basic Mapped Types

```typescript
// Make all properties optional
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};

// Make all properties readonly
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K];
};

// Make all properties required
type MyRequired<T> = {
  [K in keyof T]-?: T[K];
};

// Remove readonly
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};
```

### Key Remapping with as

TypeScript 4.1+ supports remapping keys with the `as` clause:

```typescript
// Convert all keys to getters
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface Person {
  name: string;
  age: number;
}

type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }

// Filter out specific keys
type RemoveKind<T> = {
  [K in keyof T as K extends "kind" ? never : K]: T[K];
};

interface Shape {
  kind: string;
  radius: number;
}

type ShapeWithoutKind = RemoveKind<Shape>;
// { radius: number }
```

---

## 10. Built-in Utility Types

TypeScript ships with many utility types that you should know well.

### Property Modifier Types

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
}

// Partial<T>: all properties become optional
type PartialUser = Partial<User>;
// { id?: number; name?: string; email?: string; age?: number }

// Required<T>: all properties become required
type RequiredUser = Required<User>;
// { id: number; name: string; email: string; age: number }

// Readonly<T>: all properties become readonly
type ReadonlyUser = Readonly<User>;
// { readonly id: number; readonly name: string; ... }
```

### Property Selection Types

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

// Pick<T, K>: select specific properties
type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string }

// Omit<T, K>: exclude specific properties
type PublicUser = Omit<User, "password">;
// { id: number; name: string; email: string }
```

### Union Type Operations

```typescript
type Status = "pending" | "active" | "inactive" | "deleted";

// Exclude<T, U>: remove types from T that are assignable to U
type ActiveStatus = Exclude<Status, "deleted">;
// "pending" | "active" | "inactive"

// Extract<T, U>: keep only types from T that are assignable to U
type LifeStatus = Extract<Status, "active" | "inactive">;
// "active" | "inactive"

// NonNullable<T>: remove null and undefined
type MaybeString = string | null | undefined;
type DefiniteString = NonNullable<MaybeString>;
// string
```

### Function-Related Types

```typescript
function createUser(name: string, age: number): User {
  return { id: 1, name, age, email: "" };
}

// ReturnType<T>: extract function return type
type CreateUserReturn = ReturnType<typeof createUser>;
// User

// Parameters<T>: extract function parameter types as a tuple
type CreateUserParams = Parameters<typeof createUser>;
// [string, number]

// ConstructorParameters<T>: extract constructor parameter types
class MyClass {
  constructor(public name: string, public age: number) {}
}
type MyClassParams = ConstructorParameters<typeof MyClass>;
// [string, number]

// InstanceType<T>: extract the instance type of a constructor
type MyClassInstance = InstanceType<typeof MyClass>;
// MyClass
```

### String Manipulation Types

```typescript
// Uppercase<S>
type Upper = Uppercase<"hello">; // "HELLO"

// Lowercase<S>
type Lower = Lowercase<"HELLO">; // "hello"

// Capitalize<S>
type Cap = Capitalize<"hello">; // "Hello"

// Uncapitalize<S>
type Uncap = Uncapitalize<"Hello">; // "hello"
```

### The Record Type

```typescript
// Record<K, V>: create an object type with keys K and values V
type PageInfo = {
  title: string;
  url: string;
};

type Pages = Record<"home" | "about" | "contact", PageInfo>;
// {
//   home: PageInfo;
//   about: PageInfo;
//   contact: PageInfo;
// }

// Commonly used for dictionary types
type StringMap = Record<string, string>;
type NumberMap = Record<string, number>;
```

---

## 11. Template Literal Types

### Basic Usage

```typescript
// Basic template literal
type Greeting = `Hello, ${string}`;

const g1: Greeting = "Hello, World"; // OK
// const g2: Greeting = "Hi, World"; // Error

// Combining union types
type Vertical = "top" | "bottom";
type Horizontal = "left" | "right";

type Position = `${Vertical}-${Horizontal}`;
// "top-left" | "top-right" | "bottom-left" | "bottom-right"
```

### Practical Applications

```typescript
// Event handler types
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

// CSS values
type CSSUnit = "px" | "em" | "rem" | "%";
type CSSValue = `${number}${CSSUnit}`;

const width: CSSValue = "100px"; // OK
const height: CSSValue = "50%";  // OK
// const bad: CSSValue = "100"; // Error

// API paths
type ApiVersion = "v1" | "v2";
type Resource = "users" | "posts" | "comments";
type ApiPath = `/api/${ApiVersion}/${Resource}`;
// "/api/v1/users" | "/api/v1/posts" | ...
```

### Type Inference with Template Literals

```typescript
// Extract types from template literal patterns
type ExtractRouteParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractRouteParams<Rest>]: string }
    : T extends `${infer _Start}:${infer Param}`
    ? { [K in Param]: string }
    : {};

type Params = ExtractRouteParams<"/users/:userId/posts/:postId">;
// { userId: string; postId: string }
```

---

## 12. Type Gymnastics in Practice

Type gymnastics refers to performing complex type-level computations with TypeScript's type system. Here are some common challenges.

### DeepReadonly

```typescript
// Recursively make all properties readonly
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

interface User {
  name: string;
  address: {
    city: string;
    country: string;
  };
}

type ReadonlyUser = DeepReadonly<User>;
// {
//   readonly name: string;
//   readonly address: {
//     readonly city: string;
//     readonly country: string;
//   };
// }
```

### DeepPartial

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;
```

### Flatten

```typescript
// Flatten nested array types
type Flatten<T extends any[]> = T extends [infer First, ...infer Rest]
  ? First extends any[]
    ? [...Flatten<First>, ...Flatten<Rest>]
    : [First, ...Flatten<Rest>]
  : T;

type Nested = [1, [2, [3, 4]], 5];
type Flat = Flatten<Nested>; // [1, 2, 3, 4, 5]
```

### TupleToUnion

```typescript
type TupleToUnion<T extends any[]> = T[number];

type Tuple = ["a", "b", "c"];
type Union = TupleToUnion<Tuple>; // "a" | "b" | "c"
```

### UnionToIntersection

```typescript
type UnionToIntersection<U> =
  (U extends any ? (k: U) => void : never) extends
  (k: infer I) => void ? I : never;

type Union = { a: string } | { b: number };
type Intersection = UnionToIntersection<Union>;
// { a: string } & { b: number }
```

### PickByType

```typescript
// Select properties by value type
type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

interface Model {
  name: string;
  count: number;
  isReady: boolean;
  run: () => void;
}

type StringProps = PickByType<Model, string>;
// { name: string }

type FunctionProps = PickByType<Model, Function>;
// { run: () => void }
```

---

## 13. Declaration Files

### Declaration File Basics

Declaration files (`.d.ts`) provide type definitions for JavaScript libraries.

```typescript
// types/lodash.d.ts
declare module "lodash" {
  export function chunk<T>(array: T[], size?: number): T[][];
  export function compact<T>(array: T[]): T[];
  export function uniq<T>(array: T[]): T[];
}
```

### Global Declarations

```typescript
// global.d.ts
declare global {
  interface Window {
    myGlobalVar: string;
    myGlobalFunc: (arg: string) => void;
  }

  // Global variable
  var DEBUG: boolean;

  // Global function
  function myGlobalFunction(): void;
}

export {}; // Ensure this is treated as a module
```

### Module Declarations

```typescript
// Add types for .css files
declare module "*.css" {
  const content: { [className: string]: string };
  export default content;
}

// Add types for .png files
declare module "*.png" {
  const value: string;
  export default value;
}

// Add types for .json files
declare module "*.json" {
  const value: any;
  export default value;
}
```

### Using @types Packages

```bash
# Install type declaration packages
npm install --save-dev @types/node
npm install --save-dev @types/react
npm install --save-dev @types/lodash
```

---

## 14. Module System

### ES Modules

```typescript
// math.ts - Exports
export const PI = 3.14159;

export function add(a: number, b: number): number {
  return a + b;
}

export default class Calculator {
  // ...
}

// main.ts - Imports
import Calculator, { PI, add } from "./math";
import * as math from "./math";
```

### Type-Only Imports and Exports

```typescript
// types.ts
export interface User {
  id: number;
  name: string;
}

export type ID = string | number;

// main.ts - Type-only import (recommended)
import type { User, ID } from "./types";

// Mixed import
import { type User, someFunction } from "./module";
```

### Namespaces

```typescript
// Namespaces (not recommended for new projects)
namespace Validation {
  export interface StringValidator {
    isValid(s: string): boolean;
  }

  export class EmailValidator implements StringValidator {
    isValid(s: string): boolean {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
    }
  }
}

// Usage
const validator = new Validation.EmailValidator();
```

---

## 15. Best Practices

### Leverage Type Inference

```typescript
// Let TypeScript infer types when it can
const name = "Alice";        // Inferred as string
const numbers = [1, 2, 3];   // Inferred as number[]
const user = { name: "Bob" }; // Inferred as { name: string }

// Use as const for more precise types
const status = "active" as const;     // Inferred as "active"
const tuple = [1, "hello"] as const;  // Inferred as readonly [1, "hello"]

const config = {
  host: "localhost",
  port: 3000
} as const;
// Inferred as { readonly host: "localhost"; readonly port: 3000 }
```

### Type Assertions

```typescript
// Basic assertion
const input = document.getElementById("input") as HTMLInputElement;

// Non-null assertion
function getValue(map: Map<string, string>, key: string): string {
  return map.get(key)!; // Tell TypeScript this value definitely exists
}

// Double assertion (use sparingly)
const value = (expr as unknown) as SomeType;
```

### Type Narrowing

```typescript
function process(value: string | number | null): string {
  // Use type guards to narrow the type
  if (value === null) {
    return "null";
  }

  if (typeof value === "string") {
    return value.toUpperCase();
  }

  // TypeScript now knows value is number
  return value.toFixed(2);
}
```

### Avoiding any

```typescript
// Bad
function parse(json: string): any {
  return JSON.parse(json);
}

// Better - use generics
function parse<T>(json: string): T {
  return JSON.parse(json);
}

// Best - add runtime validation
function parseUser(json: string): User {
  const data = JSON.parse(json);
  if (!isUser(data)) {
    throw new Error("Invalid user data");
  }
  return data;
}

function isUser(data: unknown): data is User {
  return (
    typeof data === "object" &&
    data !== null &&
    "name" in data &&
    "age" in data
  );
}
```

### Always Enable Strict Mode

Always enable strict mode in your `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

This is equivalent to enabling all of:
- `strictNullChecks`
- `strictFunctionTypes`
- `strictBindCallApply`
- `strictPropertyInitialization`
- `noImplicitAny`
- `noImplicitThis`
- `alwaysStrict`

---

## 16. Common Interview Questions

### What is the difference between type and interface?

- `interface` supports declaration merging; `type` does not
- `type` can define unions, tuples, and primitive aliases
- `interface` can only define object types
- They extend differently: `interface` uses `extends`, `type` uses `&`

### What is the difference between any and unknown?

- `any` bypasses type checking entirely and lets you call any method
- `unknown` requires a type check before you can use the value
- `unknown` is the type-safe counterpart of `any`

### What is the difference between never and void?

- `void` means a function returns nothing (completes normally)
- `never` means a function never returns (throws or loops forever)
- `void` can be assigned `undefined`; `never` cannot be assigned any value

### What are type guards?

Type guards are runtime checks that narrow a type within a conditional branch:
- `typeof`: checks primitive types
- `instanceof`: checks class instances
- `in`: checks for object properties
- Custom type predicates: `function isFish(pet): pet is Fish`

### What are conditional types?

Conditional types choose a type based on a condition: `T extends U ? X : Y`

Common uses:
- Extracting types with `infer`
- Filtering types
- Building utility types

### What are mapped types?

Mapped types iterate over the properties of an existing type to produce a new one:

```typescript
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};
```

### How do you implement DeepReadonly?

```typescript
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;
```

### What does the infer keyword do?

`infer` declares a type variable to be inferred within a conditional type, letting you extract part of a complex type:

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

---

## 17. TypeScript 5.x Features

### Decorators

TypeScript 5.0 ships with native ECMAScript decorator support:

```typescript
function logged(value: any, context: ClassMethodDecoratorContext) {
  const methodName = String(context.name);

  function replacementMethod(this: any, ...args: any[]) {
    console.log(`Calling ${methodName} with args:`, args);
    const result = value.call(this, ...args);
    console.log(`${methodName} returned:`, result);
    return result;
  }

  return replacementMethod;
}

class Calculator {
  @logged
  add(a: number, b: number) {
    return a + b;
  }
}
```

### const Type Parameters

```typescript
function createTuple<const T extends readonly unknown[]>(...args: T): T {
  return args;
}

const tuple = createTuple(1, 2, 3);
// Type is readonly [1, 2, 3], not number[]
```

### The satisfies Operator

```typescript
type Colors = "red" | "green" | "blue";
type RGB = [red: number, green: number, blue: number];

const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255]
} satisfies Record<Colors, string | RGB>;

// palette.red is typed as [number, number, number], not string | RGB
const redChannel = palette.red[0]; // OK
```

---

## Wrapping Up

This guide covered the core topics in TypeScript:

1. **Primitive types** -- string, number, boolean, arrays, tuples, enums, any/unknown/never/void
2. **Functions** -- declarations, optional/default/rest parameters, overloads
3. **Interfaces and type aliases** -- definitions, inheritance, and when to use each
4. **Classes** -- access modifiers, abstract classes, interface implementation
5. **Generics** -- functions, interfaces, classes, constraints, defaults
6. **Advanced types** -- unions, intersections, type guards, discriminated unions
7. **Conditional types** -- syntax, infer, distributive behavior
8. **Mapped types** -- property mapping, key remapping
9. **Utility types** -- Partial, Required, Pick, Omit, Record, and more
10. **Template literal types** -- string-level type manipulation
11. **Type gymnastics** -- real-world type-level challenges
12. **Declaration files** -- typing JavaScript libraries, global and module declarations
13. **Best practices** -- inference, assertions, narrowing, strict mode

With these concepts under your belt, you will be well equipped for both day-to-day TypeScript development and technical interviews.

**References:**

- [TypeScript Official Documentation](https://www.typescriptlang.org/docs/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript GitHub](https://github.com/microsoft/TypeScript)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)
