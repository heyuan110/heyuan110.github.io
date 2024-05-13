---
title:      "Java学习笔记（一）"
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

![](Pasted-image-20240504163728.png)
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


## 五、基础语法

### 1 字面量

字面量其实就是告诉程序员数据在程序中的书写格式

![](1660150925625.png)

### 2 变量

**定义：** 变量是用来记录程序中的数据的。其本质上是内存中的一块区域，你可以把这块区域理解成一个小盒子，盒子里放的东西就是变量记录的数据。

**格式：** `数据类型 变量名 = 初始值;`

**作用：** 使用变量来记录数据，对于数据的管理更为灵活。

### 3 关键字

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

### 4 标识符

标志符其实就是我们自己取的名字。像前面我们取的类名，变量名其实都是标志符。

### 5 二进制

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

### 6 数据类型

Java的数据类型整体上来说分为两大类： **基本数据类型**、**引用数据类型**

![image-20240505170506109](image-20240505170506109.png)

自动类型转换指的是，数据范围小的变量可以直接赋值给数据范围大的变量

![image-20240505171902906](image-20240505171902906.png)

### 7 运算符

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

### 8 程序流程控制

程序的流程控制一般分为3种：**顺序结构、分支结构、循环结构**

- 顺序结构：就是不加任何控制，代码从main方法开始自上而下执行
- 分支结构：就是根据条件判断是true还是false，有选择性的执行哪些代码。在Java语言中提供了两个格式if 、 switch

如果单从功能上来讲，if 分支 的功能是更加强大的，switch分支能做的事情if 分支都能做。但是具体用哪一种分支形式，也是有一些使用原则的.

```
- 如果是对一个范围进行判断，建议使用if分支结构
- 如果是与一个一个的值比较的时候，建议使用switch分支结构
```

- 循环结构：就是控制某一段代码重复执行。在Java语言中提供了三种格式，for、while、do-while

### 9 数组

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

### 10 方法

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

## 六、 面向对象

所谓编写对象编程，就是把要处理的数据交给对象，让对象来处理。

Java之父詹姆斯高斯林认为**万物皆对象！**任何一个对象都可以包含一些数据，数据属于哪个对象，就由哪个对象来处理。对象可以理解成一张数据表，而数据表中可以有哪些数据，是有类来设计的。

面向对象编程优点：面向对象的开发更符合人类的思维习惯，让编程变得更加简单、更加直观。

### 1 对象在计算机中的执行原理

![image-20240506104721819](image-20240506104721819.png)

与前面学习的数组变量记录的其实数数组在堆内存中的地址类似，对象可以按统一思路理解：

- `Student s1`表示的是在栈内存中，创建了一个Student类型的变量，变量名为s1

- 而`new Student()`会在堆内存中创建一个对象，而对象中包含学生的属性名和属性值

  同时系统会为这个Student对象分配一个地址值0x4f3f5b24

- 接着把对象的地址赋值给栈内存中的变量s1，通过s1记录的地址就可以找到这个对象

- 当执行`s1.name=“播妞”`时，其实就是通过s1找到对象的地址，再通过对象找到对象的name属性，再给对象的name属性赋值为`播妞`;  

### 2 类和对象注意点

![image-20240506105055502](image-20240506105055502.png)

关于一个代码文件中可以有多个类这一条，举例：

```
//public修饰的类Demo1，和文件名Demo1相同
public class Demo1{
    
}

class Student{
    
}
```

### 3 this关键字

**this是什么？** this就是一个变量，用在方法中，可以拿到当前类的对象。

![image-20240506105552235](image-20240506105552235.png)

**this有什么用？** 通过this在方法中可以访问本类对象的成员变量，哪一个对象调用方法方法中的this就是哪一个对象

### 4 构造器

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

### 5 封装性

**什么是封装？** 

封装就是用类设计对象处理某一个事物的数据时，应该把要处理的数据，以及处理数据的方法，都设计到一个对象中去。

比如：在设计学生类时，把学生对象的姓名、语文成绩、数学成绩三个属性，以及求学生总分、平均分的方法，都封装到学生对象中来。

封装的设计规范用8个字总结：**合理隐藏、合理暴露** 。举例设计一辆汽车时发动机、变松箱需要隐藏，启动按钮、刹车需要暴露出来

**封装在代码中如何体现？**

一般在设计一个类时，会将成员变量隐藏，然后把操作成员变量的方法对外暴露。需要用到**修饰符** 。前面看到的`public`就是修饰符，与之对应的有一个`private` 修饰符，被private修饰后，只能在本类中访问。如果要对外访问可以加个对外报暴漏的方法，在方法里返回变量。

![image-20240506113425295](image-20240506113425295.png)

### 6 实体JavaBean

面向对象编程中，经常写的一种类——叫实体JavaBean类，那什么是实体类？

实体类就是一种特殊的类，它需要满足下面的要求：

- 类中的成员变量都要私有，并且要对外提供相应的`getXxx`,`setXxx`方法

- 类中必须要有一个公共的无参构造器

例如写一个Student类

![image-20240506113753917](image-20240506113753917.png)

实体类中除了有给对象存、取值的方法就没有提供其他方法，所以实体类仅仅只是用来封装数据用的。

实际开发中，实体类仅仅只用来封装数据，而对数据的处理交给其他类来完成，以实现数据和数据业务处理相分离。

### 7 成员变量和局部变量

![image-20240506143612915](image-20240506143612915.png)

![image-20240506143658134](image-20240506143658134.png)



### 8 常用Java Api

#### **包**

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

 #### **String**

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

 #### **ArrayList**

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

### 9 static修饰符

static读作静态，可以用来修饰成员变量，也能修饰成员方法。

#### **修饰成员变量**

Java中的成员变量按照有无static修饰分为两种：**类变量、实例变量**

![image-20240506162549143](image-20240506162549143.png)

静态变量是属于类的，只需要通过类名就可以调用：**`类名.静态变量`**

实例变量是属于对象的，需要通过对象才能调用：**`对象.实例变量`**

![image-20240506162800881](image-20240506162800881.png)



- 1.类变量：属于类，在内存中只有一份，用类名调用
- 2.实例变量：属于对象，每一个对象都有一份，用对象调用

#### **修饰成员方法**

成员方法根据有无static也分为两类：**类方法、实例方法**

![image-20240506163026791](image-20240506163026791.png)

> 有static修饰的方法，是属于类的，称为**类方法**；调用时直接用类名调用即可。

> 无static修饰的方法，是属于对象的，称为实例方法；调用时，需要使用对象调用。

- 类方法：static修饰的方法，可以被类名调用，是因为它是随着类的加载而加载的；所以类名直接就可以找到static修饰的方法
- 实例方法：非static修饰的方法，需要创建对象后才能调用，是因为实例方法中可能会访问实例变量，而实例变量需要创建对象后才存在。所以实例方法，必须创建对象后才能调用。

![image-20240506163328827](image-20240506163328827.png)

#### **工具类**
如果一个类中的方法全都是静态的，那么这个类中的方法就全都可以被类名直接调用，由于调用起来非常方便，就像一个工具一下，所以把这样的类就叫做工具类。

![image-20240506163454647](image-20240506163454647.png)

#### **static应用-代码块**

代码块根据有无static修饰分为两种：静态代码块、实例代码块。

> 静态代码块，随着类的加载而执行，而且只执行一次。

![image-20240506163728436](image-20240506163728436.png)

![image-20240506163800678](image-20240506163800678.png)

> 实例代码块每次创建对象之前都会执行一次

![image-20240506163848096](image-20240506163848096.png)

![image-20240506164050846](image-20240506164050846.png)

#### **static应用-单例设计模式**

![image-20240506164625598](image-20240506164625598.png)

![image-20240506164801355](image-20240506164801355.png)

![image-20240506165039015](image-20240506165039015.png)

> 懒汉式单例

![image-20240506165339824](image-20240506165339824.png)

![image-20240506165422771](image-20240506165422771.png)

### 10 继承

面向对象编程三大特征：继承、封装和多态。

![image-20240506173728804](image-20240506173728804.png)

子类对象实际上是由子、父类两张设计图共同创建出来的

![image-20240506173944381](image-20240506173944381.png)

**继承可以提高代码的复用性**。

#### 权限修饰符

权限修饰符是用来限制类的成员（成员变量、成员方法、构造器...）能够被访问的范围。

四个权限修饰符：public（公有的）、private（私有的），protected（受保护的）、缺省的（不写任何修饰符）

![image-20240506174422400](image-20240506174422400.png)

```java
public class Fu {
    // 1、私有:只能在本类中访问
    private void privateMethod(){
        System.out.println("==private==");
    }

    // 2、缺省：本类，同一个包下的类
    void method(){
        System.out.println("==缺省==");
    }

    // 3、protected: 本类，同一个包下的类，任意包下的子类
    protected void protectedMethod(){
        System.out.println("==protected==");
    }

    // 4、public： 本类，同一个包下的类，任意包下的子类，任意包下的任意类
    public void publicMethod(){
        System.out.println("==public==");
    }

    public void test(){
        //在本类中，所有权限都可以被访问到
        privateMethod(); //正确
        method(); //正确
        protectedMethod(); //正确
        publicMethod(); //正确
    }
}
```

接下来，在和Fu类同一个包下，创建一个测试类Demo，演示同一个包下可以访问到哪些权限修饰的方法。

```java
public class Demo {
    public static void main(String[] args) {
        Fu f = new Fu();
        // f.privateMethod();	//私有方法无法使用
        f.method();
        f.protectedMethod();
        f.publicMethod();
    }
}
```

接下来，在另一个包下创建一个Fu类的子类，演示不同包下的子类中可以访问哪些权限修饰的方法。

```java
public class Zi extends Fu {
    //在不同包下的子类中，只能访问到public、protected修饰的方法
    public void test(){
        // privateMethod(); // 报错
        // method(); // 报错
        protectedMethod();	//正确
        publicMethod();	//正确
    }
}
```

接下来，在和Fu类不同的包下，创建一个测试类Demo2，演示一下不同包的无关类，能访问到哪些权限修饰的方法；

```java
public class Demo2 {
    public static void main(String[] args) {
        Fu f = new Fu();
        // f.privateMethod(); // 报错
        // f.method();		  //报错
        // f.protecedMethod();//报错
        f.publicMethod();	//正确

        Zi zi = new Zi();
        // zi.protectedMethod();
    }
}
```

#### 单继承、Object

Java语言只支持单继承，不支持多继承，但是可以多层继承

#### 方法重写

当子类觉得父类方法不好用，或者无法满足父类需求时，子类可以重写一个方法名称、参数列表一样的方法，去覆盖父类的这个方法，这就是方法重写。

**注意**：重写后，方法的访问遵循就近原则

写一个A类作为父类，定义两个方法print1和print2

```java
public class A {
    public void print1(){
        System.out.println("111");
    }

    public void print2(int a, int b){
        System.out.println("111111");
    }
}
```

再写一个B类作为A类的子类，重写print1和print2方法。

```java
public class B extends A{
    // 方法重写
    @Override // 安全，可读性好
    public void print1(){
        System.out.println("666");
    }


    // 方法重写
    @Override
    public void print2(int a, int b){
        System.out.println("666666");
    }
}
```

重写注意点：

- 1.重写的方法上面，可以加一个注解@Override,用于标注这个方法是复写的父类方法
- 2.子类复写父类方法时，访问权限必须大于或者等于父类方法的权限
	public > protected > 缺省
- 3. 重写的方法返回值类型，必须与被重写的方法返回值类型一样，或者范围更小
- 4. 私有方法、静态方法不能被重写，如果重写会报错。

#### 子类中访问成员特点

子类中访问其他成员（成员变量、成员方法），依据就近原则。

#### 子类中访问构造器的特点

- 子类全部构造器，都会先调用父类构造器，再执行自己

- 如果不想使用默认的`super()`方式调用父类构造器，还可以手动使用`super(参数)`调用父类有参数构造器。

  ![image-20240506201217549](image-20240506201217549.png)

```
访问本类成员：
	this.成员变量	//访问本类成员变量
	this.成员方法	//调用本类成员方法
	this()		   //调用本类空参数构造器
    this(参数)	  //调用本类有参数构造器
	
访问父类成员：
	super.成员变量	//访问父类成员变量
	super.成员方法	//调用父类成员方法
	super()		   //调用父类空参数构造器
    super(参数)	  //调用父类有参数构造器
    
注意：this和super访问构造方法，只能用到构造方法的第一句，否则会报错。
```

### 11 多态

多态是在继承、实现情况下的一种现象，表现为：对象多态、行为多态。

比如：Teacher和Student都是People的子类，代码可以写成下面的样子

![image-20240507102216180](image-20240507102216180.png)

在多态形式下，右边的代码是解耦合的，便于扩展和维护。

定义方法时，使用父类类型作为形参，可以接收一切子类对象，扩展行更强，更便利。

```java
public class Test2 {
    public static void main(String[] args) {
        // 目标：掌握使用多态的好处
		Teacher t = new Teacher();
		go(t);

        Student s = new Student();
        go(s);
    }

    //参数People p既可以接收Student对象，也能接收Teacher对象。
    public static void go(People p){
        System.out.println("开始------------------------");
        p.run();
        System.out.println("结束------------------------");
    }
}
```

多态形式下不能直接调用子类特有方法，但是转型后是可以调用。父类变量转换为子类类型。格式如下：

```java
//如果p接收的是子类对象
if(父类变量 instance 子类){
    //则可以将p转换为子类类型
    子类 变量名 = (子类)父类变量;
}
```

![image-20240507102955810](image-20240507102955810.png)

如果类型转换错了，就会出现类型转换异常ClassCastException。

### 12 final关键字

final关键字是最终的意思，可以修饰类、修饰方法、修饰变量

- final修饰类：该类称为最终类，特点是不能被继承

![image-20240507103455642](image-20240507103455642.png)

- final修饰方法：该方法称之为最终方法，特点是不能被重写。

![image-20240507103643803](image-20240507103643803.png)

- final修饰变量：该变量只能被赋值一次。

![image-20240507103754028](image-20240507103754028.png)

![image-20240507103805016](image-20240507103805016.png)

#### 常量

被 static final 修饰的成员变量，称之为常量，通常用于记录系统的配置信息。

代码来演示一下：

```java
public class Constant {
    //常量: 定义一个常量表示学校名称
    //为了方便在其他类中被访问所以一般还会加上public修饰符
    //常量命名规范：建议都采用大写字母命名，多个单词之前有_隔开
    public static final String SCHOOL_NAME = "test";
}
```

```java
public class FinalDemo2 {
    public static void main(String[] args) {
        //由于常量是static的所以，在使用时直接用类名就可以调用
        System.out.println(Constant.SCHOOL_NAME);
        System.out.println(Constant.SCHOOL_NAME);
        System.out.println(Constant.SCHOOL_NAME);
        System.out.println(Constant.SCHOOL_NAME);
        System.out.println(Constant.SCHOOL_NAME);
        System.out.println(Constant.SCHOOL_NAME);
        System.out.println(Constant.SCHOOL_NAME);
    }
}
```

程序编译后，常量会“宏替换”，出现常量的地方，全都会被替换为其记住的字面量。把代码反编译后，其实代码是下面的样子:

```java
public class FinalDemo2 {
    public static void main(String[] args) {
        System.out.println("test");
        System.out.println("test"E);
        System.out.println("test");
        System.out.println("test");
        System.out.println("test");
        System.out.println("test");
        System.out.println("test");
    }
}
```

### 13 抽象

关键字abstract（抽象），它可以修饰类（叫抽象类）也可以修饰方法（叫抽象方法，不允许有方法体）

```java
//abstract修饰类，这个类就是抽象类
public abstract class A{
    //abstract修饰方法，这个方法就是抽象方法
    public abstract void test();
}
```

- 抽象类是不能创建对象的，如果抽象类的对象就会报错。

- 抽象类虽然不能创建对象，但是它可以作为父类让子类继承,且子类继承父类必须重写父类的所有抽象方法。

  ```java
  //B类继承A类，必须复写test方法
  public class B extends A {
      @Override
      public void test() {
  
      }
  }
  ```

- 子类继承父类如果不复写父类的抽象方法，要想不出错，这个子类也必须是抽象类

```java
//B类基础A类，此时B类也是抽象类，这个时候就可以不重写A类的抽象方法
public abstract class B extends A {

}
```

抽象类的使用场景和好处

```
1.用抽象类可以把父类中相同的代码，包括方法声明都抽取到父类，这样能更好的支持多态，一提高代码的灵活性。

2.反过来用，我们不知道系统未来具体的业务实现时，我们可以先定义抽象类，将来让子类去实现，以方便系统的扩展。
```

### 14 模版方法模式

设计模式是解决某一类问题的最优方案。**模板方法模式主要解决方法中存在重复代码的问题**

比如A类和B类都有sing()方法，sing()方法的开头和结尾都是一样的，只是中间一段内容不一样。此时A类和B类的sing()方法中就存在一些相同的代码。

![image-20240509170815163](image-20240509170815163.png)

怎么解决上面的重复代码问题呢？ 我们可以写一个抽象类C类，在C类中写一个doSing()的抽象方法。再写一个sing()方法，代码如下：

![image-20240509170840515](image-20240509170840515.png)

最后，再写一个测试类Test

```
public class Test {
    public static void main(String[] args) {
        // 目标：搞清楚模板方法设计模式能解决什么问题，以及怎么写。
        B b = new B();
        b.sing();
    }
}
```

模板方法模式解决了多个子类中有相同代码的问题。具体实现步骤如下:

- 第1步：定义一个抽象类，把子类中相同的代码写成一个模板方法。
- 第2步：把模板方法中不能确定的代码写成抽象方法，并在模板方法中调用。
- 第3步：子类继承抽象类，只需要父类抽象方法就可以了。

### 15 接口interface

java提供了一个关键字interface，用它来定义接口这种特殊结构，格式如下：

```
public interface 接口名{
    //成员变量（常量）
    //成员方法（抽象方法）
}
```

![image-20240509171311349](image-20240509171311349.png)

接口要注意下面两点：

- 接口是用来被类实现（implements）的，我们称之为实现类。
- 一个类是可以实现多个接口的（接口可以理解成干爹），类实现接口必须重写所有接口的全部抽象方法，否则这个类也必须是抽象类

接口的好处：

- 弥补了类单继承的不足，一个类同时可以实现多个接口。
- 让程序可以面向接口编程，这样程序员可以灵活方便的切换各种业务实现。

案例演示，假设有一个Studnet学生类，还有一个Driver司机的接口，还有一个Singer歌手的接口。现在要写一个A类，想让他既是学生，偶然也是司机能够开车，偶尔也是歌手能够唱歌。那我们代码就可以这样设计，如下：

![image-20240509172146952](image-20240509172146952.png)

一个接口可以继承多个接口，接口同时也可以被类实现。

### 16 内部类

 内部类是类中的五大成分之一（成员变量、方法、构造器、内部类、代码块），如果一个类定义在另一个类的内部，这个类就是内部类。

当一个类的内部，包含一个完整的事物，且这个事物没有必要单独设计时，就可以把这个事物设计成内部类。

内部类有四种形式，分别是成员内部类、静态内部类、局部内部类、匿名内部类。

匿名内部类使用相对较多一点，匿名内部类是一种特殊的局部内部类；所谓匿名，指的是程序员不需要为这个类声明名字。

匿名内部类的格式：

```
new 父类/接口(参数值){
    @Override
    重写父类/接口的方法;
}
```

匿名内部类本质上是一个没有名字的子类对象、或者接口的实现类对象。

![image-20240509173407482](image-20240509173407482.png)

匿名内部类的作用：简化了创建子类对象、实现类对象的书写格式。

**只有在调用方法时，当方法的形参是一个接口或者抽象类，为了简化代码书写，而直接传递匿名内部类对象给方法。**这样就可以少写一个类。比如，看下面代码：

![image-20240509173532567](image-20240509173532567.png)

### 17 枚举

枚举是一种特殊的类，它的格式是：

```
public enum 枚举类名{
    枚举项1,枚举项2,枚举项3;
}
```

其实枚举项就表示枚举类的对象，只是这些对象在定义枚举类时就预先写好了，以后就只能用这几个固定的对象。

![image-20240509173839500](image-20240509173839500.png)

枚举一般表示几个固定的值，然后作为参数进行传输

### 18 泛型

泛型指的是，在定义类、接口、方法时，同时声明了一个或者多个类型变量（如：<E>），称为泛型类、泛型接口、泛型方法、它们统称为泛型。

前面学过的ArrayList类就是一个泛型类，打开API文档查看

![image-20240509174121417](image-20240509174121417.png)

- 泛型的好处：在编译阶段可以避免出现一些非法的数据。
- 泛型的本质：把具体的数据类型传递给类型变量

#### 自定义泛型类

实际工作中一般都是源代码中写好，我们直接用的，就是ArrayList<E>这样的，自己定义泛型类是非常少的，自定义泛型类的格式如下：

```
//这里的<T,W>其实指的就是类型变量，可以是一个，也可以是多个。
public class 类名<T,W>{
    
}
```

![image-20240509174419959](image-20240509174419959.png)

![image-20240509174430125](image-20240509174430125.png)

#### 自定义泛型接口

泛型接口其实指的是在接口中把不确定的数据类型用`<类型变量>`表示。定义格式如下：

```
//这里的类型变量，一般是一个字母，比如<E>
public interface 接口名<类型变量>{
    
}
```

#### 泛型方法

格式：

```
public <泛型变量,泛型变量> 返回值类型 方法名(形参列表){
    
}
```

![image-20240509174828524](image-20240509174828524.png)

![image-20240509194737575](image-20240509194737575.png)

#### 泛型限定

泛型限定的意思是对泛型的数据类型进行范围的限制。有如下的三种格式：

- <?> 表示任意类型
- <? extends 数据类型> 表示指定类型或者指定类型的子类
- <? super 数据类型> 表示指定类型或者指定类型的父类

演示一下，假设有Car作为父类，BENZ，BWM两个类作为Car的子类，代码如下：

![image-20240509195036598](image-20240509195036598.png)

#### 泛型擦除

泛型只能编译阶段有效，一旦编译成字节码，字节码中是不包含泛型的

泛型只支持引用数据类型，不支持基本数据类型

把下面的代码的字节码进行反编译

![image-20240509195159818](image-20240509195159818.png)

下面是反编译之后的代码，我们发现ArrayList后面没有泛型

![image-20240509195222000](image-20240509195222000.png)

### 19 包装类

Java中有一句很经典的话，万物皆对象。Java中的8种基本数据类型还不是对象，所以要把它们变成对象，变成对象之后，可以提供一些方法对数据进行操作。

8种基本数据类型都用一个包装类与之对一个，如下图所示

![image-20240510144338285](image-20240510144338285.png)

#### 创建包装类的对象方式、自动装箱和拆箱的特性；以Integer为例：

```java
//1.创建Integer对象，封装基本类型数据10
Integer a = new Integer(10);

//2.使用Integer类的静态方法valueOf(数据)
Integer b = Integer.valueOf(10);

//3.还有一种自动装箱的写法（意思就是自动将基本类型转换为引用类型）
Integer c = 10;

//4.有装箱肯定还有拆箱（意思就是自动将引用类型转换为基本类型）
int d = c;

//5.装箱和拆箱在使用集合时就有体现
ArrayList<Integer> list = new ArrayList<>();
//添加的元素是基本类型，实际上会自动装箱为Integer类型
list.add(100);
//获取元素时，会将Integer类型自动拆箱为int类型
int e = list.get(0);
```

#### 包装类数据类型转换

- 把字符串转换为数值型数据：包装类.parseXxx(字符串)

```
public static int parseInt(String s)
    把字符串转换为基本数据类型
```

- 将数值型数据转换为字符串：包装类.valueOf(数据);

```
public static String valueOf(int a)
    把基本类型数据转换为
```

![image-20240510144917163](image-20240510144917163.png)

### 20 常用API

#### 1. Object类

Object类是Java中所有类的祖宗类，因此，Java中所有类的对象都可以直接使用Object类中提供的一些方法。

- clone()
- equals(Object obj)
- toString()

#### 2. Objects类

Objects是一个工具类，提供了一些方法可以对任意对象进行操作。主要方法如下

![image-20240510145748115](image-20240510145748115.png)

Object也有equals，Objects有equals，那两者有什么区别呢？

![image-20240510145915640](image-20240510145915640.png)

Object的equals方法前提是对象不能为null，Objects则可以，使用更安全。

#### 3. StringBuilder类

- StringBuilder代表可变字符串对象，相当于是一个容器，它里面的字符串是可以改变的，就是用来操作字符串的。

- 好处：StringBuilder比String更合适做字符串的修改操作，效率更高，代码也更加简洁。

  ![image-20240510150136587](image-20240510150136587.png)

为什么说StringBuilder对字符串进行操作比String效率高？

![image-20240510150212090](image-20240510150212090.png)

直接使用Stirng拼接100万次，等了1分钟，还没结束，但是使用StringBuilder做拼接，不到1秒钟出结果了，why？

简单说：String是不可变对象，而StringBuilder在拼接时只是把字符串转为char拷贝到char[]

String对象不可变，则每次拼接都会创建新的String对象。即使在新的jdk有对`String+`的优化，仍然是效率不够高，比如每次循环拼接时都会被自动创建一个StringBuider对象来append，最后还会将该对象调用toString()方法。

![image-20240510152257362](image-20240510152257362.png)

StringBuilder其实就是个char[]，append时，是将String对象转为char后放入StringBuilder的char[]内。当长度不够放时，对该char[]扩容即可。

![image-20240510152318548](image-20240510152318548.png)

#### 4. StringJoiner

StringJoiner号称是拼接神器，不仅效率高，而且代码简洁

![image-20240510152549736](image-20240510152549736.png)

#### 5. Math类

Math是数学的意思，该类提供了很多个进行数学运算的方法，如求绝对值，求最大值，四舍五入等。

```java
public class MathTest {
    public static void main(String[] args) {
        // 目标：了解下Math类提供的常见方法。
        // 1、public static int abs(int a)：取绝对值（拿到的结果一定是正数）
        //    public static double abs(double a)
        System.out.println(Math.abs(-12)); // 12
        System.out.println(Math.abs(123)); // 123
        System.out.println(Math.abs(-3.14)); // 3.14

        // 2、public static double ceil(double a): 向上取整
        System.out.println(Math.ceil(4.0000001)); // 5.0
        System.out.println(Math.ceil(4.0)); // 4.0

        // 3、public static double floor(double a): 向下取整
        System.out.println(Math.floor(4.999999)); // 4.0
        System.out.println(Math.floor(4.0)); // 4.0

        // 4、public static long round(double a)：四舍五入
        System.out.println(Math.round(3.4999)); // 3
        System.out.println(Math.round(3.50001)); // 4

        // 5、public static int max(int a, int b)：取较大值
        //   public static int min(int a, int b)：取较小值
        System.out.println(Math.max(10, 20)); // 20
        System.out.println(Math.min(10, 20)); // 10

        // 6、 public static double pow(double a, double b)：取次方
        System.out.println(Math.pow(2, 3)); // 2的3次方   8.0
        System.out.println(Math.pow(3, 2)); // 3的2次方   9.0

        // 7、public static double random()： 取随机数 [0.0 , 1.0) (包前不包后)
        System.out.println(Math.random());
    }
}
```

#### 6. System类

System类，提供了一些获取获取系统数据的方法。比如获取系统时间

```java
/**
 * 目标：了解下System类的常见方法。
 */
public class SystemTest {
    public static void main(String[] args) {

        // 1、public static void exit(int status):
        //   终止当前运行的Java虚拟机。
        //   该参数用作状态代码; 按照惯例，非零状态代码表示异常终止。
        System.exit(0); // 人为的终止虚拟机。(不要使用)

        // 2、public static long currentTimeMillis():
        //    获取当前系统的时间
        //    返回的是long类型的时间毫秒值：指的是从1970-1-1 0:0:0开始走到此刻的总的毫秒值，1s = 1000ms
        long time = System.currentTimeMillis();
        System.out.println(time);

        for (int i = 0; i < 1000000; i++) {
            System.out.println("输出了：" + i);
        }

        long time2 = System.currentTimeMillis();
        System.out.println((time2 - time) / 1000.0 + "s");
    }
}
```

#### 7. Runtime类

运行时类叫Runtime类，这个类可以用来获取JVM的一些信息，也可以用这个类去执行其他的程序

![image-20240510160528198](image-20240510160528198.png)

#### 8. BigDecimal类

![image-20240510160659140](image-20240510160659140.png)

BigDecimal的出现是为了解决计算精度损失的问题。它提供了一些方法可以对数据进行四则运算，而且不丢失精度，同时还可以保留指定的小数位。

```java
public class Test2 {
    public static void main(String[] args) {
        // 目标：掌握BigDecimal进行精确运算的方案。
        double a = 0.1;
        double b = 0.2;

        // 1、把浮点型数据封装成BigDecimal对象，再来参与运算。
        // a、public BigDecimal(double val) 得到的BigDecimal对象是无法精确计算浮点型数据的。 注意：不推荐使用这个，
        // b、public BigDecimal(String val)  得到的BigDecimal对象是可以精确计算浮点型数据的。 可以使用。
        // c、public static BigDecimal valueOf(double val): 通过这个静态方法得到的BigDecimal对象是可以精确运算的。是最好的方案。
        BigDecimal a1 = BigDecimal.valueOf(a);
        BigDecimal b1 = BigDecimal.valueOf(b);

        // 2、public BigDecimal add(BigDecimal augend): 加法
        BigDecimal c1 = a1.add(b1);
        System.out.println(c1);

        // 3、public BigDecimal subtract(BigDecimal augend): 减法
        BigDecimal c2 = a1.subtract(b1);
        System.out.println(c2);

        // 4、public BigDecimal multiply(BigDecimal augend): 乘法
        BigDecimal c3 = a1.multiply(b1);
        System.out.println(c3);

        // 5、public BigDecimal divide(BigDecimal b): 除法
        BigDecimal c4 = a1.divide(b1);
        System.out.println(c4);

//        BigDecimal d1 = BigDecimal.valueOf(0.1);
//        BigDecimal d2 = BigDecimal.valueOf(0.3);
//        BigDecimal d3 = d1.divide(d2);
//        System.out.println(d3);

        // 6、public BigDecimal divide(另一个BigDecimal对象，精确几位，舍入模式) : 除法，可以设置精确几位。
        BigDecimal d1 = BigDecimal.valueOf(0.1);
        BigDecimal d2 = BigDecimal.valueOf(0.3);
        BigDecimal d3 = d1.divide(d2,  2, RoundingMode.HALF_UP); // 0.33
        System.out.println(d3);

        // 7、public double doubleValue() : 把BigDecimal对象又转换成double类型的数据。
        //print(d3);
        //print(c1);
        double db1 = d3.doubleValue();
        double db2 = c1.doubleValue();
        print(db1);
        print(db2);
    }

    public static void print(double a){
        System.out.println(a);
    }
}
```

### 21 日期类

#### 1. Date类

Java中是由Date类的对象表示日期或者时间。Date对象记录的时间是用毫秒值来表示的。

Java语言规定，1970年1月1日0时0分0秒认为是时间的起点，此时记作0，那么1000（1秒=1000毫秒）就表示1970年1月1日0时0分1秒，依次类推。

![image-20240510161315322](image-20240510161315322.png)

Date类的构造方法，和常见的成员方法

![image-20240510161655966](image-20240510161655966.png)

![image-20240510161727189](image-20240510161727189.png)

#### 2. SimpleDateFormat

- 把Date对象转换为指定格式的日期字符串这个操作，叫做**日期格式化**
- 反过来把指定格式的日期符串转换为Date对象的操作，叫做**日期解析

![image-20240510161847571](image-20240510161847571.png)

注意：创建SimpleDateFormat对象时，在构造方法的参数位置传递日期格式，而日期格式是由一些特定的字母拼接而来的。我们需要记住常用的几种日期/时间格式

```
字母	   表示含义
yyyy	年
MM		月
dd		日
HH		时
mm		分
ss		秒
SSS		毫秒

"2022年12月12日" 的格式是 "yyyy年MM月dd日"
"2022-12-12 12:12:12" 的格式是 "yyyy-MM-dd HH:mm:ss"
按照上面的格式可以任意拼接，但是字母不能写错
```

上代码演示一下

![image-20240510161942363](image-20240510161942363.png)

#### 3. Calendar类

Calendar类表示日历，它提供了一些比Date类更好用的方法。

![image-20240510162355817](image-20240510162355817.png)

用Date类就不太好做，而用Calendar就特别方便。因为Calendar类提供了方法可以直接对日历中的年、月、日、时、分、秒等进行运算。

![image-20240510162422251](image-20240510162422251.png)

#### 4. JDK8日期、时间、日期时间

为什么以前的Date类就可以表示日期，为什么要有新增的日期类呢？

![image-20240510162617601](image-20240510162617601.png)

JDK8新增的日期类分得更细致一些，比如表示年月日用LocalDate类、表示时间秒用LocalTime类、而表示年月日时分秒用LocalDateTime类等；除了这些类还提供了对时区、时间间隔进行操作的类等。它们几乎把对日期/时间的所有操作都通过了API方法，用起来特别方便。

![image-20240510162700984](image-20240510162700984.png)

- LocalDate类的基本使用

  ![image-20240510163143116](image-20240510163143116.png)

- LocalTime类的基本使用

- LocalDateTime类的基本使用

  ![image-20240510163231996](image-20240510163231996.png)

#### 5. JDK8日期（时区）

由于世界各个国家与地区的经度不同，各地区的时间也有所不同，因此会划分为不同的时区。每一个时区的时间也不太一样。

![image-20240510163335612](image-20240510163335612.png)

![image-20240510163445694](image-20240510163445694.png)

#### 6. JDK8日期（Instant类）

通过获取Instant的对象可以拿到此刻的时间，该时间由两部分组成：从1970-01-01 00:00:00 开始走到此刻的总秒数+不够1秒的纳秒数。

该类提供的方法如下图所示，可以用来获取当前时间，也可以对时间进行加、减、获取等操作。

![image-20240510163610933](image-20240510163610933.png)

作用：可以用来记录代码的执行时间，或用于记录用户操作某个事件的时间点。

![image-20240510163651157](image-20240510163651157.png)

#### 7. JDK8日期（格式化器）

![image-20240513144441716](image-20240513144441716.png)

![image-20240513144513507](image-20240513144513507.png)

演示一下

```java
/**
 *  目标：掌握JDK 8新增的DateTimeFormatter格式化器的用法。
 */
public class Test6_DateTimeFormatter {
    public static void main(String[] args) {
        // 1、创建一个日期时间格式化器对象出来。
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH:mm:ss");

        // 2、对时间进行格式化
        LocalDateTime now = LocalDateTime.now();
        System.out.println(now);

        String rs = formatter.format(now); // 正向格式化
        System.out.println(rs);

        // 3、格式化时间，其实还有一种方案。
        String rs2 = now.format(formatter); // 反向格式化
        System.out.println(rs2);

        // 4、解析时间：解析时间一般使用LocalDateTime提供的解析方法来解析。
        String dateStr = "2029年12月12日 12:12:11";
        LocalDateTime ldt = LocalDateTime.parse(dateStr, formatter);
        System.out.println(ldt);
    }
}
```

#### 8. JDK8日期（Period类）

![image-20240513144701091](image-20240513144701091.png)

先来演示Period类的用法，它的方法如下图所示。可以用来计算两个日期之间相隔的年、相隔的月、相隔的日。**只能两个计算LocalDate对象之间的间隔**

![image-20240513144742162](image-20240513144742162.png)

#### 9. JDK8日期（Duration类）

**可以用于计算两个时间对象相差的天数、小时数、分数、秒数、纳秒数；支持LocalTime、LocalDateTime、Instant等时间**

![image-20240513144902194](image-20240513144902194.png)

---



[下一篇《Java学习笔记（二）》](../2024-05-13-learn-java2)



## *参考*

[Java程序员学习路线图](https://yun.itheima.com/subject/javamap/index.html)

[Java入门基础视频教程(B站)](https://www.bilibili.com/video/BV1Cv411372m/?spm_id_from=333.999.0.0) 

[Java基础教程(YouTube)](https://www.youtube.com/watch?v=VqfGCmjQt10)

[JavaWeb开发教程(B站)](https://www.bilibili.com/video/BV1m84y1w7Tb/?vd_source=4d819443886ce5506c7c6b65b4a7ad93)