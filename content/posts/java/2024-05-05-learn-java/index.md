---
title:      "Java学习笔记"
date:       2024-05-04 21:00:00
author:     "bruce"
toc: true
tags:
    - java
---

![image](java-logo.jpg)

## 一、背景

1995年SUN 公司推出，最早叫 Oak(橡树)，后改名叫 Java，Java之父詹姆斯（James），SUN 在2009年被 ORACLE收购。

## 二、整体学习路线

![](Pasted-image-20240504163728.png)/
![](Pasted%20image%2020240504163749.png)

Java 技术体系（JAVA SE、JAVA EE、JAVA ME）。
Java基本啥都能干，但主要做互联网系统的开发.

## 三、JDK 

![](Pasted%20image%2020240504194249.png)
![](Pasted%20image%2020240504200330.png)

javac：编译工具

java ：执行工具

JVM(Java Virtual Machine)：Java 虚拟机，真正运行 Java程序的地方
核心类库：Java 自己写好的程序

JRE（Java Runtime Environment）:Java的运行环境

JDK(Java Development Kit): Java开发工具包(包含上面所有)

## 四、IDE IDEA

![](Pasted%20image%2020240504200858.png)

IDEA几种常见的快捷键，以及他们的作用

| **快捷键**                        | **功能效果**                     |
| --------------------------------- | -------------------------------- |
| main/psvm、sout、…                | 快速键入相关代码                 |
| Ctrl + D                          | 复制当前行数据到下一行           |
| Ctrl + Y                          | 删除所在行，建议用Ctrl + X       |
| Ctrl + ALT + L                    | 格式化代码                       |
| ALT + SHIFT + ↑ , ALT + SHIFT + ↓ | 上下移动当前代码                 |
| Ctrl + / , Ctrl + Shift + /       | 对代码进行注释(讲注释的时候再说) |

## 五、JAVA SE基础

### 1. 基础语法

#### 1.1 字面量

字面量其实就是告诉程序员数据在程序中的书写格式

![](1660150925625.png)

#### 1.2 变量

**定义：** 变量是用来记录程序中的数据的。其本质上是内存中的一块区域，你可以把这块区域理解成一个小盒子，盒子里放的东西就是变量记录的数据。

**格式：** `数据类型 变量名 = 初始值;`

**作用：** 使用变量来记录数据，对于数据的管理更为灵活。

#### 1.3 关键字

关键字是java语言中有特殊含义的单词

| **abstract**   | **assert**       | **boolean**   | **break**      | **byte**   |
| -------------- | ---------------- | ------------- | -------------- | ---------- |
| **case**       | **catch**        | **char**      | **class**      | **const**  |
| **continue**   | **default**      | **do**        | **double**     | **else**   |
| **enum**       | **extends**      | **final**     | **finally**    | **float**  |
| **for**        | **goto**         | **if**        | **implements** | **import** |
| **instanceof** | **int**          | **interface** | **long**       | **native** |
| **new**        | **package**      | **private**   | **protected**  | **public** |
| **return**     | **strictfp**     | **short**     | **static**     | **super**  |
| **switch**     | **synchronized** | **this**      | **throw**      | **throws** |
| **transient**  | **try**          | **void**      | **volatile**   | **while**  |

#### 1.4 标识符

标志符其实就是我们自己取的名字。像前面我们取的类名，变量名其实都是标志符。

#### 1.5 二进制

**变量里的数据在计算机中的存储原理**：任何数据在计算机中都是以**二进制**表示。整数先转成二进制再存储

字符怎么存储的呢？只需要将字符映射到整数，就可以用二进制表示了，所以需要一个字符数字映射表（字符<----->数字），就是大家经常听到的美国ASCII编码，中文GBK编码等

图片怎么存储呢？图片无限放大后可以看到像素点，每一个像素点就是一种颜色，任何一种颜色用三原色RGB表示(R红色，G绿色，B蓝色)，R、G、B种每一种颜色用一个字节的整数表示，取值范围[0,255]，转成整数后再转成二进制存储。、

声音怎么存储呢？声音以波的形式传播，把声波在表示在一个坐标系上，然后在坐标系上取一些点，把这些点的坐标值以二进制的形式存储到计算机中，这就是声音的存储原理

![image-20240505163630547](image-20240505163630547.png)

视频怎么存储呢？视频是图片和声音组成，按上面讲的图片和声音存储原理理解。

**十进制转二进制 、二进制转十进制**，有一种计算方式8421码，请注意。

![image-20240505164329830](image-20240505164329830.png)

**八进制、十六进制**

![image-20240505165805742](image-20240505165805742.png)

计算机的数据单位最小组成单元：字节，1B = 8b，1个字节等于8位

在B基础上发展出来KB、MB、GB、TB单位

![image-20240505170246173](image-20240505170246173.png)

#### 1.6 数据类型

Java的数据类型整体上来说分为两大类： **基本数据类型**、**引用数据类型**

![image-20240505170506109](image-20240505170506109.png)

自动类型转换指的是，数据范围小的变量可以直接赋值给数据范围大的变量

![image-20240505171902906](image-20240505171902906.png)

#### 1.7 运算符

Java提供的运算符有很多种，主要有下面几种：

- 基本算术运算符

  ![image-20240505172859556](image-20240505172859556.png)

  `+`符号除了用于加法运算，还可以作为连接符

- 自增自减运算符

  `++`读作自增，`--`读作自减； 运算规则如下

  ![image-20240505172940033](image-20240505172940033.png)

```
1.单独使用：++或者--放在变量前面没有区别
	   int a =10; 
	    a++;  //11
		--a;  //10
		System.out.println(a); //10

2.混合使用：++或者--放在变量或者前面运算规则稍有不通过
	//++在后：先做其他事情，再做自增和自减
	int a = 10;
	int b = a++; //等价于 int b = a; a++; 

	//++在前：先自增或者自减，再做其他运输
	int x = 10;
	int y = --x; //等价于x--; int y = x;  
```

- 赋值运算符

![image-20240505173409193](image-20240505173409193.png)

- 关系运算符

![image-20240505173436225](image-20240505173436225.png)

- 逻辑运算符

![image-20240505173508752](image-20240505173508752.png)

- 三元运算符

三元运算符的格式：`关系表达式? 值1 : 值2;`

#### 1.8 程序流程控制

程序的流程控制一般分为3种：**顺序结构、分支结构、循环结构**

- 顺序结构：就是不加任何控制，代码从main方法开始自上而下执行
- 分支结构：就是根据条件判断是true还是false，有选择性的执行哪些代码。在Java语言中提供了两个格式if 、 switch

如果单从功能上来讲，if 分支 的功能是更加强大的，switch分支能做的事情if 分支都能做。但是具体用哪一种分支形式，也是有一些使用原则的.

```
- 如果是对一个范围进行判断，建议使用if分支结构
- 如果是与一个一个的值比较的时候，建议使用switch分支结构
```

- 循环结构：就是控制某一段代码重复执行。在Java语言中提供了三种格式，for、while、do-while

#### 1.9 数组

数组就是一个容器，用来存一批同种类型的数据的。数组有两种初始化的方式，一种是静态初始化、一种是动态初始化

**静态初始化**标准格式： `数据类型[] 变量名 = new 数据类型[]{元素1,元素2,元素3};`

```
//定义数组，用来存储多个年龄
int[] ages = new int[]{12, 24, 36}
//定义数组，用来存储多个成绩
double[] scores = new double[]{89.9, 99.5, 59.5, 88.0};
```

静态初始化简化格式: `数据类型[] 变量名 = {元素1,元素2,元素3};`

```
//定义数组，用来存储多个年龄
int[] ages = {12, 24, 36}
//定义数组，用来存储多个成绩
double[] scores = {89.9, 99.5, 59.5, 88.0};
```

**注意**定义数组时， `数据类型[] 数组名` 也可写成 `数据类型 数组名[]` 

```
//以下两种写法是等价的。但是建议大家用第一种，因为这种写法更加普遍
int[] ages = {12, 24, 36};
int ages[] = {12, 24, 36}
```

**动态初始化**格式:`//数据类型[]  数组名 = new 数据类型[长度];`,例如`int[] arr = new int[3];`

使用动态初始化定义数组时，根据元素类型不同，默认值也有所不同。

![image-20240505180102841](image-20240505180102841.png)

**数组在计算机中的执行原理**

程序在内存中执行,Java程序是把编译后的字节码加载到Java虚拟机中执行.

![image-20240505180222119](image-20240505180222119.png)

```
public class ArrayDemo1 {
    public static void main(String[] args) {
        int a = 10;
        System.out.println(a);

        int[] arr = new int[]{11, 22, 33};
        System.out.println(arr);

        System.out.println(arr[1]);

        arr[0] = 44;
        arr[1] = 55;
        arr[2] = 66;

        System.out.println(arr[0]);
        System.out.println(arr[1]);
        System.out.println(arr[2]);
    }
}
```

Java为了便于虚拟机执行Java程序，将虚拟机的内存划分为 **方法区、栈、堆**、本地方法栈、寄存器 这5块区域,每部分存储内容如下：

- **方法区**：字节码文件先加载到这里
- **栈**：方法运行时所进入的内存区域，由于变量在方法中，所以变量也在这一块区域中
- **堆**：存储new出来的东西，并分配地址。由于数组是new 出来的，所以数组也在这块区域。

上面案例执行的内存原理如下图所示，按照① ② ③ ④ ⑤ ⑥ 的标记的顺序来看

![image-20240505180635088](image-20240505180635088.png)

**总结一下`int a = 10`与 `int[] arr = new int[]{11,22,33}的区别`**

- **a**是一个变量，在栈内存中，**a**变量中存储的数据就是**10**这个值。
- **arr**也是一个变量，在栈中，存储的是数组对象在堆内存中的地址值

```
// 这里的int a是一个基本类型变量，存储的是一个数值
int a = 10 ; 
//这里的int[] arr是一个引用类型的变量，存储的是一个地址值
int[] arr = new int[]{44,55,66};
```

#### 1.10 方法

方法是一种语法结构，它可以把一段代码封装成一个功能，以便重复调用。格式:

![image-20240505182105273](image-20240505182105273.png)

例如:

```
//目标：掌握定义方法的完整格式，搞清楚使用方法的好处。
public class MethodDemo1 {
    public static void main(String[] args) {
        // 需求：假如现在很多程序员都要进行2个整数求和的操作。
        // 1、李工。
        int rs = sum(10, 20);
        System.out.println("和是：" + rs);

        // 2、张工。
        int rs2 = sum(30, 20);
        System.out.println("和是：" + rs2);
    }

    public static int sum(int a,int b) {
        int c = a + b;
        return c;
    }
}
```

方法的好处，可以归纳为2点：

- 提高了代码的复用性，提高了开发效率。
- 让程序的逻辑更清晰。

**方法在计算机中的执行原理**

Java的方法是在栈内存区域中执行，**每次调用方法，方法都会进栈执行；执行完后，又会弹栈出去。**先进后出

假设在main方法中依次调用A方法、B方法、C方法，在内存中的执行流程如下：

![image-20240505200300178](image-20240505200300178.png)

**Java的参数传递机制都是：值传递，传递的是实参存储的值的副本。**

基本类型和引用类型的参数在传递的时候有什么不同？

- 都是值传递
- 基本类型的参数传递存储的数据值。
- 引用类型的参数传递存储的地址值。（String,Array都是引用类型）

**方法重载**

定义：一个类中，多个方法的名称相同，但它们形参列表不同。

```
public class MethodOverLoadDemo1 {
    public static void main(String[] args) {
        // 目标：认识方法重载，并掌握其应用场景。
        test();
        test(100);
    }

    public static void test(){
        System.out.println("===test1===");
    }

    public static void test(int a){
        System.out.println("===test2===" + a);
    }

    void test(double a){

    }

    void test(double a, int b){
    }

    void test(int b, double a){
    }

    int test(int a, int b){
        return a + b;
    }
}
```

**方法重载需要注意什么？**

- 一个类中，只要一些方法的名称相同、形参列表不同，那么它们就是方法重载了，
  	  其它的都不管（如：修饰符，返回值类型是否一样都无所谓）。

- 形参列表不同指的是：形参的个数、类型、顺序不同，不关心形参的名称。

### 2. 面向对象

所谓编写对象编程，就是把要处理的数据交给对象，让对象来处理。

Java之父詹姆斯高斯林认为**万物皆对象！**任何一个对象都可以包含一些数据，数据属于哪个对象，就由哪个对象来处理。对象可以理解成一张数据表，而数据表中可以有哪些数据，是有类来设计的。

面向对象编程优点：面向对象的开发更符合人类的思维习惯，让编程变得更加简单、更加直观。

#### 2.1 对象在计算机中的执行原理

![image-20240506104721819](image-20240506104721819.png)

与前面学习的数组变量记录的其实数数组在堆内存中的地址类似，对象可以按统一思路理解：

- `Student s1`表示的是在栈内存中，创建了一个Student类型的变量，变量名为s1

- 而`new Student()`会在堆内存中创建一个对象，而对象中包含学生的属性名和属性值

  同时系统会为这个Student对象分配一个地址值0x4f3f5b24

- 接着把对象的地址赋值给栈内存中的变量s1，通过s1记录的地址就可以找到这个对象

- 当执行`s1.name=“播妞”`时，其实就是通过s1找到对象的地址，再通过对象找到对象的name属性，再给对象的name属性赋值为`播妞`;  

#### 2.2 类和对象注意点

![image-20240506105055502](image-20240506105055502.png)

关于一个代码文件中可以有多个类这一条，举例：

```
//public修饰的类Demo1，和文件名Demo1相同
public class Demo1{
    
}

class Student{
    
}
```

#### 2.3 this关键字

**this是什么？** this就是一个变量，用在方法中，可以拿到当前类的对象。

![image-20240506105552235](image-20240506105552235.png)

**this有什么用？** 通过this在方法中可以访问本类对象的成员变量，哪一个对象调用方法方法中的this就是哪一个对象

#### 2.4 构造器

**什么是构造器？**

构造器其实是一种特殊的方法，但是这个方法没有返回值类型，方法名必须和类名相同

![image-20240506105926248](image-20240506105926248.png)

**构造器特点？**

在创建对象时，会调用构造器。**new 对象就是在执行构造方法**

![image-20240506110057497](image-20240506110057497.png)

![image-20240506110105660](image-20240506110105660.png)



构造器就是用来创建对象的。可以在创建对象时给对象的属性做一些初始化操作.

构造器注意事项:

```
1.在设计一个类时，如果不写构造器，Java会自动生成一个无参数构造器。
2.一定定义了有参数构造器，Java就不再提供空参数构造器，此时建议自己加一个无参数构造器。
```

#### 2.5 封装性

**什么是封装？** 

封装就是用类设计对象处理某一个事物的数据时，应该把要处理的数据，以及处理数据的方法，都设计到一个对象中去。

比如：在设计学生类时，把学生对象的姓名、语文成绩、数学成绩三个属性，以及求学生总分、平均分的方法，都封装到学生对象中来。

封装的设计规范用8个字总结：**合理隐藏、合理暴露** 。举例设计一辆汽车时发动机、变松箱需要隐藏，启动按钮、刹车需要暴露出来

**封装在代码中如何体现？**

一般在设计一个类时，会将成员变量隐藏，然后把操作成员变量的方法对外暴露。需要用到**修饰符** 。前面看到的`public`就是修饰符，与之对应的有一个`private` 修饰符，被private修饰后，只能在本类中访问。如果要对外访问可以加个对外报暴漏的方法，在方法里返回变量。

![image-20240506113425295](image-20240506113425295.png)

#### 2.6 实体JavaBean

面向对象编程中，经常写的一种类——叫实体JavaBean类，那什么是实体类？

实体类就是一种特殊的类，它需要满足下面的要求：

- 类中的成员变量都要私有，并且要对外提供相应的`getXxx`,`setXxx`方法

- 类中必须要有一个公共的无参构造器

例如写一个Student类

![image-20240506113753917](image-20240506113753917.png)

实体类中除了有给对象存、取值的方法就没有提供其他方法，所以实体类仅仅只是用来封装数据用的。

实际开发中，实体类仅仅只用来封装数据，而对数据的处理交给其他类来完成，以实现数据和数据业务处理相分离。

#### 2.7 成员变量和局部变量

![image-20240506143612915](image-20240506143612915.png)

![image-20240506143658134](image-20240506143658134.png)



#### 2.8 常用Java Api

**包**

学习API类之前，要了解包，Java官方提供了很多类，为了对这些类进行分门别类的管理，将写好的类都是放在不同的包里。

包类似于文件夹，一个包能放多个类文件。

![image-20240506144925767](image-20240506144925767.png)

建包的语法格式：

```
//类文件的第一行定义包
package com.itheima.javabean;

public class 类名{
    
}
```

在自己的程序中调用其他包中的程序，注意：

- 如果当前程序中，要调用自己所在包下的其他程序，可以直接调用。（同一个包下的类，互相可以直接调用）

- 如果当前程序中，要调用其他包下的程序，则必须在当前程序中导包, 才可以访问！

  导包格式：` import 包名.类名`

- 如果当前程序中，要调用Java.lang包下的程序，不需要我们导包的，可以直接使用。

- 如果当前程序中，要调用多个不同包下的程序，而这些程序名正好一样，此时默认只能导入一个程序，另一个程序必须带包名访问。

 **String**

String代表字符串对象，可以用来封装字符串数据，并提供了很多操作字符串的方法。创建字符串的方式：

	方式一： 直接使用双引号“...” 。
	方式二：new String类，调用构造器初始化字符串对象。

![image-20240506145701393](image-20240506145701393.png)

```
// 1、直接双引号得到字符串对象，封装字符串数据
String name = "黑马666";
System.out.println(name);

// 2、new String创建字符串对象，并调用构造器初始化字符串
String rs1 = new String();
System.out.println(rs1); // ""

String rs2 = new String("itheima");
System.out.println(rs2);

char[] chars = {'a', '黑', '马'};
String rs3 = new String(chars);
System.out.println(rs3);

byte[] bytes = {97, 98, 99};
String rs4 = new String(bytes);
System.out.println(rs4);
```

String类常用方法

![image-20240506145806557](image-20240506145806557.png)

```java
public class StringDemo2 {
    public static void main(String[] args) {
        //目标：快速熟悉String提供的处理字符串的常用方法。
        String s = "黑马Java";
        // 1、获取字符串的长度
        System.out.println(s.length());

        // 2、提取字符串中某个索引位置处的字符
        char c = s.charAt(1);
        System.out.println(c);

        // 字符串的遍历
        for (int i = 0; i < s.length(); i++) {
            // i = 0 1 2 3 4 5
            char ch = s.charAt(i);
            System.out.println(ch);
        }

        System.out.println("-------------------");

        // 3、把字符串转换成字符数组，再进行遍历
        char[] chars = s.toCharArray();
        for (int i = 0; i < chars.length; i++) {
            System.out.println(chars[i]);
        }

        // 4、判断字符串内容，内容一样就返回true
        String s1 = new String("黑马");
        String s2 = new String("黑马");
        System.out.println(s1 == s2); // false
        System.out.println(s1.equals(s2)); // true

        // 5、忽略大小写比较字符串内容
        String c1 = "34AeFG";
        String c2 = "34aEfg";
        System.out.println(c1.equals(c2)); // false
        System.out.println(c1.equalsIgnoreCase(c2)); // true

        // 6、截取字符串内容 (包前不包后的)
        String s3 = "Java是最好的编程语言之一";
        String rs = s3.substring(0, 8);
        System.out.println(rs);

        // 7、从当前索引位置一直截取到字符串的末尾
        String rs2 = s3.substring(5);
        System.out.println(rs2);

        // 8、把字符串中的某个内容替换成新内容，并返回新的字符串对象给我们
        String info = "这个电影简直是个垃圾，垃圾电影！！";
        String rs3 = info.replace("垃圾", "**");
        System.out.println(rs3);

        // 9、判断字符串中是否包含某个关键字
        String info2 = "Java是最好的编程语言之一，我爱Java,Java不爱我！";
        System.out.println(info2.contains("Java"));
        System.out.println(info2.contains("java"));
        System.out.println(info2.contains("Java2"));

        // 10、判断字符串是否以某个字符串开头。
        String rs4 = "张三丰";
        System.out.println(rs4.startsWith("张"));
        System.out.println(rs4.startsWith("张三"));
        System.out.println(rs4.startsWith("张三2"));

        // 11、把字符串按照某个指定内容分割成多个字符串，放到一个字符串数组中返回给我们
        String rs5 = "张无忌,周芷若,殷素素,赵敏";
        String[] names = rs5.split(",");
        for (int i = 0; i < names.length; i++) {
            System.out.println(names[i]);
        }
    }
}
```

字符串原理理解注意下面两点：

- String是不可变字符串对象。

![image-20240506150738527](image-20240506150738527.png)

看起来例子里的name值变了呀，为什么说字符串不可变呢？

这需要从字符串在内存中存储原理来解释，以`”“`形式创建的字符串对象，会在堆内存中的 **字符串常量池** 中存储。

![image-20240506151040074](image-20240506151040074.png)





- 只要是以“...”方式写出的字符串对象，会存储到字符串常量池，且相同内容的字符串只存储一份；但通过new方式创建字符串对象，每new一次都会产生一个新的对象放在堆内存中。

![image-20240506151836976](image-20240506151836976.png)

 **ArrayList**

ArrayList是集合中最常用的一种，集合类似于数组，也是容器，用来装数据的，但集合的大小可变

有数组为什么还要有集合？因为在java中数组长度是固定的，一旦创建不可改变，集合则可以根据需要想存几个就存几个，长度可变。

创建ArrayList容器对象一般使用空参数构造方法：

![image-20240506161915929](image-20240506161915929.png)

调用ArrayList类的常用方法对容器中的数据进行操作

![image-20240506161933504](image-20240506161933504.png)

```java
public class ArrayListDemo1 {
    public static void main(String[] args) {
        // 1、创建一个ArrayList的集合对象
        // ArrayList<String> list = new ArrayList<String>();
        // 从jdk 1.7开始才支持的
        ArrayList<String> list = new ArrayList<>();

        list.add("黑马");
        list.add("黑马");
        list.add("Java");
        System.out.println(list);

        // 2、往集合中的某个索引位置处添加一个数据
        list.add(1, "MySQL");
        System.out.println(list);

        // 3、根据索引获取集合中某个索引位置处的值
        String rs = list.get(1);
        System.out.println(rs);

        // 4、获取集合的大小（返回集合中存储的元素个数）
        System.out.println(list.size());

        // 5、根据索引删除集合中的某个元素值，会返回被删除的元素值给我们
        System.out.println(list.remove(1));
        System.out.println(list);

        // 6、直接删除某个元素值，删除成功会返回true，反之
        System.out.println(list.remove("Java"));
        System.out.println(list);

        list.add(1, "html");
        System.out.println(list);

        // 默认删除的是第一次出现的这个黑马的数据的
        System.out.println(list.remove("黑马"));
        System.out.println(list);

        // 7、修改某个索引位置处的数据，修改后会返回原来的值给我们
        System.out.println(list.set(1, "黑马程序员"));
        System.out.println(list);
    }
}
```

#### 2.9 static修饰符

static读作静态，可以用来修饰成员变量，也能修饰成员方法。

**修饰成员变量**

Java中的成员变量按照有无static修饰分为两种：**类变量、实例变量**

![image-20240506162549143](image-20240506162549143.png)

静态变量是属于类的，只需要通过类名就可以调用：**`类名.静态变量`**

实例变量是属于对象的，需要通过对象才能调用：**`对象.实例变量`**

![image-20240506162800881](image-20240506162800881.png)



- 1.类变量：属于类，在内存中只有一份，用类名调用
- 2.实例变量：属于对象，每一个对象都有一份，用对象调用

**修饰成员方法**

成员方法根据有无static也分为两类：**类方法、实例方法**

![image-20240506163026791](image-20240506163026791.png)

> 有static修饰的方法，是属于类的，称为**类方法**；调用时直接用类名调用即可。

> 无static修饰的方法，是属于对象的，称为实例方法；调用时，需要使用对象调用。

- 类方法：static修饰的方法，可以被类名调用，是因为它是随着类的加载而加载的；所以类名直接就可以找到static修饰的方法
- 实例方法：非static修饰的方法，需要创建对象后才能调用，是因为实例方法中可能会访问实例变量，而实例变量需要创建对象后才存在。所以实例方法，必须创建对象后才能调用。

![image-20240506163328827](image-20240506163328827.png)

**工具类**
如果一个类中的方法全都是静态的，那么这个类中的方法就全都可以被类名直接调用，由于调用起来非常方便，就像一个工具一下，所以把这样的类就叫做工具类。

![image-20240506163454647](image-20240506163454647.png)

**static应用-代码块**

代码块根据有无static修饰分为两种：静态代码块、实例代码块。

**静态代码块，随着类的加载而执行，而且只执行一次。**

![image-20240506163728436](image-20240506163728436.png)

![image-20240506163800678](image-20240506163800678.png)

**实例代码块每次创建对象之前都会执行一次**

![image-20240506163848096](image-20240506163848096.png)

![image-20240506164050846](image-20240506164050846.png)

**static应用-单例设计模式**









### 3. 集合技术 & I/O 技术

### 4. 网络编程 & 多线程技术

### 5. JDK特性 & 基础加强

## 六、JAVA WEB

## 七、JAVA WEB进阶




---
## *参考*

[Java程序员学习路线图](https://yun.itheima.com/subject/javamap/index.html)

[Java入门基础视频教程(B站)](https://www.bilibili.com/video/BV1Cv411372m/?spm_id_from=333.999.0.0) 

[Java基础教程(YouTube)](https://www.youtube.com/watch?v=VqfGCmjQt10)

[JavaWeb开发教程(B站)](https://www.bilibili.com/video/BV1m84y1w7Tb/?vd_source=4d819443886ce5506c7c6b65b4a7ad93)