# JavaSE

## 代码实例

### 字符串

```java
import java.security.PublicKey;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        String s1 = "acd";

        String s2 = new String();//使用次数较少

        char[] c1 = {'a', 'c', 'd'};

        String s3 = new String(c1);

        byte[] b1 = {'5', '4'};

        String s4 = new String(b1);

        String s5 = "acd";

        String s6 = "ACD";

        Scanner sc=new Scanner(System.in);
        String s7=sc.next();
        System.out.println(s7);
        System.out.println(s1);
        System.out.println(s2);
        System.out.println(s3);
        System.out.println(s4);
        System.out.println(s7);
        System.out.println("------------------------------------------------------------------");
        System.out.println(s1 == s3);//地址值不一样 false
        System.out.println(s1 == s5);//地址值一样，string的复用性 true

        //equal 方法比较的是字符串本身
        //equalignorecase 会忽略比较的的字符串之间的大小写
        //Scanner 底层利用了new 关键字 在堆中开辟了一块内存
        //String s=""   利用了串池 stringtable jdk7 以前在方法区，在以后的版本串池被移入堆内存中
        System.out.println(s1.equals(s3));//返回为 true
        System.out.println(s1.equalsIgnoreCase(s6)); //return true
        System.out.println(s1 == s7);//return false
        System.out.println(s1.equals(s7));//return true
        System.out.println("-------------------------------------------------------------------");

        Scanner sc1=new Scanner(System.in);
        String s8 = sc1.next();
        System.out.println(s8);
        for (int i = 0; i < s8.length(); i++) {
            //charat 利用字符串的索引返回对应的字符
            char c2=s8.charAt(i);
            System.out.println(c2);
        }
        System.out.println("--------------------------------------------------------------------");

        int [] i1={1117,0221,804,904,218};
        String s13 = arrTostring(i1);
        System.out.println(s13);
        String s14="zfdsgjbhdhdjgh";
        System.out.println(s14.substring(1, 2));//substring方法 截取字符串
        System.out.println(s14.replace("z", "!"));//字符串中字符的替换
    }
    public static String arrTostring(int  []  arr) {
        if (arr.length == 0) {
            return "字符为空";
        } else if (arr==null) {
            return"";

        }
        String s12="[";
        for (int i = 0; i < arr.length; i++) {

            if(i== arr.length-1){
                s12=s12+arr[i]+"]";
                break;
            }
            s12=s12+arr[i]+",";
        }
        return s12;
    }
}

```

#### 字符串容器StringBuilder

```java
import java.util.Scanner;
import java.util.StringJoiner;

public class Main {
    public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        String s2 = sc.next();

        System.out.println(reverse(s2));

        StringBuilder sb1=new StringBuilder("hello world!");
        System.out.println(sb1.reverse());//此处直接输出STringbuilder的反转 !dlrow olleh
        //reverse(sb1);//此处报错，sb1为Stringbuilder对象
        System.out.println(reverse(sb1.toString()));//此处转换对象类型即可使用  hello world!
        System.out.println(sb1);//!dlrow olleh 此处sb1对象已经被反转
        System.out.println(sb1.append("Bye!")); //!dlrow ollehFuch u
        System.out.println(sb1);//!dlrow ollehFuch u
        System.out.println(sb1.length());
        //PS：SB对象中的数据是可以直接改变，但是string 类型的数据无法直接对其进行操作
        System.out.println(boolreverse(s2));

    }
    public static  String reverse(String  arr){

        String s1="";

        for (int length = arr.length()-1; length >= 0; length--) {

                char c=arr.charAt(length);
                s1=s1+c;
        }
        return s1;
    }
    public static boolean boolreverse(String s1){
        Scanner sc=new Scanner(System.in);
        String s2 = sc.next();
        StringBuilder sb=new StringBuilder(s2);
        if(s2.equals(sb.reverse().toString())){
            return true;
        }else {
            return false;
        }
    }
    public  static String arrTostring(int[]arr){
        StringJoiner sj=new StringJoiner(",","","]");
        for (int i = 0; i < arr.length - 1; i++) {
            sj.add("---");
        }
        return sj.toString();

    }
}

```

### 泛型

```java
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        MyArraylist<String> MYlist=new MyArraylist<>();
        //MyArraylist3<Integer> list5=new MyArraylist3();

        //由于定义中的给定泛型为String 所以在在上一行的Integer 类型会报错，（错误名为没有类型形参）
        MyArraylist3 list6=new MyArraylist3();//默认创建的是String 类型


        System.out.println("------------------------------------------------------------------------");

        //泛型不具备继承性，但数据可以继承
        ArrayList<ye> list7=new ArrayList<>();
        ArrayList<fu> list8=new ArrayList<>();
        ArrayList<zi> list9=new ArrayList<>();
        method1(list7);
        method1(list8);
        method1(list9);//此处在method1使用了E所以可以使用所有类型的变量

        System.out.println("------------------------------------------------------------------------");

        method2(list7);
        method2(list8);
        method2(list9);//此处使用method2使用了? extends E


        System.out.println("------------------------------------------------------------------------");


        method3(list7);
        method3(list8);
        method3(list9);//此处使用了method3使用了? super E


    }
    public static <E>void method1(ArrayList<E> list7){}
    public static void method2(ArrayList<? extends ye> list7){}//? extends E 表示可以从传递E或者E的子类
    public static void method3(ArrayList<? super zi> list7){}//? super E 表示可以从传递E或者E的父类

}
class ye{};
class fu extends ye{};
class zi extends fu{};
```

#### 泛型小结

```java
import java.util.ArrayList;
import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        ArrayList list=new ArrayList<>();
        list.add("aaa");
        list.add("bbb");
        //如果没有给集合添加特定类型，集合的所有数据类型都是obj类型，
        //优点是可以添加任何类型的元素
        //缺点是不能使用add等特有操作，就算使用了类型强转，也容易发生类型转换错误
        //添加泛型可以统一集合的数据类型
        //Java中的泛型是伪泛型，底层使用了强转
        list.add(new Student(18,"zhengsan"));
        Iterator it = list.iterator();
        //创建迭代器对象，其中的迭代器泛型与集合的泛型一致
        while(it.hasNext()){
            Object next = it.next();
            //next.add;//该行会报错，原因是多态不能访问子类特有的功能
        }
        MyArraylist<Integer> list1=new MyArraylist<>();//自定义泛型类，使用E泛型保证数据多样
        list1.add(123);
        list1.add(456);
        list1.add(789);
        System.out.println(list1.tostring());
        System.out.println("----------------------------------------------------------");
        ArrayList<String> list4=new ArrayList<>();
        util.add(list4,"aaaaa","cccc","a","deeeee","aaaaa","aaaaa");
        System.out.println(list4);
    }
}
```



### 递归

```java
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        int sum=0;
        for (int i = 10; i <= 20; i++) {
            sum=sum+factorial(i);
        }
        System.out.println(sum);

    }
    public static int factorial(int num){
        if(num==0){
            return 1;
        }else {
            return (num*factorial(num-1));//递归调用计算阶乘
        }
    }
}
```

### 集合

#### List集合

```java
import com.sun.jdi.IntegerValue;

import java.sql.SQLOutput;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;

public class Main {
    public static void main(String[] args) {
        List<String> list=new ArrayList<>();
        list.add("nihao");
        list.add("HI");
        list.add("China");
        list.add("3");
        //startwith方法，顾名思义
        System.out.println("------------------------------------------");
        System.out.println(list);
        System.out.println("------------------------------------------");
        //在索引处添加需要的元素
        list.add(1,"adad");
        System.out.println(list);//[nihao, adad, HI, China, 3]

        System.out.println("------------------------------------------");
        //在索引处删除指定的元素同时返回被删除的元素
        list.remove(3);

        //手动装箱
        Integer i= Integer.valueOf(3);
        list.remove(i);
        System.out.println(list);//[nihao, adad, HI, 3]
        System.out.println("------------------------------------------");
        //set方法修改指定索引的元素
        //get方法获取指定索引的元素
        String s1=list.set(3,"kkkkkk");
        list.get(2);
        System.out.println(s1);//3
        System.out.println(list);//[nihao, adad, HI, kkkkkk]

        System.out.println("------------------------------------------");
        //迭代器遍历
        Iterator<String> it= list.iterator();
        while(it.hasNext()){
            System.out.println(it.next());

        }
        System.out.println("------------------------------------------");
        //增强for
        for (String s:list){
            System.out.println(s);
        }
        System.out.println("------------------------------------------");
        //Lambda遍历
        list.forEach(s -> System.out.println(s));
        System.out.println("------------------------------------------");
        //列表迭代器
        //区别是可以在遍历的时候修改元素
        ListIterator<String>it1= list.listIterator();
        while(it1.hasNext()){


            String str= it1.next();
            if("HI".equals(str)){
                it1.add("klkl");
            }
            System.out.println(str);
        }
        System.out.println("------------------------------------------");
        System.out.println("------------------------------------------");
    }
}
```

#### Map与Hashmap集合

```java
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

public class Main {
    public static void main(String[] args) {
        //map主要是键值对的
        //map是一个接口，所以创建对象必须要创建实现类的对象
        Map<String,String>m1=new HashMap<>();
        m1.put("郭靖","黄蓉");//put添加数据（键值对的形式）
        m1.put("aa","bb");
        m1.put("aa","cc");
        m1.put("bb","ee");
        m1.put("kk","gg");
        //put方法的细节：
        //添加数据的时候，如果键不存在，就会把数据添加在map中
        //在添加数据时，如果数据存在，就会把原有的键值对对象覆盖，同时会把被覆盖的值返回
        System.out.println(m1.put("aa", "dd"));//此处cc被覆盖 输出cc
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1.remove("bb"));//返回键对应的被删除的值
        System.out.println(m1.remove("cc"));//null  不存在返回为空
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1.containsKey("aa"));//true 存在返回就真（其返回类型为布尔类型）
        System.out.println(m1.containsKey("cc"));//false
        System.out.println(m1.containsValue("ee"));//false 此处false因为上面移除了bb键值对
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1);//集合打印  {aa=dd, kk=gg, 郭靖=黄蓉}
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1.size());//集合的长度  3
        System.out.println("-----------------------------------------------------------------");
        m1.clear();//清空集合
        System.out.println(m1.isEmpty());//true
        System.out.println("-----------------------------------------------------------------");
        //map的遍历方式
        //1.键找值的方法
        Map<String,String> m2 =new HashMap<>();
        m1.put("aa","AA");
        m1.put("bb","BB");
        m1.put("cc","CC");
        //增强for遍历方式
        Set<String> keys = m1.keySet();
        for (String s : keys) {
            System.out.println(s);
        }
        System.out.println("-----------------------------------------------------------------");
        //LAmbda遍历
        keys.forEach(s -> System.out.println(s));
        System.out.println("-----------------------------------------------------------------");
        //迭代器遍历
        Iterator<String> it1= keys.iterator();//创建迭代器对象
        while (it1.hasNext()){
            System.out.println(it1.next());
        }
        System.out.println("-----------------------------------------------------------------");
        //第二种遍历方式，键值对遍历
        Map<String,String> m3=new HashMap<>();
        m3.put("AA","BB");
        m3.put("bb","CC");
        m3.put("cc","DD");
        Set<Map.Entry<String, String>> en1 = m3.entrySet();//返回键值对对象，其中前者接受的泛型为键值对
        //Lambda表达式遍历
        en1.forEach(stringStringEntry -> System.out.println(stringStringEntry));
        System.out.println("-----------------------------------------------------------------");
        //增强for
        for (Map.Entry<String, String> stringStringEntry : en1) {
            System.out.println(en1);
        }
        System.out.println("-----------------------------------------------------------------");
        //迭代器遍历
        Iterator<Map.Entry<String, String>> it3=en1.iterator();//Map.Entry<String, String>，此时创建的迭代器的对象泛型需要使用键值对的类型，否则会报错，前后对应的关系
        while (it3.hasNext()){
            System.out.println(it3.next());
        }
        System.out.println("-----------------------------------------------------------------");
        //Lambda表达式遍历map
        Map<String,String> m4=new HashMap<>();
        m3.put("hh","JJ");
        m3.put("jj","KK");
        m3.put("ll","FF");
        System.out.println("-----------------------------------------------------------------");
        m3.forEach((s, s2) -> System.out.println(s +"="+s2));//此处的sout中不能直接写(s,s2),会报错,可以写成(s +"="+s2)
        System.out.println("-----------------------------------------------------------------");
        //hashmap都用的map的方法，没有其余的方法
        //1，hashmap时map里的一个实现类
        //2，方法用map的方法
        //3，特点由键值对决定（无序，不重复，无索引）
        //4，hashmap和hashset的底层原理都是哈希表结构（数组加链表，同时还会有红黑树）
        //hashmap的底层是哈希表，依靠hashcode方法，和equals方法保证键的唯一，如果建存储的是自定义对象，需要重写hashcode和equals方法，如果值存储自定义对象，则不需要重写上述两种方法
    }
}
```

#### Hashtree

```java
import java.lang.invoke.LambdaConversionException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.TreeSet;
import java.util.function.Consumer;

public class Main {
    public static void main(String[] args) {
        Student s1=new Student("zhangsan",18);
        Student s2=new Student("zhangsan",18);
        Student s3=new Student("lisi",18);
        System.out.println(s1.hashCode());//-1461067297
        System.out.println(s2.hashCode());//s1=s2在类中重写了hashcode的方法，使其对属性值进行计算，属性相同哈希值相同
        System.out.println(s3.hashCode());//102983072
        System.out.println("===========================================================================");

        System.out.println("abc".hashCode());
        System.out.println("abc".hashCode());//String内部重写了hashcode方法
        System.out.println("acb".hashCode());
        System.out.println("===========================================================================");



        //hashset可以保证在添加数据时可以去重
        //通过equals方法 以及hashcode保证数据不会重复
        //必须要在对象类中重写hsahcode以及equals方法（快捷键是alt insert 方法）
        //在new是开辟了新空间地址值不一样，所以在创建属性值相同时时也不会去重，因为他俩地址值不一样，这也是在面对在面对自定义对象时必须要重写hashcode 以及equals 方法
        //但对于Integer String 来说，Java在底层已经重写好了他们的这两个方法，保证这两只数据的遍历使用

        Student s4=new Student("aa",12);
        Student s5=new Student("bb",13);
        Student s6=new Student("cc",15);
        Student s7=new Student("aa",12);

        HashSet<Student> set1=new HashSet<>();
        boolean b1 = set1.add(s4);//true
        boolean b2 = set1.add(s5);//true
        boolean b3 = set1.add(s6);//true
        boolean b4 = set1.add(s7);//false
        System.out.println(b1);
        System.out.println(b2);
        System.out.println(b3);
        System.out.println(b4);

        System.out.println("===========================================================================");
        //Linkedhashset
        //有序，无重复 无索引
        //底层利用了双向链表，保证数据的添加顺序，在最后读取时，也通过双向链表进行读取
        Student s8=new Student("aa",11);//true
        Student s9=new Student("bb",11);//true
        Student s10=new Student("cc",11);//true
        Student s11=new Student("aa",11);//false
        LinkedHashSet<Student> linkedHashSet=new LinkedHashSet<>();

        System.out.println(linkedHashSet.add(s8));
        System.out.println(linkedHashSet.add(s9));
        System.out.println(linkedHashSet.add(s10));
        System.out.println(linkedHashSet.add(s11));
        System.out.println(linkedHashSet);
        System.out.println("===========================================================================");
        new eat(){
            //匿名内部类
            //eat为接口名

            @Override
            public void eat() {
                System.out.println("在吃饭");
            }
        };
        System.out.println("===========================================================================");

        //Treeset 有序的，无索引，无重复
        TreeSet<Integer> ts=new TreeSet<>();
        System.out.println(ts.add(1));//true
        System.out.println(ts.add(4));//true
        System.out.println(ts.add(2));//true
        System.out.println(ts.add(3));//true
        System.out.println(ts.add(1));//false
        System.out.println(ts);//[1, 2, 3, 4]

        System.out.println("===========================================================================");

        //迭代器遍历
        Iterator<Integer> it2= ts.iterator();
        while(it2.hasNext()){
            System.out.println(it2.next());
        }

        //增强for

        for(int i:ts){
            System.out.println(i);
        }

        //Lambda遍历

        ts.forEach(integer -> System.out.println(integer));

        //下方使用了匿名内部类改进得到上方的Lambda遍历
        ts.forEach(new Consumer<Integer>() {
            @Override
            public void accept(Integer integer) {
                System.out.println(integer);
            }
        });



        System.out.println("===========================================================================");

        Student ss1=new Student("aa",1);
        Student ss2=new Student("bb",2);
        Student ss3=new Student("kk",5);
        Student ss4=new Student("cc",3);
        Student ss5=new Student("dd",3);
        Student ss6=new Student("aa",1);
        Student ss7=new Student("aa",2);

        TreeSet<Student>ts1=new TreeSet<>();
        System.out.println(ts1.add(ss1));//true
        System.out.println(ts1.add(ss2));//true
        System.out.println(ts1.add(ss3));//true
        System.out.println(ts1.add(ss4));//true
        System.out.println(ts1.add(ss5));//false  虽然属性值不是完全相同但是年龄相同，再重写的compareto 方法中是根据年龄比较的，所以在集合中根据年龄排序
        System.out.println(ts1.add(ss6));//false
        System.out.println(ts1.add(ss7));//false
        System.out.println(ts1);//[Student{name = aa, age = 1}, Student{name = bb, age = 2}, Student{name = cc, age = 3}, Student{name = kk, age = 5}]
        //只要数据有重复就会去重，无论是年龄还是名字
        //言多必失


        System.out.println("===========================================================================");
        TreeSet<String> ts3=new TreeSet<>((o1, o2) -> {
            //创建比较器的对象，（使用匿名内部类改进得到Lambda表达式的写法，
            int i=o1.length()-o2.length();
            i=i==0? o1.compareTo(o2):i;//按照字符串的长度进行红黑树的比较，从小到大
            return i;
        });
        System.out.println(ts3.add("m"));//true
        System.out.println(ts3.add("aad"));//true
        System.out.println(ts3.add("ef"));//true
        System.out.println(ts3.add("gaaaaaa"));//[m, ef, aad, gaaaaaa]
        System.out.println(ts3);
        System.out.println("===========================================================================");
        System.out.println("===========================================================================");
    }
}

//学生类
import java.util.Objects;

public class Student implements Comparable<Student>{
    private String name;
    private int age;

    public Student() {
    }

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Student student = (Student) o;
        return age == student.age && Objects.equals(name, student.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + "}";
    }

    @Override
    public int compareTo(Student o) {
        return this.getAge()-o.getAge();
        //-1 表示添加的元素比当前元素小，按要求加载红黑树中
        //1 表示添加的元素比当前元素大，按要求加载红黑树中
        //0 表示添加的元素已经有相同，不加载红黑树中
    }
}


public interface eat {
    public  void eat();
}

```

#### Treemap集合

```java
import java.util.TreeMap;

public class Main {
    public static void main(String[] args) {

        //Treemap底层为红黑树的结构，不重复无索引，实现comparato比较器对象，指定比较规则，或者实现comparable的接口，指定比较规则(此时不重复无索引，是指键的关系)
        //基于红黑树的结构，增删改查的性能比较好

        TreeMap<Character,Integer>tm1=new TreeMap<>();
        String s1="abcddeabaebb";
        for (int i = 0; i < s1.length(); i++) {
            char c1=s1.charAt(i);
            //利用countainskey对集合进行判断，当其存在时，创建一个整形，将c1字符的数量进行提取，并且自增，最终将count和c1进行添加到集合中，输出结果
            //关键为对字符串的遍历时，对字符串的每一个字符进行提取，字符串调用charAt(index)的方法(其中index为字符串中每个字符的索引)，常用fori遍历，其中i即为字符串的索引
            if(tm1.containsKey(c1)){
                int count=tm1.get(c1);
                count++;
                tm1.put(c1,count);
            }else{
                tm1.put(c1,1);
            }
        }
        System.out.println(tm1);
        System.out.println("----------------------------------------------");
        StringBuilder sb1=new StringBuilder();
        tm1.forEach((character, integer) -> sb1.append("(").append(character).append(":").append(integer).append(")"));
        System.out.println(sb1);
    }
}
```

#### Treeset

```java
import java.util.TreeSet;

public class Main {
    public static void main(String[] args) {

        Student s1 = new Student("aa", 56, 24, 55, 45, 55);
        Student s2 = new Student("bb", 42, 54, 41, 45, 66);
        Student s3 = new Student("cc", 56, 78, 65, 79, 77);
        Student s4 = new Student("dd", 44, 43, 60, 99, 88);
        Student s5 = new Student("aa", 34, 21, 79, 77, 99);
        TreeSet<Student> ts = new TreeSet<>();
        System.out.println(ts.add(s1));
        System.out.println(ts.add(s2));
        System.out.println(ts.add(s3));
        System.out.println(ts.add(s4));
        System.out.println(ts.add(s5));

        System.out.println(ts);
        for (Student s:ts){
            System.out.println(s);
        }
    }
}


//////////////////////////////////


public class Student implements Comparable<Student> {
    private String Name;
    private int Age;
    private int Chinese;
    private int Math;
    private int English;
    private int Allscore;

    public Student() {
    }

    public Student(String Name, int Age, int Chinese, int Math, int English, int Allscore) {
        this.Name = Name;
        this.Age = Age;
        this.Chinese = Chinese;
        this.Math = Math;
        this.English = English;
        this.Allscore = Allscore;
    }

    /**
     * 获取
     * @return Name
     */
    public int allscore(){
        return this.getEnglish()+this.getChinese()+this.getMath();
    }
    public String getName() {
        return Name;
    }

    /**
     * 设置
     * @param Name
     */
    public void setName(String Name) {
        this.Name = Name;
    }

    /**
     * 获取
     * @return Age
     */
    public int getAge() {
        return Age;
    }

    /**
     * 设置
     * @param Age
     */
    public void setAge(int Age) {
        this.Age = Age;
    }

    /**
     * 获取
     * @return Chinese
     */
    public int getChinese() {
        return Chinese;
    }

    /**
     * 设置
     * @param Chinese
     */
    public void setChinese(int Chinese) {
        this.Chinese = Chinese;
    }

    /**
     * 获取
     * @return Math
     */
    public int getMath() {
        return Math;
    }

    /**
     * 设置
     * @param Math
     */
    public void setMath(int Math) {
        this.Math = Math;
    }

    /**
     * 获取
     * @return English
     */
    public int getEnglish() {
        return English;
    }

    /**
     * 设置
     * @param English
     */
    public void setEnglish(int English) {
        this.English = English;
    }

    /**
     * 获取
     * @return Allscore
     */
    public int getAllscore() {
        return Allscore;
    }

    /**
     * 设置
     * @param Allscore
     */
    public void setAllscore(int Allscore) {
        this.Allscore = Allscore;
    }

    public String toString() {
        return "Student{Name = " + Name + ", Age = " + Age + ", Chinese = " + Chinese + ", Math = " + Math + ", English = " + English + ", Allscore = " + Allscore + "}";
    }

    @Override
    public int compareTo(Student o) {
        int sumofthis=this.allscore();
        int sumofo=o.allscore();
        int i=sumofthis-sumofo;
        i=i==0? this.getChinese()-o.Chinese:i;
        i=i==0? this.getMath()-o.Math:i;
        i=i==0?this.getEnglish()-o.getEnglish():i;
        i=i==0?this.getAge()-o.getAge():i;
        i=i==0?this.getName().compareTo(o.getName()):i;
        return i;
    }
}

```



### 正值表达式

```java
public class Main {
    public static void main(String[] args) {


        System.out.println("---------------------------------------------------");

        String regex1 = "1[3-9]\\d{9}";//手机号码
        System.out.println("手机号码");



        System.out.println("13251083456".matches(regex1));//true
        System.out.println("1325108345".matches(regex1));//false
        System.out.println("132adadadd5".matches(regex1));//false


        System.out.println("---------------------------------------------------");

        String regex2 = "[2-9]\\d{5,11}";//QQ号码
        System.out.println("QQ号码");


        System.out.println("838992123".matches(regex2));//true
        System.out.println("838adad".matches(regex2));//false
        System.out.println("8323".matches(regex2));//false

        System.out.println("---------------------------------------------------");


        String regex3="\\w{6,9}@[\\w^_]{2,7}(\\.com|\\.cn){1,2}";
        System.out.println("邮箱号码");



        System.out.println("123134@qq.com".matches(regex3));//true
        System.out.println("123134qq.com".matches(regex3));//false
        System.out.println("123d34@q.com.cn".matches(regex3));//false
        System.out.println("1ada34@qq.c".matches(regex3));//false
        System.out.println("123aad4@qq.cm".matches(regex3));//false


        System.out.println("-------------------------------------------------------------------------");

        String regex4="((?i)\\w){1,9}";
        System.out.println("忽略大小写的1-9位字符");



        System.out.println("dadad".matches(regex4));//true
        System.out.println("@@@@@".matches(regex4));//faLse
        System.out.println("da??/".matches(regex4));//false
        System.out.println("dadad_".matches(regex4));//true

        System.out.println("-------------------------------------------------------------------------");

        String regex5="((?i)\\w){1,9}";
        System.out.println("adadaD#".matches(regex5));//false


    }

}
```



### 流操作

```java
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        //filter 过滤操作
        //limit  获取前几个元素
        //skip   跳过前几个元素
        //ps: 1.中间方法，返回新的Stream流，原来的Stream流只能使用一次，建议使用链式编程
        //    2.修改Stream流中的数据，不会影响原来集合或者数组中的数据
        ArrayList<String> al1=new ArrayList<>();
        Collections.addAll(al1,"张三","李四","王五","赵六","张无忌","张三丰");
        ArrayList<String> al2=new ArrayList<>();
        Collections.addAll(al2,"赵子龙","黄忠","吕布","张飞");
        //filter过滤元素满足的留下，不满足的去除
        //创建s变量，对其进行筛选，对不满足要求的进行去除（使用lambda表达式）
        al1.stream().filter(s -> s.startsWith("张")).filter(s -> s.length()==3).forEach(System.out::println);
        System.out.println("------------------------------------------------------------------------------------------------------");
        //换行
        System.out.println("------------------------------------------------------------------------------------------------------");
        //skip方法的参数：n(其中n为想要跳过流中的数量)
        //跳过前两个
        al1.stream().skip(2).forEach(s -> System.out.println(s));
        //limit方法的参数：n(n代表前几个元素)
        //
        al1.stream().limit(3).forEach(System.out::println);
        //distinct方法：
        //元素去重，其依赖hashcode equals方法
        al1.stream().distinct().forEach(s -> System.out.println(s));
        //concat方法：
        //合并两个流为一个流
        //尽可能保持a，b两个流的数据类型保持相同，两个流合并为c，那么c为其父类
        //零散数据（必须保证零散数据的类型是相同的）
        Stream.of(1,2,3,4).forEach(System.out::println);
        Stream.of("a","b","c").forEach(System.out::println);
        System.out.println("------------------------------------------------------------------------------------------------------");
        Stream.concat(al1.stream(),al2.stream()).forEach(s -> System.out.println(s));
        System.out.println("------------------------------------------------------------------------------------------------------");
        //map转换流中的数据类型
        ArrayList<String> al3=new ArrayList<>();
        Collections.addAll(al3,"zhangsan-18","lisi-19","wangwu-20");//String->int parseint转换为整形
        al3.stream().map(s -> Integer.parseInt(s.split("-")[1])).forEach(s-> System.out.println(s));
        System.out.println("-------------------------------------");
        //stream终结方法
        //forEach
        al1.stream().forEach(s -> System.out.println(s));
        //count
        long count = al1.stream().count();
        System.out.println(count);
        //toArray
        //收集流中的数据放到数组中
        //先创建一个指定类型的数组，toArray的底层，会依次得到流里面的每一个数据，并把数据放到数组中，方法的返回值是一个装着流里面所有数据的数组
        Object[] objects = al1.stream().toArray();
        System.out.println(objects);
        System.out.println("-----------------------------");
        //collect 收集流中的数据放在集合中
        ArrayList<String> al4=new ArrayList<>();
        Collections.addAll(al4,"aa-man-17","bb-man-15","cc-woman-14","dd-man-20","ee-man-21","ff-woman-9");
        //tolist
        List<String> collect = al4.stream().filter(s -> "man".equals(s.split("-")[1])).collect(Collectors.toList());
        System.out.println(collect);
        //toset
        //对于list与set，在面对set时底层会自动去重（list与set的区别）
        al4.stream().filter(s -> "man".equals(s.split("-")[1])).collect(Collectors.toSet());
        System.out.println("---------------------------------------------------------------------");
        //tomap（明确指定键值对的对应）
        //在tomap方法中明确指定键值对的对应方法
        //参数1：Function泛型1：表示流中的每一个数据的类型  泛型2：表示Map集合中的键的数据类型
        //方法apply形参：以此表示流里面的每一个数据返回值：已经生成的键
        //参数2：Function 泛型1 表示流里面的每一个数据的类型  泛型2：Map集合中的值的数据类型
        //apply形参：依次表示流里面的每一个数据，方法体：生成值的代码 返回值：已经生成的值123567
        Map<String, String> collect1 = al4.stream().filter(s -> "man".equals(s.split("-")[1])).collect(Collectors.toMap(s -> s.split("-")[0], s -> s.split("-")[2]));
        System.out.println(collect1);
        System.out.println("----------------------------------------------------------------");
        String s1="welcome-China-Beijing";
        System.out.println(s1.split("-")[0]);//welcome
        System.out.println(s1.split("-")[1]);//China
        System.out.println(s1.split("-")[2]);//Beijing
        System.out.println("-----------------------------------------------------------------");

    }
}
```

### Scanner

```java
import java.util.Scanner;

public class MyScanner {
    public static void main(String[] args) {
        Scanner sc1 =new Scanner(System.in);
        while (sc1.hasNext()){
            String line = sc1.nextLine();
            System.out.println(line);
        }
    }
    //循环读取打印到标准输出流
    //nextLine读取用户的一行数据
    //next读取下一个标记，默认空格作为分隔符

}
```

### Math类与Biginteger

#### Math类

Math类是Java中的一个标准类，提供了许多数学计算相关的静态方法，例如求绝对值、幂次方、三角函数、对数函数、随机数等等。以下是Math类常用的一些方法：

1. abs(x)

该方法返回参数x的绝对值，例如：

```java
TXT复制int x = -10;
int absX = Math.abs(x);
System.out.println(absX); // 输出：10
```

1. pow(x, y)

该方法返回x的y次幂，例如：

```java
TXT复制double x = 2.0;
double y = 3.0;
double powXY = Math.pow(x, y);
System.out.println(powXY); // 输出：8.0
```

1. sqrt(x)

该方法返回x的平方根，例如：

```java
TXT复制double x = 16.0;
double sqrtX = Math.sqrt(x);
System.out.println(sqrtX); // 输出：4.0
```

1. random()

该方法返回一个[0,1)之间的随机浮点数，例如：

```java
TXT复制double randomNum = Math.random();
System.out.println(randomNum); // 输出：0.398734867473452
```

1. round(x)

该方法返回参数x的四舍五入值，例如：

```java
TXT复制double x = 3.49;
int roundX = Math.round(x);
System.out.println(roundX); // 输出：3
```

1. sin(x)、cos(x)、tan(x)

这三个方法分别返回参数x的正弦、余弦和正切值（单位是弧度），例如：

```java
TXT复制double x = Math.PI / 6;
double sinX = Math.sin(x);
double cosX = Math.cos(x);
double tanX = Math.tan(x);
System.out.println(sinX + " " + cosX + " " + tanX); // 输出：0.5 0.8660254037844386 0.5773
```

#### Biginteger

1. BigInteger(String val)

该构造方法用于创建一个BigInteger对象，其值与参数val相等，例如：

```java
TXT
复制BigInteger bigInt = new BigInteger("12345678901234567890");
```

上述代码会创建一个BigInteger对象，其值为12345678901234567890。

1. add(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象与参数val相加的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("123456789");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.add(b);
System.out.println(c); // 输出：1111111110
```

1. subtract(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象减去参数val的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("987654321");
BigInteger b = new BigInteger("123456789");
BigInteger c = a.subtract(b);
System.out.println(c); // 输出：864197532
```

1. multiply(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象乘以参数val的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("123456789");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.multiply(b);
System.out.println(c); // 输出：1219326311376555329
```

1. divide(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象除以参数val的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("1219326311376555329");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.divide(b);
System.out.println(c); // 输出：123456789
```

1. mod(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象除以参数val的余数，例如：

```java
TXT复制BigInteger a = new BigInteger("1219326311376555329");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.mod(b);
System.out.println(c); // 输出：864197532
```

### Swing与awt

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Main {
    public static void main(String[] args) {
        //JFrame对象
        JFrame jFrame1 =new JFrame("hello world");
        //设置JFrame的大小
        //setSize设置窗口大小
        //setLocation设置窗口
        //setBounds设置窗口的初始位置，窗口高度
        //setVisible设置窗口是否可见
        //setResizable设置窗口是否可调整大小，默认可调整
        //dispose撤销当前窗口，释放资源
        //JFrame的关闭方式
        //setDefaultCloseOperation：DO_NOTHING_ON_CLOSE,HIDE_ON_CLOSE,DISPOSE_ON_CLOSE(隐藏窗口，释放窗口占用资源),EXIT_ON_CLOSE

        jFrame1.setBounds(200,200,400,400);
        jFrame1.setVisible(true);
        jFrame1.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);


        //JDialog
        JDialog jDialog =new JDialog(jFrame1,"I Love U");
        jDialog.setBounds(100,100,100,100);
        jDialog.setVisible(true);
        jDialog.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);

        //常用的面板
        //JPanel
        JFrame jFrame2 =new JFrame("test2");
        jFrame2.setBounds(500,500,100,100);
        jFrame2.setVisible(true);
        jFrame2.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        JPanel jPanel =new JPanel();
        JButton jb1=new JButton("open");
        JButton jb2=new JButton("close");
        JButton jb3=new JButton("apple");
        JButton jb4=new JButton("banana");
//        jPanel.setBounds(300,300,200,200);
        jPanel.add(jb1);
        jPanel.add(jb2);
        jPanel.add(jb3);
        jPanel.add(jb4);
        jPanel.setVisible(true);
//        jFrame.add(jPanel);
//        jPanel.setVisible(true);
//        jFrame.add(jPanel);
        //JScrollPane
        JScrollPane jScrollPane =new JScrollPane(jPanel);
        jScrollPane.setVisible(true);
        jFrame2.add(jScrollPane);

        //常用的组件
        //JLabel
        //构造方法方法，设置图标，水平对齐方式，设置文本
        JFrame jFrame3 =new JFrame("003");
        jFrame3.setBounds(250,250,50,50);
        jFrame3.setVisible(true);
        JLabel jLabel=new JLabel("test");
        jLabel.setVisible(true);
        jFrame3.add(jLabel);
        jFrame3.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        //JButton
        //按钮
        //setEnable设置按钮是否可用
        //setBorderPainted设置边界是否可用

        //单选按钮组件
        //JRadioButton，ButtonGroup
        //单选按钮需要被加入到按钮组中
        JFrame jFrame4 =new JFrame("005");
        jFrame4.setBounds(400,400,50,50);

        ButtonGroup buttonGroup =new ButtonGroup();
        jFrame4.setLayout(new FlowLayout());
        JRadioButton jRadioButton1 =new JRadioButton("test001");
        JRadioButton jRadioButton2 =new JRadioButton("test004");
        buttonGroup.add(jRadioButton1);
        buttonGroup.add(jRadioButton2);
        jFrame4.add(jRadioButton1);
        jFrame4.add(jRadioButton2);

        jFrame4.setVisible(true);
        jFrame4.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);


        //下拉列表框组件
        //JComboBox
        //JComboBox(ComboBox dataModel) 使用list model创建一个下拉列表
        //方法addItem() 添加下拉内容

        JFrame jFrame5 =new JFrame("006");
        jFrame5.setBounds(50,50,200,200);
        jFrame5.setLayout(new FlowLayout());
        jFrame5.setVisible(true);
        jFrame5.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        JComboBox box =new JComboBox<>();
        box.addItem("hello world");
        box.addItem("I LOVE U");
        jFrame5.add(box);

        //菜单栏
        //一级菜单栏
        //二级菜单栏
        //创建菜单条JMenuBar  创建菜单 JMenu  创建菜单项 JMenuItem
        JFrame jFrame6 =new JFrame("menu test");
        jFrame6.setBounds(600,600,200,200);
        jFrame6.setLayout(new FlowLayout());
        jFrame6.setVisible(true);
        jFrame6.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        JMenuBar jMenuBar =new JMenuBar();
        JMenu jMenu =new JMenu("main menu !");
        JMenuItem jMenuItem1 =new JMenuItem("001");
        JMenuItem jMenuItem2 =new JMenuItem("002");
        JMenuItem jMenuItem3 =new JMenuItem("003");
        jMenuBar.add(jMenu);
        jMenu.add(jMenuItem1);
        jMenu.add(jMenuItem2);
        jMenu.add(jMenuItem3);
        jFrame6.add(jMenuBar);

        /*
        文本组件
        JTextField是单行文本框 JTextArea是多行文本框,可以使用转义字符进行操作
                JTextField和JTextArea都是Swing中的文本框组件，用于在GUI中显示和编辑文本内容。
                它们的区别如下：

                大小和样式：JTextField是一个单行文本框，只能显示一行文本；
                而JTextArea是一个多行文本框，可以显示多行文本。JTextField通常比较小，适合用于输入简短的文本；而JTextArea通常比较大，适合用于输入较长的文本。

                输入方式：JTextField只能输入单行文本，不能换行；
                而JTextArea可以输入多行文本，并支持换行。

                布局方式：JTextField默认使用FlowLayout布局，可以方便地对齐其他组件；
                而JTextArea默认使用BorderLayout布局，需要放在JScrollPane中才能正确显示滚动条。

                方法和属性：JTextArea相比JTextField拥有更多的方法和属性，
                例如设置行数、列数、自动换行、滚动条等等。
        */


        JFrame jFrame7 =new JFrame("text area!");
        jFrame7.setLayout(new FlowLayout());
        jFrame7.setBounds(0,400,200,200);
        JTextField jTextField1 =new JTextField("hell world  I LOVE U");
        JTextArea jTextArea1 =new JTextArea("hello asdasdasassda\nsdasiorhwfhfbcudd",2,5);
        jFrame7.add(jTextField1);
        jFrame7.add(jTextArea1);
        jFrame7.setVisible(true);
        jFrame7.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        //密码框组件
        JPasswordField jPasswordField1=new JPasswordField("psw");
        jPasswordField1.setColumns(10);//设置宽度
        jFrame7.add(jPasswordField1);


        /*
        事件监听
        基于接口的监听器
            基于接口的监听器是指实现了特定接口的类，用于响应特定的事件。
            例如，ActionListener接口用于响应按钮的点击事件，MouseListener接口用于响应鼠标的点击事件。
        基于适配器的监听器
            基于适配器的监听器是指继承了特定适配器类的类，用于响应特定的事件。适配器类是一个抽象类，实现了特定接口的所有方法，但是方法体为空。
            例如MouseAdapter类是MouseListener接口的适配器类，它实现了MouseListener接口的所有方
        */
        JFrame jFrame8 =new JFrame("action listener!");
        jFrame8.setBounds(800,400,300,300);
        jFrame8.setLayout(new FlowLayout());
        JButton jButton3 =new JButton("click me 001");
        JButton jButton4 =new JButton("click me 002");
        jButton3.addActionListener(new MyActionListener());
        jButton4.addMouseListener(new MyMouseListener());
        jFrame8.add(jButton3);
        jFrame8.add(jButton4);
        jFrame8.setVisible(true);
        jFrame8.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);


        //test
        JFrame jFrame9 =new JFrame("testing!");
        jFrame9.setBounds(400,400,300,300);
        JPanel jPanel1=new JPanel(new FlowLayout());
        jPanel1.setVisible(true);
        JPasswordField jPasswordField =new JPasswordField(5);
        jPasswordField.setVisible(true);

        JButton jButton5 =new JButton("click me and get password!");
        jButton5.addActionListener(e -> {
            char [] password=jPasswordField.getPassword();
            JOptionPane.showMessageDialog(null,new String(password));
        });
        jPanel1.add(jPasswordField);
        jPanel1.add(jButton5);
        jFrame9.add(jPanel1);
        jFrame9.setVisible(true);
        jFrame9.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
    }
}




////////////////////////



import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class MyMouseListener extends MouseAdapter {
    @Override
    public void mouseClicked(MouseEvent e) {
        System.out.println("click me!!!");
    }
}


//////////////////////////



import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MyActionListener implements ActionListener {
    @Override
    public void actionPerformed(ActionEvent e) {
        //按钮点击触发事件
        System.out.println("hello world!");
    }
}

```



#### 利用流对集合数据进行流水线处理

```java
import java.lang.reflect.Array;
import java.util.*;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        //Stream的使用方法
        //单列集合        default Stream<E> stream()                            Collection中的默认方法
        //双列集合        无                                                   无法直接使用Stream流
        //数组           public static <T> Stream<T> stream(T[] array)        Arrays工具类中的静态方法
        //一堆零散数据     public static<T> Stream<T> of (T...values)           Stream接口中的静态方法
        //单列集合
        ArrayList<String> l1=new ArrayList<>();
        l1.add("张三");
        l1.add("李四");
        l1.add("王五");
        l1.add("赵六");
        l1.stream().forEach(s -> System.out.println(s));
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //双列集合
        HashMap<Integer,String>hm1=new HashMap<>();
        //方法1：创建单列集合进行添加
        //Collections.addAll(m1,1,"a1",2,"b2",3,"c3");
        hm1.put(1,"a1");
        hm1.put(2,"b2");
        hm1.put(3,"c3");
        hm1.put(4,"d4");
        ArrayList<Integer>al1=new ArrayList<>();
        ArrayList<String>al2=new ArrayList<>();
        hm1.forEach((integer, s) -> {
            al1.add(integer);
            al2.add(s);
        });
        al1.stream().forEach(System.out::println);
        al2.stream().forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //方法2:直接利用keyset方法和values方法进行键，值的单列集合的获取
        hm1.keySet().stream().forEach(System.out::println);
        hm1.values().stream().forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //方法3：使用entryset方法进行键值对对象的获取，再利用流进行操作
        hm1.entrySet().stream().forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //数组
        int [] arr1 ={1,2,3,4,5,6,5,43,21};
        Arrays.stream(arr1).forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");

    }
}
```

#### 流操作实例

```java
import java.lang.reflect.Array;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        //定义一个集合，并添加一些参数 1，2，3，4，5，6，7,8,9
        //过滤奇数
        ArrayList<Integer> al1=new ArrayList<>();
        Collections.addAll(al1,1,2,3,4,5,6,7,8,9);
        al1.stream().filter(s-> s%2==0).forEach(s-> System.out.println(s));
        System.out.println("--------------------------------------------------");
        //添加数据进入集合中，对每个数据的年龄进行判断，排除年龄小于等于24的并将数据添加到map集合中
        ArrayList<String>al2 =new ArrayList<>();
        Collections.addAll(al2,"zhangsan,23","lisi,24","wangwu,25");
        //在此处的字符串的判断中需要对字符串进行类型转换，利用Integer下的parseInt方法进行转换后对整形进行判断
        Map<String, String> m1 = al2.stream().filter(s -> Integer.parseInt(s.split(",")[1]) > 24).collect(Collectors.toMap(s -> s.split(",")[0], s -> s.split(",")[1]));
        m1.forEach((s, n)-> System.out.println(s+":"+n));
        System.out.println("-------------------------------------------------------");
        //创建两个集合，分别为男演员，女演员的集合
        //要求：男演员只需要名字为3个字的前两个人，女演员只要姓杨的，并且不要第一个，将过滤后的两个集合进行合并，同时将其变为Actor对象，将所有的对象添加到list集合中
        //Ps：演员类Actor，属性有name，age
        ArrayList<String> actor=new ArrayList<>();
        ArrayList<String> actress=new ArrayList<>();
        Collections.addAll(actor,"李华，18","白岩松，33","杨开山，25","张维为，40","赵匡胤，18","杨梅梅，19");
        Collections.addAll(actress,"李里，18","白江波，33","杨十五，25","杨十六，40","赵事实，18","杨萃萃，16");
        //System.out.println(actor);
        //actor.stream().filter(s->s.startsWith("杨")&&s.split(",")).forEach(s -> System.out.println(s));
        Stream<String> sm1 = actor.stream().filter(s -> s.split("，")[0].length() == 3).limit(2);
        Stream<String> sm2 = actress.stream().filter(s -> s.split("，")[0].startsWith("杨")).skip(1);//分别对两个流进行分别筛选打印
        List<Actor>l1=Stream.concat(sm1,sm2).map(s -> new Actor(Integer.parseInt(s.split("，")[1]),s.split("，")[0])).collect(Collectors.toList());
        //此处流的合并需要创建一个流的对象，方便后续的操作，在创建list的对象添加Actor的泛型，利用map进行匹配，
        System.out.println(l1);
//        sm3.forEach(s -> new Actor((Integer.parseInt(s.split("，")[0])),s.split("，")[1]));
//        System.out.println(sm3.collect(Collectors.toList()));
        System.out.println("-------------------------------------------------------");


    }
    static class Actor{
        private int age;
        private String name;

        public Actor() {
        }

        public Actor(int age, String name) {
            this.age = age;
            this.name = name;
        }

        /**
         * 获取
         * @return age
         */
        public int getAge() {
            return age;
        }

        /**
         * 设置
         * @param age
         */
        public void setAge(int age) {
            this.age = age;
        }

        /**
         * 获取
         * @return name
         */
        public String getName() {
            return name;
        }

        /**
         * 设置
         * @param name
         */
        public void setName(String name) {
            this.name = name;
        }

        public String toString() {
            return "Actor{age = " + age + ", name = " + name + "}";
        }
    }
}
```



### 方法引用

```java
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        Integer[] ite1={5,2,39,34,45,46,77,68,39};
        //匿名内部类
        Arrays.sort(ite1, new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o1-o2;
            }
        });
        //lambda表达式
        Arrays.sort(ite1,(Integer o1,Integer o2) ->{return (o1-o2);});
        //lambda简化表达式
        Arrays.sort(ite1,((o1, o2) -> o1-o2));
        //方法引用
        //Ps:方法引用处需要函数时接口，被引用的方法需要已经存在，被引用的形参和返回值需要与需要的形参由于返回值相同，满足当前的要求
        Arrays.sort(ite1,Main::Func);
        //此处静态的方法需要用类名对函数进行调用
        //::方法引用符

        //方法引用的分类
        //引用静态方法
        ArrayList<String>al1=new ArrayList<>();
        Collections.addAll(al1,"1","111111","11111","111","11","2");
        al1.stream().map(Integer::parseInt).forEach(s-> System.out.println(s));
        System.out.println("---------------------------------------------");
        //Integer::parseInt
        //引用成员方法
        //静态的方法中无法使用this关键字，需要使用时稚只能创建其对象进行操作，例如本类想要使用this只能创建本类的对象对其进行引用
        //对象::方法  1.其他  类名::方法名  2.本类this::方法名   3.父类super::方法名
        //关于本类与父类的方法需要注意:无法引用静态的方法，静态方法中无super与this关键字
        ArrayList<String>al2 = new ArrayList<>();
        Collections.addAll(al2,"张三","王五","李四","赵是三","张二三","张一三");
        al2.stream().filter(s -> s.length()==3).filter(s->s.startsWith("张")).forEach(s -> System.out.println(s));
        //al2.stream().filter(this::StringJudge)  此处为上述的实例
        al2.stream().filter(new Main()::StringJudge).forEach(s -> System.out.println(s));
        System.out.println("-----------------------------------");
        //引用构造方法(目的是为了创建对象)
        //格式：  类名::new
        ArrayList<String> al3=new ArrayList<>();
        al3.add("张无忌，15");
        //⬇此处详见类中注释
        List<Student> list1_stu = al3.stream().map(Student::new).collect(Collectors.toList());
        System.out.println(list1_stu);
        System.out.println("----------------------------------------------------------");
        //其他调用方法
        //使用类名引用构造方法，引用数组的构造方法
        //格式:  类名::成员方法   eg：String::subString
        //此方法的弊端在于，不能引用所有的方法，在只有一个参数时，能引用的方法仅仅是其类型的类，例如当参数为String 类下的参数时，只能引用在String类下的方法
        //第一个参数与引用的方法类型相同，第二个到最后一个需要保证原参数与引用方法的类型相同，
        ArrayList<String> al4=new ArrayList<>();
        Collections.addAll(al4,"aaa","bbb","ddd","ccc");
        al4.stream().map(String::toUpperCase).forEach(s -> System.out.println(s));
        //此处调用String类下的uppercas方法进行大小写转换

        System.out.println("-----------------------------------------------------------");
        //引用数组的构造方法
        //数组类型[]::new
        ArrayList<Integer> at1=new ArrayList<>();
        Collections.addAll(at1,1,2,3,4,5,6,7,8,9);
        //数组的类型与流中的数据类型保持一致
        Integer[] it1=at1.stream().toArray(Integer[]::new);
        //Arrays下的toString方法，保证其能合理输出
        System.out.println(Arrays.toString(it1));;

        //方法引用要点：1，被引用的方法需要有函数式接口，   2，被引用的方法必须已经存在，   3，被引用方法的形参必须和抽象方法的形参保持一致  4，满足需求
        ArrayList<String> al5=new ArrayList<>();
        Collections.addAll(al5,"张三，11","李四，12","王五，13");
        Student[] stu1 = al5.stream().map(Student::new).toArray(Student[]::new);
        System.out.println(Arrays.toString(stu1));

        System.out.println("-----------------------------------------------------------------");
        ArrayList<Student> astu1=new ArrayList<>();
        astu1.add(new Student(10,"张三"));
        astu1.add(new Student(11,"李四"));
        astu1.add(new Student(12,"王五"));
        String[] str2 = astu1.stream().map(new Function<Student, String>() {
            @Override
            public String apply(Student student) {
                return student.getName();
            }
        }).toArray(String[]::new);
        System.out.println(Arrays.toString(str2));
        System.out.println("------------------------------------------------");
        String[] str3 = astu1.stream().map(Student::getName).toArray(String[]::new);
        System.out.println(Arrays.toString(str3));
        System.out.println("------------------------------------------------");

        String[] str4 = astu1.stream().map(Student::toinformation).toArray(String[]::new);
        System.out.println(Arrays.toString(str4));


    }
    public static int Func(int o1, int o2)
    {
        return o1-o2;
    }
    public  boolean StringJudge(String s)
    {
        return s.startsWith("张")&&s.length()==3;
    }

}




//学生类
public class Student {
    private int age;
    private String name;

    public Student() {
    }

    public Student(int age, String name) {
        this.age = age;
        this.name = name;
    }
    public Student(String str)
    {
        String [] arr_str=str.split("，");
        age=Integer.parseInt(arr_str[1]);
        name=arr_str[0];
    }
    //由于对象的构造方法在创建时就已经返回了对象，所以上述的构造方法不会有返回值，
    //由于方法的引用需要参数与返回值的相同，所以在此处重载新的构造函数同时保证只有一种需要的参数即(String)
    //上述方法利用临时的字符串数组对参数进行截取，split如果无后续指定，默认将截取的剩下的存入字符串数组中

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    public String toString() {
        return "Student{age = " + age + ", name = " + name + "}";
    }
    public String toinformation(){
        return (this.getName()+"-"+this.age);
    }
}
	

```

### 可变参数

```java
public class Main {
    public static void main(String[] args) {
        //可变参数：方法的形参数可以变化（从jdk5进行改进）
        //格式：属性类型...名字（例如int...args）
        //注意：方法的形参只能使用一个可变参数，当大于一个时会报错
        int sum=getSum(1,2,3,4,5,6,7,8,9,10);
        System.out.println(sum);

    }
    public static int getSum(int...args){
        int sum=0;
        for(int i:args){
            sum+=i;
        }
        return sum;
    }
}
```

### IO流

#### 文件File常用方法

```java
import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.sql.Array;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;

public class Main {
    public static void main(String[] args) throws IOException {
        //文件file的使用
        //路径：相对路径与绝对路径
        //1.根据文件路径创建对象
        String all="C:\\Users\\83899\\Desktop\\File_test.txt";//此处使用绝对路径
        File f1=new File(all);
        System.out.println(f1);
        //2.根据父路径与子路径   子路径：eg:a.txt
        String parent="C:\\Users\\83899\\Desktop";
        String children="File_test.txt";
        File f2=new File(parent,children);//此时在底层会根据操作系统使用不同的分隔符
        File f3=new File(parent+"\\"+children);

        File f4=new File(parent);
        File f5=new File(f4,children);//此处表示利用上一个file对象的路径作为父路径，第二个参数是子路径


        System.out.println("------------------------------1---------------------------------");
        //file判断和获取方法
        //isDriectory()      isFile()     exists()   length()     getAbsolutPath()       getpath()     getName()
        //length方法：只能获取文件的大小，如果获取的是文件夹，那么会导致其获取的数据显示为0   （单位是字节）

        File f8=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\src\\text.txt");//此处路径下为文件
        File f9=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\src\\test");//此处为文件的绝对路径
        System.out.println(f8.length());//39字节
        System.out.println(f9.length());//0

        //需要获取文件夹的大小需要累加各种文件的大小
        System.out.println("-----------------------------2------------------------------");
        //对文件夹进行判断
        File f6=new File(parent);//此处为文件夹
        System.out.println(f6.isDirectory());//判断是否为文件夹
        //对文件路径判断
        File f7=new File(all);
        System.out.println(f7.isFile());//判断是否为文件
        //判断文件路径是否存在
        System.out.println(f7.exists());
        System.out.println("-------------------------------3----------------------------");
        //获取文件绝对路径
        System.out.println(f7.getAbsolutePath());
        //获取文件相对路径
        System.out.println(f7.getPath());
        //返回文件的大小
        System.out.println(f7.length());
        //获取文件名字的大小
        System.out.println(f7.getName());//调用者为文件时会返回文件的名字+后缀，如果是文件夹会指返回文件夹的名称
        System.out.println("-------------------------------4--------------------------");
        //获取文件的上一次的更改时间（利用时间日期类SimpleDateFormat）
        File f10=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\src\\text.txt");
        long l1 = f10.lastModified();
        System.out.println(l1);//1677755995279   此处为毫秒
        Date dt1=new Date(l1);
        SimpleDateFormat sp1=new SimpleDateFormat("yyyy-mm-dd-HH-MM-SS");
        System.out.println(sp1.format(dt1));
        System.out.println("--------------------------------5------------------------");
        //文件的删除 创建
        //创建一个新的空的文件
        File f11=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\a1.txt");
        boolean b1 = f11.createNewFile();//此方法会出现两个选择，catch或者是抛出
        System.out.println(b1);
        //Ps：1.如果当前路径没有该文件，那么会创建这个文件，同时返回true，反之返回false，
        // 2.如果该路径的父级路径是不存在的，会出现IOException的异常
        // 3.利用createNewfile方法创建的一定是文件，如果没有指定后缀，他会直接创建一个没有后缀的文件
        System.out.println("----------------------------------6-------------------------------------");
        //创建单极文件夹（目录）
        File f12=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\b");
        boolean b2 = f12.mkdir();//mkdir方法make Directory
        System.out.println(b2);
        //创建多级文件夹（目录）
        File f13=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\c\\b\\a");
        boolean b3 = f13.mkdirs();
        System.out.println(b3);//创建多级文件夹也能创建单级文件夹，使用时可以使用多级文件夹，但是其底层是利用了mkdir()
        System.out.println("-----------------------------------7-------------------------");
        //删除文件夹
        File f14=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\text.txt");
        boolean b4 = f14.delete();
        System.out.println(b4);//PS:1.如果删除的是文件或者空的文件夹，直接删除不走回收站  2。如果删除的是非空的文件夹，会删除失败
        //获取并遍历
        File f15=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File");
        File[] ff1 = f15.listFiles();//该方法获取该路径下的所有文件内容
        for (File file : ff1) {
            System.out.println(file);
            //其中的file依次表示文件之中的各种文件夹和文件
        }//当调用者表示的路径是文件或不存在会返回null    当调用者的路径是空文件夹会返回长度为0的file数组   当调用者的路径是需要权限才能访问的文件是会返回null   除此之外都可以将文件夹中的文件依次返回（包括隐藏文件）


        //**************************************************************************//
        //lisiRoots()  获取系统所有盘符             list() 获取该路径下的所有文件名   list(文件名过滤器)    listFiles()
        File f16=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File");
        String s1 = ".txt";
        File[] ff2 = f16.listFiles(new FileFilter() {
            @Override
            public boolean accept(File pathname) {
                return pathname.isFile() && pathname.getName().endsWith(".txt");
            }
        });
        System.out.println(Arrays.toString(ff2));
        //同时与创建对象时相同会有相似之处，在pathname 和子路径，父路径匹配的相似



    }
}
```

#### 文件File对象训练

```java
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        File f1=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\File_test\\a.txt");
        File f2=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\File_test\\a");
        File f3=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\File_test");
        boolean b1 = f1.createNewFile();//创建文件
        boolean b2 = f2.mkdirs();//创建文件夹
        System.out.println(b1);
        System.out.println("------------------1-------------");
        boolean b3 = Search_avi(f1);
        System.out.println(b3);//整体思路对文件的每个文件进行遍历（不考虑子文件夹）
        boolean b4 = Search_Avi(f3);
        System.out.println(b4);//对该路径下的所有文件夹进行遍历，包括(子级目录下的)
        System.out.println("------------------2-------------");
        File f4=new File("D:\\DY3rn2jPq2_d5");
        delete(f4);//删除一个多级文件夹
        System.out.println("------------------3-------------");
        long getlen = Getlen(f4);//获取文件的总大小
        System.out.println("------------------4-------------");
        HashMap<String, Integer> getcount = getcount(f4);//统计相关后缀的文件夹数量
        System.out.println(getcount);
        System.out.println("------------------5-------------");
    }

    public static void Search_avi(){
        File[] files = File.listRoots();
        for (File file : files) {
            Search_avi(file);
        }
    }
    public static boolean Search_avi(File pathname){
        File[] ff1 = pathname.listFiles();
        for (File ff2 : ff1) {
            if(ff2.isFile()&&ff2.getName().endsWith(".avi")){
                return true;
            }
        }
        return false;
    }
    public static boolean Search_Avi(File pathname){
        File[] ff1 = pathname.listFiles();
        for (File ff2 : ff1) {
            if(ff2.isFile()){
                if (ff2.getName().endsWith(".avi")) {
                    System.out.println(ff2);
                }
            }else {
                Search_Avi(ff2);
                //此处直接递归，当调用者为文件夹时，直接对子级文件夹进行遍历，重复此过程
            }

        }
        return false;

    }
    public static void delete(File pathname){
        File[] files = pathname.listFiles();//进入文件
        for (File file : files) {//文件遍历
            if(file.isFile()){//判断是否为文件
                delete(file);//删除文件
            }else {
                delete(file);//若为文件夹，递归后删除文件夹
            }
        }
        pathname.delete();//删除自己
    }
    public static long Getlen(File pathname){
        File[] files = pathname.listFiles();
        long length=0;
        for (File file : files) {
            if(file.isFile()){
                 length = file.length()+ length;
            }else {
                 length = Getlen(file)+length;
            }
        }
        return length;
    }
    public static HashMap<String,Integer> getcount(File pathname){
        HashMap<String,Integer> hm1=new HashMap<>();//创建新Map集合
        File[] files = pathname.listFiles();//文件数组
        for (File file : files) {
            if(file.isFile()){//如果是文件
                String name = file.getName();
                String[] split = name.split("\\.");//对文件名进行分割处理
                if(split.length>=2){//当文件名为xxx.xxx或者xxx.xx.xxx
                    String Name=split[split.length-1];//获取最后一位
                    if(hm1.containsKey(Name)){//如果Map集合中已经存在
                        hm1.put(Name,hm1.get(Name)+1);////直接对其进行加1
                    }else {
                        hm1.put(Name,1);//如果不存在创建一个键值对且值初始化为1
                    }
                }
            }else {//如果不是文件
                HashMap<String, Integer> SonMap = getcount(file);//子文件集合
                for (Map.Entry<String, Integer> stringIntegerEntry : SonMap.entrySet()) {//增强for对集合进行遍历
                    String key= stringIntegerEntry.getKey();//获取键
                    int value= stringIntegerEntry.getValue();//获取值
                    if(hm1.containsKey(key)){
                        hm1.put(key,value+hm1.get(key));
                    }else{
                        hm1.put(key,value);
                    }
                }
            }
        }
        return hm1;//返回主集合
    }
}

```



#### 文件复制拷贝

```java
public static void File_copy(File pathname01,File pathname02) throws IOException {//文件拷贝方法（包含子级文件夹）
        pathname02.mkdirs();//在该路径创建一个文件夹（前提是该路径无文件夹）
        File[] files = pathname01.listFiles();
        for (File file : files) {//对文件数组进行遍历
            if(file.isFile()){//是文件
                int len = 0;
                byte []bytes1=new byte[20];
                FileInputStream fi1=new FileInputStream(file);
                FileOutputStream fo1=new FileOutputStream(new File(pathname02,file.getName()));
                while((len=fi1.read(bytes1))!=-1){//读入数组
                    fo1.write(bytes1,0,len);//按照数组依次写入
                }
                fo1.close();
                fi1.close();
            }else {//是文件夹
                File_copy(file,new File(pathname02,file.getName()));//递归时，父级路径使用pathname02，子级路径用new File 创建对象以及 getNname方法去创建同名文件夹
            }
        }
    }
```

#### 文件加密

```java
public static boolean File_lock(File pathname01,File pathname02) throws IOException {
        if(pathname01.isFile()){
            FileInputStream fi1=new FileInputStream(pathname01);
            FileOutputStream fo1=new FileOutputStream(pathname02);
            int len=0;
            byte[]bytes1=new byte[20];
            while((len=fi1.read())!=-1);{
                fo1.write(len^2);
            }
            fo1.close();
            fi1.close();
            return true;
        }else {
            return false;
        }
    }
```

#### 序列化流

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        File f1=new File("101.txt");
        //序列化流：用于输出对象的流（生于字节流中），需要关联基本流
        //构造方法
        ObjectOutputStream oos=new ObjectOutputStream(new FileOutputStream(f1));
        Student s1=new Student(18,"Lisa");
        oos.writeObject(s1);//此方法用于写对象
        oos.close();
        //反序列化流
        ObjectInputStream ois1=new ObjectInputStream(new FileInputStream(f1));
        Student o =(Student) ois1.readObject();//利用Stu对象接受反序列化流读取的对象
        System.out.println(o);
        ois1.close();
    }
}

//学生类
import java.io.Serial;
import java.io.Serializable;

public class Student implements Serializable {
    @Serial
    private static final long serialVersionUID=20230313L;//版本号的不变性可以让类中所有数据更改后依旧保持序列化的数据版本号不变
    private int age;
    private String name;

    public Student() {
    }

    public Student(int age, String name) {
        this.age = age;
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    public String toString() {
        return "Student{age = " + age + ", name = " + name + "}";
    }
}
```

#### 多对象写入文件

```java
import java.io.*;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        File f1=new File("101.txt");
        File f2=new File("102.txt");
        
        //方法一：直接进行最原始的逐个写入逐个读取，速度较慢，且在读取到末尾时，会出现EOFException(文件末尾异常)

        //方法二直接使用Arraylist

        Student s1=new Student(18,"王梦楠","北京");
        Student s2=new Student(19,"林云龙","西安");
        Student s3=new Student(20,"李小龙","中国");
        ArrayList<Student> als1=new ArrayList<>();
        als1.add(s1);
        als1.add(s2);
        als1.add(s3);//存入Arraylist集合中
        /*
序列化多个对象
        ObjectOutputStream oos1=new ObjectOutputStream(new FileOutputStream(f1));
        oos1.writeObject(als1);
        oos1.close();             将上述集合直接写入
*/

        ObjectInputStream ois1=new ObjectInputStream(new FileInputStream(f1));
        ArrayList<Student>als2= (ArrayList<Student>) ois1.readObject();

        for (Student student : als2) {
            System.out.println(student);
        }
        //Student{age = 18, name = 王梦楠, address = 北京}Student{age = 19, name = 林云龙, address = 西安} Student{age = 20, name = 李小龙, address = 中国}
        ois1.close();//文件的读取末尾会出现EOFException文件末尾异常
    }
}
```

#### 字节打印流

```java
import java.io.*;
import java.nio.charset.Charset;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        //打印流(只写不读)
        //打印流的底层构造会依据你提供的，创建outputStream，他的构造参数有字符集编码类型，指定字符编码，自动刷新，Ps:打印流的底层没有缓冲区，所以自动刷新可有可无
        //write println print printf   都可以保证数据的原样写出
        File f1=new File("101.txt");
        PrintStream ps1=new PrintStream(new FileOutputStream(f1),true, Charset.forName("UTF-8"));
        ps1.println(99);
        ps1.print(true);
        ps1.println();
        ps1.printf("%s 爱上了 %s","阿珍","阿强");
        ps1.close();



    }
}
```

#### 字符打印流

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        File f1=new File("101.txt");
        File f2=new File("102.txt");
        //字符打印流在构造方法上与字节打印流一致
        //字符打印流拥有底层的缓冲区，所以效率比字节打印流要高
        PrintWriter pw1=new PrintWriter(new FileWriter(f1),true);//此处关联基本字符流
        pw1.write(99);
        pw1.println();
        pw1.println("I love YOU"); 
        pw1.print(true);
        pw1.printf("%s你来自何处呢","阿飞");
        pw1.close();
//        System.out.println();
        //上一行代码可以用以下方法代替
        PrintStream out = System.out;//此打印流在虚拟机启动时，由虚拟机创建，默认指向控制台
        out.println();//通过打印流调用方法（合理）
        System.out.println();//直接写法变为如此sout+
        //该打印流是唯一的，不关闭，在被关闭后会导致后续代码无法执行

    }
}
```

#### hutool包IO流操作

```java
import cn.hutool.core.io.FileUtil;
import cn.hutool.core.util.ReUtil;
import cn.hutool.http.HttpUtil;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        //hutool包使用
        //FileUtil类
        File f1=new File("101.txt");
        File f2=new File("102.txt");
        File f3=new File("103.txt");
        File f4=new File("Test_java");
        File f5=new File("Test(02)_java");
        File f6=new File("105.txt");
        File f7=new File("106.txt");


        File f8 = FileUtil.file();//此处查看其中的参数包含可变参数使用
        FileUtil.touch(f2);//touch方法创建一个新的文件夹，如果父级路径不存在，不报错直接创建父级路径，根据参数创建文件
        ArrayList<String>als1=new ArrayList<>();
        als1.add("aaa");
        als1.add("ccc");
        als1.add("bbb");
        FileUtil.writeLines(als1,f2,"UTF-8",true);//四个参数分别表示：集合名，文件写出的路径，字符集名称，是否追加
        FileUtil.appendLines(als1,f2,"UTF-8");
        List<String> str1 = FileUtil.readLines(f2, "UTF-8");//第三个参数是自己创建一个集合然后把数据存在集合中，其中它会把一行数据认为是集合中的一个
        String str2 = HttpUtil.get("https://hanyu.baidu.com/s?wd=%E7%99%BE%E5%AE%B6%E5%A7%93&device=pc&from=home");
        List<String> all = ReUtil.findAll("(.{4})(，|。)",str2, 1);//三个参数：正则表达式，传入的需要筛选的字符串，分组的所选组号
        System.out.println(all);
    }
}
```



### 异常

#### 异常概念

```java
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Main {
    public static void main(String[] args) throws ParseException {
        //Error 系统级别错误
        //Exception   异常，程序出现的问题，异常体系最上层父类为Exception
        // 1.编译时异常，未继承RuntimeException，直接继承于Exception，编译阶段就会错误提示
        //2.运行时异常：RuntimeException本身和子类，编译阶段没有错误提示，运行时出现的

        //编译时期异常
        String time="2023.3.1";
        SimpleDateFormat sdf1=new SimpleDateFormat("yyyy.mm.dd");
        Date date=sdf1.parse(time);
        //此处parse方法需要手动签名，否则报错
        System.out.println(date);


        //运行时期异常
        int[]arr1={1,2,3,4,5};
        System.out.println(arr1[10]);
        //次数数组索引越界但是不会在编译时期报错，在运行时会出现异常

        /*
         Java文件->（过程1）(通过javac命令)字节码文件->（过程2）(通过java命令)运行结果
        过程一：编译时异常     过程二：运行时异常
        编译时java不会运行代码，只会检查语法是否错误，或者优化性能
        编译异常就是为了提醒程序员检查本地信息 运行时期异常就是程序运行的错误
        throw 抛出关键字，在面对数据错误时，可以选择抛出数据错误去提醒操作者去更改数据
        例如：throw RuntimeException
        异常可以用来调试bug，也可以使代码调用者更改代码
        虚拟机异常Jvm：将异常打印在控制台，同时异常后的代码停止执行，
        自己处理异常
         */
        //自己处理异常（捕获异常）
//        try {
//            //可能出现的异常的代码                    //此处出现错误会创建相应错误的对象，下方catch会对异常进行捕获，在异常被捕获后会执行catch下的代码
//        }catch(异常类名 变量名){
//            异常的处理代码
//        }

        //目的时让代码出现异常时可以正常运行下去
        //try中不报错，直接执行try不会执行catch
        //try遇到了多个问题，多个catch进行捕获，如果存在异常的父子类关系，要把父类写在最下面
        //在jdk7拥有的新功能：异常中使用|隔开表示其是同一种解决方案
        //未捕获就会直接报错：很合理
        //try中遇到了问题：下面的代码不会执行，会跳到对应catch的语句中
        //getMessage 方法返回此throwable的详细信息字符串
        //tostring返回此错误的简短描述
        //printstackTrace把异常的错误输出在控制台，其中，printstackTrace是输出错误信息最多的方法，最为常用
        System.err.println(123);//错误的输出语句
        //throw 将异常抛出写在方法内，throws，写在方法定义处，告诉编写者此处需要注释异常




        //自定义异常1。定义异常类  2.写继承关系  3.空参构造  4.带参构造
        //目的是让报错信息更加的见名之意（方便查找问题）


    }
}
```

异常练习

```java
public class Girlfriend {
    private int age;
    private String name;

    public Girlfriend() {
    }

    public Girlfriend(int age, String name) {
        this.age = age;
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        if(age<18||age>40){
            throw new OverboundsException();
        }
        this.age=age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        if(name.length()<3||name.length()>10){
            throw new OverboundsException();
        }
        this.name = name;
    }

    public String toString() {
        return "Girlfriend{age = " + age + ", name = " + name + "}";
    }
}


/////////////////////////////////////





import java.io.Serial;

public class OverboundsException extends RuntimeException{
    @Serial
    private static final long serialVersionUID = 2254863261008994300L;

    //在类名的命名时Exception
    //Exception主要是给维护人员检查用的
    public OverboundsException(){}
    public OverboundsException(String message){
        super(message);
    }
}


/////////////////////////////////////////////


import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Girlfriend gf1=new Girlfriend();
        Scanner sc1=new Scanner(System.in);
        while (true) {
            try{


                String agegf=sc1.nextLine();
                int age_gf = Integer.parseInt(agegf);//此处为第一个错误，NumberformatException错误
                gf1.setAge(age_gf);//此处报错RuntimeException

                String name_gf=sc1.nextLine();
                gf1.setName(name_gf);//此处也有可能会出现RuntimeException错误
                break;//如未捕捉到错误，直接停止循环，代表数据正常
            }catch(NumberFormatException n){
                n.printStackTrace();
            }catch (OverboundsException r){//Runtime Exception是NumberFormatException的父类，写在下面,二次改为OverboundExcrption,此处为自定义异常
                r.printStackTrace();//catch执行完之后无break继续执行
            }
            System.out.println("输入有误，重新输入");
        }

        System.out.println(gf1);
    }
}


/////////////////////////////////////////////
```



### 线程

#### 线程对象创建

```java
//方法1
public class ForThread1 extends Thread{
    @Override
    public void run() {
        while (true) {
            System.out.println(getName()+"开始发车！");
        }
    }
}
//方法2
public class ForThread2 implements Runnable{
    @Override
    public void run() {
        while (true){
            Thread t=Thread.currentThread();//获取当前线程的对象，同时返回给t
            System.out.println(t.getName()+"你好！");
        }
    }
}

//方法3
import java.util.concurrent.Callable;

public class ForThread3 implements Callable<String> {//此处Callable有泛型，表示返回线程结果的类型
    @Override
    public String call() throws Exception {
        return "你好我回来了";
    }
}


//////////////////////////////////


import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

public class Main {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        //线程
        //并发：同一时刻多个指令在单个CPU上同步运行
        //并行：同一时刻多个指令在多个CPU上同时运行
        //三种实现方式：
        //1，继承Threa类
        //特点：编程比较简单，可以直接使用Thread类中的方法，缺点是由于Java中类只能实现单继承，不能继承其他的类所以拓展性较大
        ForThread1 pc1=new ForThread1();
        ForThread1 pc2=new ForThread1();
        pc1.setName("Thread 1");
        pc2.setName("Thread 2");
        pc1.start();
        pc2.start();


        //2，实现Runnable接口
        //特点：拓展性强，实现该接口的同时还可以继承其他的类，编程相对于复杂，不能直接使用Thread类中的方法

        ForThread2 ft1=new ForThread2();
        Thread t1=new Thread(ft1);
        Thread t2=new Thread(ft1);
        t1.setName("THread 1");
        t2.setName("THread 2");
        t1.start();
        t2.start();
        //3，利用callable和Future接口方式实现，特点与方式2相同

        ForThread3 f3=new ForThread3();//创建实现了Callable接口的类的对象
        FutureTask<String> ft2=new FutureTask<>(f3);//创建FutureTask
        Thread t3=new Thread(ft2);//创建线程对象
        t3.start();//启动线程

        String str1 = ft2.get();//利用FutureTask对象的get方法获得其运行结果
        System.out.println(str1);//打印出结果

        //线程的生命周期
        //创建线程对象（新建）-> 有执行资格，无执行权（就绪，各个线程对CPU进行抢夺）->有执行资格有执行权（运行），如果被其他的线程抢走执行权，就会接着去就绪状态
        //当遇到其他的阻塞方法时线程会停止，没有执行资格也没有执行权，在run（）方法执行完毕后，线程会死亡

    }
}
```

#### 线程常用方法

```java
public class Main {
    public static void main(String[] args) {
        //常用方法：
        //String getName() 返回此线程的名称
        //void setName(String name)   设置线程的名字（构造方法也可以设置名字）
        //static Thread currentThread()   获取当前线程的对象
        //static void sleep(long time)     让线程休眠指定的时间，单位为毫秒


        //getName()          线程如果没有初始化名字，线程会有自己的默认名字Thread-X（x是从0开始的）
        ForThread ft1=new ForThread();
        Thread t1=new Thread(ft1);
        t1.setName("getName演示线程");
        t1.start();
        //在使用构造方法设置时，需要在子类重写一个对象
        //currentThread：获取当前线程的对象   
        Thread t2 = Thread.currentThread();
        System.out.println(t2.getName());//此处显示main  代表当前存在一个main线程
        // 当Java运行时，虚拟机会自动启动多条线程，其中的main线程就是所写的main方法里的代码，在之前所写代码基本都在mian线程中
        //sleep:那条线程执行到这个代码，就会休眠，休眠的时间长短与其中的参数有关，休眠结束继续执行之后的代码
        ForThread ft2=new ForThread("Thread构造方法演示");
        Thread t3=new Thread(ft2);
        t3.start();
        System.out.println(t3.getName());
    }
}

//线程优先级
public class Main {
    public static void main(String[] args) {
        //Thread方法
        //优先级：线程的优先级越高，优先运行的概率越大
        //线程的默认优先级为5         1~10
        //获取优先级的方法getPriorityd()
        //main线程的优先级默认为5
        ForThread01 ft1=new ForThread01();
        Thread t1=new Thread(ft1,"First");
        Thread t2=new Thread(ft1,"Second");
//        t1.start();
//        t2.start();
        System.out.println(t1.getPriority());//5
        System.out.println(t2.getPriority());//5

        t1.setPriority(10);
        t2.setPriority(1);
        //优先级不是绝对的而是概率问题

        t1.start();
        t2.start();


    }
}


/////////////////////////////////////



//守护线程
public class Main {
    public static void main(String[] args) throws InterruptedException {
        //守护线程
        //setDaemon() 设置守护线程
        // 当其他的非守护线程执行完毕，守护线程会陆续结束
        //应用场景  QQ聊天
        //出让线程
        //yield()
        //出让当前的CPU的执行权，尽可能的使线程执行的密集一点
        ForThread01 ft1=new ForThread01();
        Thread t1=new Thread("出让线程测试方法测试线程");
        Thread t2=new Thread("线程2");

        //插入线程
        //join()
        //将调用该方法的线程插入到当前的线程之前
        t1.join();
        for (int i = 0; i < 100; i++) {
            System.out.println("main线程"+i);
        }
    }
}

public class ForThread01 implements Runnable{
    @Override
    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(Thread.currentThread().getName()+i);
        }
    }
}

```

#### 线程锁

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ForThread01 implements Runnable{
    static int tickets=1;
    static Lock lock=new ReentrantLock();//Lock锁，创建Lock对象，由于Lock只是一个接口，只能创建他的实现类的对象，锁对象有上锁方法和解锁方法

    //锁线程关键字：synchronized(锁){
    //                       操作共享数据的代码
    //}
    //特点：1.锁默认打开，有一个线程进去后锁会自动关闭     2.里面的代码全部执行完毕，线程出来，锁自动打开


    //创建一个唯一的锁对象(使用static关键字修饰),或者使用类的字节码文件进行传入
    public void run() {

        while (true){
            //lock.lock();//上锁
            //将能共享数据操作的代码锁起来，在一个线程操作时，其余的线程就算有执行资格，也无法对其进行操作
            //解决线程问题方法：1，同步代码块
            //把操作共享数据的代码锁起来
            synchronized (ForThread01.class) {//对其中的代码上锁，Ps：锁对象一定得是唯一的
                if(tickets<=100){
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    System.out.println(Thread.currentThread().getName()+"正在卖"+(tickets++)+"张票！");
                }else{
                    System.out.println("票已经卖完了！");
                    break;
                }
            }
            //lock.unlock();//解锁
            //在上述实例中，如果直接使用unlock()，会导致在循环中断后，锁对象未解锁，从而导致程序无法结束
            //解决方案：将代码块用try catch finally包裹，其中finally中的代码无论无论循环中断与否都可以正常执行，保证锁一定会被解开
        }
    }
}

////////////////////////////////////////


public class ForThread02 extends Thread{
    //同步方法
    int tickets=1;

    @Override
    public void run() {
        while (true)
         if(method()) break;
        }

    private synchronized boolean method() {//使用了synchronized关键字
            if(tickets==101){
                return true;
            }else {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                System.out.println(Thread.currentThread().getName()+"在卖第"+(tickets++)+"张票！");
            }
        return false;
    }
}


////////////////////////////////


public class Main {
    public static void main(String[] args) {
        ForThread02 ft1=new ForThread02();
        Thread t1=new Thread(ft1,"1号窗口");
        Thread t2=new Thread(ft1,"2号窗口");

        Thread t3=new Thread(ft1,"3号窗口");
        t1.setPriority(1);
        t2.setPriority(5);
        t3.setPriority(10);
        //由于多个线程在操作时具有随机性，所以在面对多个线程操作同一个数据时会出现实际数据错误的情况
        t1.start();
        t2.start();
        t3.start();
        //StringBuffer是线程安全的
    }
}

```



### 反射

```java
import java.lang.reflect.*;

public class Learn_reflex {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException, NoSuchFieldException {
        //反射：允许对成员变量 成员方法 构造函数进行编程访问的操作
        //获取class对象的三种方式：
        //1.全类名：Class.forName("全类名") 2.类名.class  3.对象.getclass
        Class clazz1 = Class.forName("Student");
        Class clazz2 = Student.class;
        Student s1=new Student();
        Class clazz3 = s1.getClass();
//        System.out.println(clazz1);
//        System.out.println(clazz2);
//        System.out.println(clazz3);
        //获取构造方法的对象
        //getConstructors()           返回所有公共构造方法对象的数组
        //getDeclaredConstructors()   返回所有构造方法对象的数组
        //getConstructors()           返回单个公共构造方法对象
        //getDeclaredConstructor()    返回单个构造方法对象


        //Constructor类中用于创建对象的方法
        //T newInstance(Object。。。initargs)   根据指定的构造方法创建对象
        //setAccessible(boolean flag)          设置为true，表示取消访问检查
        System.out.println("=======================0=====================");
        Class<?> clazz4 = Class.forName("Student");//字节码文件对象
        Constructor<?>[] cons1 = clazz4.getConstructors();
        for (Constructor<?> con1 : cons1) {
            System.out.println(con1);
        }//获取所有的公共构造方法
        System.out.println("=======================1=====================");
        //获取所有的构造方法
        Constructor<?>[] dcons1 = clazz4.getDeclaredConstructors();
        for (Constructor<?> constructor : dcons1) {
            System.out.println(constructor);
        }
        System.out.println("========================2====================");
        //获取单个构造
        Constructor<?> dcon1 = clazz4.getDeclaredConstructor();//括号里面的参数需要和构造方法里面的参数保持一致
        Constructor<?> cons2 = clazz4.getConstructor(String.class, int.class, String.class);
        System.out.println("=========================3===================");
        int modf1 = cons2.getModifiers();
        System.out.println(modf1);
        //每个权限修饰符都有属于自己的一个值，即权限修饰符的整数形式
        Parameter[] cons2Parameters = cons2.getParameters();
        for (Parameter cons2Parameter : cons2Parameters) {
            System.out.println(cons2Parameter);
        }
        //返回构造方法中的所有参数
        System.out.println("=========================4==================");
        //利用构造方法创建对象
        //暴力反射
        cons2.setAccessible(true);//要想使用newInstance方法创建对象需要使用setAccessible方法去取消权限修饰符的校验
        Student stu1 = (Student)cons2.newInstance("张三", 18,"male");//创建对象
        System.out.println(stu1);
        System.out.println("=========================5==================");
        //                  利用反射获取成员变量
        //getFileds()                返回所有公共成员变量对象的数组
        //getDeclaredFileds()        返回所有成员变量对象的数组
        //getFiled(String name)                   返回单个公共成员变量对象
        //getDeclaredFiled(String name)           返回单个成员变量

        //Filed类中的创建对象的方法
        //void set(Object obj,Object value) 赋值
        //Object get(Object obj)            获取值
        System.out.println("=========================6==================");
        Class<?> clazz5 = Class.forName("Student");//字节码文件对象
        Field[] clazz5Fields = clazz5.getFields();
        for (Field field : clazz5Fields) {
            System.out.println(field);//遍历输出
        }
        //获取所有的公共的成员变量
        System.out.println("=========================7==================");
        Field[] clazz5DeclaredFields = clazz5.getDeclaredFields();//获取所有的成员变量
        for (Field field : clazz5DeclaredFields) {
            System.out.println(field);//遍历输出
        }
        System.out.println("=========================8==================");
        //获取单个公共成员变量
        Field gender = clazz5.getDeclaredField("gender");//返回成员变量gender
        //此处为私有变量无法获取，需要用Declared
        //获取单个成员变量
        Field age = clazz5.getDeclaredField("age");//返回成员变量age
        int genderModifiers = gender.getModifiers();//权限修饰符号
        String genderName = gender.getName();//成员变量的名字
        Class<?> genderType = gender.getType();//成员变量的数据类型
        //获取成员变量对象的值
        gender.setAccessible(true);//临时取消修饰符权限检查
        Student stu2=new Student("张三",18,"male");
        Object gender_stu2 = gender.get(stu2);//返回stu2对象的gender
        //修改对象里面的值
        gender.set(stu2,"Formal");//修改stu2对象里的gender为Formal
        System.out.println("=========================9==================");
        //                      反射获取成员方法
        //getMethods()                  返回共有的成员方法对象的数组，包括继承的
        //getDeclaredMethods()          返回成员方法对象的数组，不包括继承的
        //getMethod()                   返回单个公有成员方法对象
        //getDeclaredMethod()           返回单个成员方法对象


        //Method类中用于创建对象的方法
        //object invoke(Object obj,Objecct ...args):运行方法
        //其中  参数一：用obj对象调用该方法  参数二：调用该方法的传递的参数(如果没有就不写)  返回值：方法的返回值(如果没有就不写)
        System.out.println("========================10==================");
        Class<?> clazz6 = Class.forName("Student");
        Method[] clazz6Methods = clazz6.getMethods();//获取所有公共方法对象数组
        for (Method method : clazz6Methods) {
            System.out.println(method);
        }
        Method[] clazz6DeclaredMethods = clazz6.getDeclaredMethods();//获取所有的方法对象的数组
        for (Method method : clazz6DeclaredMethods) {
            System.out.println(method);
        }
        System.out.println("========================11==================");
        Method clazz6Method1 = clazz6.getMethod("setName", String.class);
        Method clazz6Method2 = clazz6.getMethod("setAge", int.class);
        //获取指定的方法
        Method getName = clazz6.getDeclaredMethod("getName");
        Method setName = clazz6.getDeclaredMethod("setName", String.class);
        Method testReflex = clazz6.getDeclaredMethod("test_reflex", String.class);//此方法为私有使用DeclaredMethod
        //获取方法的所有信息
        //获取方法的权限修饰符
        int setNameModifiers = setName.getModifiers();
        //获取方法名字
        String setNameName = setName.getName();
        //获取参数的个数
        int setNameParameterCount = setName.getParameterCount();
        //获取参数的类型
        Class<?>[] setNameParameterTypes = setName.getParameterTypes();
        //获取参数的对象数组
        Parameter[] setNameParameters = setName.getParameters();
        for (Parameter parameter : setNameParameters) {
            System.out.println(parameter);
        }
        //获取方法的返回值
        //获取方法的抛出异常
        Class<?>[] testReflexExceptionTypes = testReflex.getExceptionTypes();
        for (Class<?> exceptionType : testReflexExceptionTypes) {
            System.out.println(exceptionType);
        }
        System.out.println("========================11==================");
        //invoke 方法
        Student stu3=new Student();
        Object invoke = testReflex.invoke(stu3, "李四");//设置stu3对象的名字为李四，利用反射调用testreflex方法
        System.out.println(invoke);//此处输出返回值，即invoke方法的接受值就是返回值
        System.out.println("========================12==================");
    }
}


//学生类
public class Student {
   private String name;
   private int age;
   private String gender;

    public Student() {
    }

    public Student(String name, int age, String gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return gender
     */
    public String getGender() {
        return gender;
    }

    /**
     * 设置
     * @param gender
     */
    public void setGender(String gender) {
        this.gender = gender;
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + ", gender = " + gender + "}";
    }
    private char test_reflex(String name){
        System.out.println(name);
        if (name.equals("0000"))throw new NullPointerException();
        if(name.equals("9999"))throw new RuntimeException();
        return name.charAt(1);

    }
    public void study(){
        System.out.println("学生在学习！");
    }
}

```

#### 利用反射写入将对象写入文件

```java
import java.io.*;
import java.lang.reflect.Field;

public class Test_Reflex {
    public static void main(String[] args) throws IllegalAccessException, IOException {
        Student s1=new Student("aaa",18,"male");
        Teacher t1=new Teacher(30,"bbb","English");
        File f1=new File("101.txt");
        saveObject(s1,f1);
    }
    public static void saveObject(Object obj, File pathname) throws IllegalAccessException, IOException {
        Class<?> objClasz = obj.getClass();
        BufferedWriter bw= new BufferedWriter(new FileWriter(pathname));//缓冲流
        Field[] objClaszDeclaredFields = objClasz.getDeclaredFields();
        for (Field field : objClaszDeclaredFields) {
            field.setAccessible(true);
            String name = field.getName();
            Object value = field.get(obj);
            bw.write(name+"="+value);
            bw.newLine();//换行
            System.out.println(name+"="+value);
        }
        bw.close();
    }
}
```

### Java_net

```java
import java.io.IOException;
import java.net.InetAddress;
import java.net.MulticastSocket;

public class group_net {
    public static void main(String[] args) throws IOException {
        //组播：IP范围：224.0.0.0~239.255.255.255
        //其中：224.0.0.0~224.0.0.255为预留的组播地址
        MulticastSocket ms=new MulticastSocket();//与单播的区别在于此处创建的为组播的对象
        //同样的，在没有参数的构造中使用随机的端口进行发送
        //打包数据和定义端口号操作相同（见SendData类）
        //在创建address对象时候，需要对多个数据接收对象进行同一个地址限制
        InetAddress address=InetAddress.getByName("224.0.0.1");

    }
}

```

```java
import java.util.ArrayList;

public class Java_net_learn {
    //三次握手：1.发出请求等待确认  2.回应请求   3.发出确认消息，链接建立
    //四次挥手：1.发出取消请求     2.接受请求同时验证服务的所有信息处理完毕  3.服务端发出确认信息
    // 4.客户端再次发送确认信息链接取消
    public static void main(String[] args) {

    }
}

```

```java
public class radio_net {
    public static void main(String[] args) {
        //广播地址：255.255.255.255
        //广播对象可以将IP改为255.255.255.255,直接就可以将信息发送在局域网的所有设备
    }
}

```

```java
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;

public class ReceiveData {
    public static void main(String[] args) throws IOException {
        //接收数据包
        //创建端口对象
        DatagramSocket ds=new DatagramSocket(10086);
        byte []bytes=new byte[1024];

        DatagramPacket dp=new DatagramPacket(bytes,bytes.length);//接收的数据包不需要IP和端口

        while (true) {
            ds.receive(dp);//接收数据包
            byte[] data = dp.getData();
            int length = dp.getLength();
            System.out.println(new String(data,0,length));//打印数据
        }
    }
}

```

```java
import java.io.IOException;
import java.net.*;
import java.util.Scanner;

public class SendData {
    public static void main(String[] args) throws IOException {
        DatagramSocket ds=new DatagramSocket();//创建端口对象
        //空参构造：在可用的端口中随机选择一个进行发送
        //带参构造：指定端口
        Scanner sc=new Scanner(System.in);
        while (true) {
            System.out.println("Please enter words!");
            String s = sc.nextLine();
            if(s.equalsIgnoreCase("886")){//输入886结束数据包输入
                break;
            }
            byte []bytes=s.getBytes();
            InetAddress address=InetAddress.getByName("127.0.0.1");//定义IP对象
            int port=10086;//定义端口（整形）
            DatagramPacket dp=new DatagramPacket(bytes,bytes.length,address,port);//打包数据包
            ds.send(dp);//利用端口对象调用send方法发送数据包
        }
        ds.close();//释放资源
    }
}
```

```java
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

public class TCP_net {
    public static void main(String[] args) throws IOException {
        //客户端 Socket   服务端 SeverSocket
        //创建Socket对象，链接服务端，如果无法连接就会报错
        Socket socket=new Socket("127.0.0.1",1000);
        String s1 = "Hello China!";
        String s2 = "Hello 中国!";
        OutputStream os = socket.getOutputStream();
        os.write(s2.getBytes());
        socket.close();//关闭流
        //由此可见 TCP的底层是利用了IO流进行数据的操作

    }
}

```

```java
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class TCP_receive {
    public static void main(String[] args) throws IOException {
        //创建服务器端
        ServerSocket serverSocket=new ServerSocket(1000);//绑定端口
        Socket accept = serverSocket.accept();//监听用户的链接
        InputStream inputStream = accept.getInputStream();
        InputStreamReader ir=new InputStreamReader(inputStream);//此处使用转换流，使得输入的中文可以被读取出来，不出现乱码
        // 字节流->字符流
        int b=0;
        while ((b=ir.read())!=-1){
            System.out.println((char) b);
        }

        accept.close();//断开与客户端的链接
        serverSocket.close();//关闭服务器

    }
}

```



### 大学Java实验

#### 实验一

```java
//贪心猪
public class Main {
    public static void main(String[] args) {
        Player_computer pc1=new Player_computer(0,0);
        Player_person pp1=new Player_person(0,0);
        Game_TanxinPig(pp1,pc1);
        System.out.println("最终比分：  "+"人类"+pp1.getSum_score()+":"+"电脑"+pc1.getSum_score());
        System.out.println( (pp1.getSum_score()> pc1.getSum_score()? "人类":"电脑")+"是赢家！");
    }
    public static void Game_TanxinPig(Player_person pp,Player_computer pc){
        System.out.println("贪心猪游戏开始！");
        System.out.println("你先手，输入R（r）重新投掷骰子，输入H（h）保留本轮已得分数，进入电脑回合");
        System.out.println("--------------------------------------------------------------");
        while (pp.getSum_score()<100&&pc.getSum_score()<100){
            //当任意一方的总分达到100结束
            System.out.println("你的分数为："+pp.getSum_score()+"分");
            System.out.println("电脑分数为："+pc.getSum_score()+"分");
            //输出双方成绩和与点数
            pp.Play();
            //人类玩家先手
            pc.Play();
            //电脑玩家后手
            System.out.println("=========================================================");
        }
    }
}

////////////////////////////////////////////////////////




public class Play {
    public void Game_TanxinPig(Player_person pp,Player_computer pc){
        while (pp.getSum_score()<100&&pc.getSum_score()<100){
            //当任意一方的总分达到100结束
            System.out.println(pp);
            System.out.println(pc);
            pp.Play();
            //人类玩家先手
            pc.Play();
            //电脑玩家后手
        }
    }
}


////////////////////////////////////////////////////////

import java.util.Random;

/**

 玩家类，代表电脑玩家
 */
public class Player_computer {
    private int Sum_score; // 玩家获得所有分数之和
    private int Now_score; // 玩家在本轮获得的分数

    /**

     构造函数，创建一个新的玩家对象
     */
    public Player_computer() {
    }
    /**

     构造函数，创建一个新的玩家对象，指定总得分和本轮得分
     @param Sum_score 玩家获得所有分数之和
     @param Now_score 玩家在本轮获得的分数
     */
    public Player_computer(int Sum_score, int Now_score) {
        this.Sum_score = Sum_score;
        this.Now_score = Now_score;
    }
    /**

     获取玩家获得所有分数之和
     @return 玩家获得所有分数之和
     */
    public int getSum_score() {
        return Sum_score;
    }
    /**

     设置玩家获得所有分数之和
     @param Sum_score 玩家获得所有分数之和
     */
    public void setSum_score(int Sum_score) {
        this.Sum_score = Sum_score;
    }
    /**

     获取玩家在本轮获得的分数
     @return 玩家在本轮获得的分数
     */
    public int getNow_score() {
        return Now_score;
    }
    /**

     设置玩家在本轮获得的分数
     @param Now_score 玩家在本轮获得的分数
     */
    public void setNow_score(int Now_score) {
        this.Now_score = Now_score;
    }
    /**

     重写toString方法，返回玩家对象的字符串表示形式
     @return 玩家对象的字符串表示形式
     */
    public String toString() {
        return "Player_computer{Sum_score = " + Sum_score + ", Now_score = " + Now_score + "}";
    }
    /**

     玩家进行游戏的方法，模拟电脑玩家的游戏过程
     */
    public void Play(){
        Random r=new Random(); // 创建随机数生成器
        int Dice=r.nextInt(6)+1; // 随机生成1-6之间的整数，模拟骰子投掷结果
        System.out.println("电脑投掷点数为："+Dice+"点"); // 输出电脑投掷结果
        if(this.Now_score<20){ // 如果本轮点数总数小于20
            if(Dice==1){ // 如果电脑投掷骰子为1，直接中断
                this.Now_score=0; // 本次不得分
            }else { // 如果电脑投掷骰子数为2-6，继续下去
                this.Now_score=this.Now_score+Dice; // 累加本轮所得分数
                Play(); // 递归，再次调用Play方法
            }
        }else { // 如果本轮点数总数大于等于20
            this.Sum_score=this.Sum_score+this.Now_score; // 总得分为：原总得分+本轮所得分
            this.Now_score=0; // 重置本轮的已得分数供下一轮使用
        }
        this.Sum_score=this.Sum_score+this.Now_score; // 累加总得分
    }
}



////////////////////////////////////////////////////////

import java.util.Random;
import java.util.Scanner;
/**
 * @author 计算机2103 郑子豪
 */

/**

 玩家类，用于描述一个玩家的信息和行为

 包括总分数和本轮得分数

 可以进行投掷骰子、保留得分或重新投掷的操作
 */
public class Player_person {

    /**

     玩家获得所有分数之和
     */
    private int Sum_score;
    /**

     玩家本轮所得分数之和
     */
    private int Now_score;
    /**

     空参构造器
     */
    public Player_person() {
    }
    /**

     全参构造器，第一个参数为Sum_score，第二个参数为Now_score
     @param Sum_score 玩家获得所有分数之和
     @param Now_score 玩家本轮所得分数之和
     */
    public Player_person(int Sum_score, int Now_score) {
        this.Sum_score = Sum_score;
        this.Now_score = Now_score;
    }
    /**

     获取玩家总得分数
     @return 玩家总得分数
     */
    public int getSum_score() {
        return Sum_score;
    }
    /**

     设置玩家总得分数
     @param Sum_score 玩家总得分数
     */
    public void setSum_score(int Sum_score) {
        this.Sum_score = Sum_score;
    }
    /**

     获取玩家本轮得分数
     @return 玩家本轮得分数
     */
    public int getNow_score() {
        return Now_score;
    }
    /**

     设置玩家本轮得分数
     @param Now_score 玩家本轮得分数
     */
    public void setNow_score(int Now_score) {
        this.Now_score = Now_score;
    }
    /**

     重写toString方法，返回玩家总得分数和本轮得分数
     @return 玩家总得分数和本轮得分数
     */
    public String toString() {
        return "Player_person{Sum_score = " + Sum_score + ", Now_score = " + Now_score + "}";
    }
    /**

     玩家游玩方法，投掷骰子、保留得分或重新投掷
     */
    public void Play(){
        Random r=new Random();
        int Dice = r.nextInt(6) + 1;//随机数构成的6面骰子
        System.out.println("你本次投掷点数为："+Dice+"点");

        if(Dice==1){
            this.Now_score=0;
        }else {
            Scanner sc=new Scanner(System.in);
            String s = sc.nextLine();
            if(s.equalsIgnoreCase("r")){//如果输入R（忽略大小写），重新投掷筛子，
                this.Now_score=this.Now_score+Dice;//再玩一局得分为：目前已经获得的分数+骰子的点数
                Play();//再次Play，进行递归
            } else if (s.equalsIgnoreCase("h")) {//如果输入H保留得分
                this.Sum_score=this.Sum_score+this.Now_score+Dice;//保留得分的分数为：目前总得分数为：原总分数+已得分数+骰子点数
                this.Now_score=0;
            }else{
                System.out.println("请玩家按要求重新输入");
                Play();//输入非R（r） 非H（h）玩家重新输入
            }
        }
    }
}

```

#### 实验二

```java
public class ItemnotFound extends RuntimeException{
    //异常类
    public ItemnotFound() {};
    public ItemnotFound(String message) {
        super(message);
    };
}


////////////////////////////////////////////////////////
import java.io.File;
import java.io.IOException;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedList;

public class Main {
    public static void main(String[] args) throws IOException {
        File f1=new File("C:\\Users\\83899\\Desktop\\101.txt");
        LinkedHashMap<String,Integer> itemList=new LinkedHashMap<>();
        itemList.put("Books",1);
        itemList.put("Magazine",1);
        itemList.put("DVD",1);
        itemList.put("Blurays",1);
        itemList.put("MusicCD",1);
        Store s1=new Store(itemList);
        Warehouse w1= new Warehouse(s1);
        boolean porn = w1.addItem(s1, "Porn");
        System.out.println(porn);//true
        boolean dvd = w1.borrowItem(s1, "DVD");
        System.out.println(dvd);//DVD已经成功借出
        boolean books = w1.deletItem(s1, "Books");
        System.out.println(books);//true
        int blurays = w1.searchItem(s1, "Blurays");
        System.out.println(blurays);//2
        boolean dvd1 = w1.InputFile(f1, s1, "DVD");
        System.out.println(dvd1);//true
    }
}

////////////////////////////////////////////////////////
import java.io.Serial;
import java.io.Serializable;
import java.util.LinkedHashMap;
import java.util.LinkedList;
//商店类
public class Store implements Serializable {
    @Serial
    private static final long serialVersionUID = -2478039495513913839L;
    public LinkedHashMap<String,Integer> itemList;


    public Store() {
    }

    public Store(LinkedHashMap<String, Integer> itemList) {
        this.itemList = itemList;
    }

    /**
     * 获取
     * @return itemList
     */
    public LinkedHashMap<String, Integer> getItemList() {
        return itemList;
    }

    /**
     * 设置
     * @param itemList
     */
    public void setItemList(LinkedHashMap<String, Integer> itemList) {
        this.itemList = itemList;
    }

    public String toString() {
        return "Store{itemList = " + itemList + "}";
    }
}



////////////////////////////////////////////////////////
import org.jetbrains.annotations.NotNull;

import java.io.*;


//仓库类
public class Warehouse extends Store {

    @Serial
    private static final long serialVersionUID = -3707654935347249552L;

    public Warehouse() {
    }

    public Warehouse(Store store) {
        this.itemList=store.itemList;
    }

    public boolean addItem(@NotNull Store store, String item){
        if (store.itemList.containsKey(item)){
            System.out.println("货物已经存在！");
            return false;
        }else {
            store.itemList.put(item,1);
            return true;
        }

    }
    public boolean deletItem(@NotNull Store store, String item){
        if (store.itemList.isEmpty()){
            return false;
        }
        else if(store.itemList.containsKey(item)){
            store.itemList.remove(item);
            return true;
        }else {
            return false;
        }

    }
    public int searchItem(@NotNull Store store, String item){
        if (store.itemList.isEmpty()){
            return -1;//如果货物链表为空返回-1
        }
        else {
            return (store.itemList.get(item)+1);
            //返回链表的逻辑位序
        }
    }
    public boolean borrowItem(@NotNull Store store, String item){
        if(store.itemList.isEmpty()){
            return false;//如果商店为空返回错误
        }else {
            if(store.itemList.get(item)==1){//货物未被借走
                System.out.println(item+"已经成功借出");
                store.itemList.remove(item);
                store.itemList.put(item,0);
                return true;
            }else if (store.itemList.get(item)==0){//货物已经被借出
                System.out.println(item+"已经被借出");
                throw new ItemnotFound();//抛出货物未找到异常
            }else {
                return false;//货物不存在
            }
        }
    }
    public boolean InputFile(File pathname, @NotNull Store store, String item) throws IOException {
        if(store.itemList.isEmpty()){
            return false;//如果列表为空
        }else if(store.itemList.containsKey(item)){//如果列表中包含货物
            char[]chars=new char[30];
            FileWriter fileWriter=new FileWriter(pathname);
            Integer integer = store.itemList.get(item);
            fileWriter.write(item+":"+integer);
            fileWriter.close();//关闭流
            return true;
        }else {
            //货物未找到
            throw new ItemnotFound();
        }
    }

    public String toString() {
        return "Warehouse{}";
    }
}
```

#### 实验三

##### 1.

```java
import java.util.ArrayList;

public class TimerAlarm extends Thread{

    private int totalSeconds = 0;
    private boolean isRunning = true;

    public void run() {
        while (isRunning) {
            totalSeconds++;
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public void stopTimer() {
        isRunning = false;
    }

    public void displayTime() {
        int hours = totalSeconds / 3600;
        int minutes = (totalSeconds % 3600) / 60;
        int seconds = totalSeconds % 60;
        System.out.printf("%02d:%02d:%02d\n", hours, minutes, seconds);
    }

    public void displayTotalSeconds() {
        System.out.println("Total seconds: " + totalSeconds);
    }
}
////////////////////////////////////////////////////////
import java.math.BigInteger;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        TimerAlarm timer = new TimerAlarm();
        timer.start();

        try {
            while (true) {
                timer.displayTime();
                Thread.sleep(1000);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            timer.stopTimer();
            timer.displayTotalSeconds();
        }
    }
}

```

##### 2.

```java
import cn.hutool.core.io.FileUtil;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        File word_sorce = new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\MyJava\\Code in (college)\\Test_13\\src\\words.txt");
        File newwords_sorce = new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\MyJava\\Code in (college)\\Test_13\\src\\newwords.txt");
        ArrayList<String> als = new ArrayList<>();
        FileUtil.readLines(word_sorce, "UTF-8", als);
        Collections.reverse(als);
        FileUtil.writeLines(als, newwords_sorce, "UTF-8", true);
    }
}
```

#### 实验四

```java
import javax.swing.*;
import java.util.ArrayList;
public class Windows extends JFrame  {
    public Windows() {
        this.setLayout(null);
        this.setVisible(true);
        this.setBounds(0,0,1000,600);

        JButton button_sort=new JButton("字典排序");
        button_sort.setBounds(200,300,100,20);//排序按钮
        this.add(button_sort);
        button_sort.setVisible(true);

        JButton button_clear=new JButton("清空");
        button_clear.setBounds(600,300,100,20);//清空按钮
        this.add(button_clear);
        button_clear.setVisible(true);

        JTextArea text_in=new JTextArea();
        text_in.setBounds(0,0,500,300);//输入文本框
        this.add(text_in);
        text_in.setVisible(true);

        JTextArea text_sort=new JTextArea();
        text_sort.setBounds(500,0,500,300);//排序文本框
        this.add(text_sort);
        text_sort.setVisible(true);

        button_clear.addActionListener(e -> {
            text_sort.setText("  ");
            text_in.setText("  ");
        });


        button_sort.addActionListener(e -> {
            ArrayList<String> als=new ArrayList<>();
            String s1=" ";
            String text []= text_in.getText().split("\n");
            for (String s : text) {
                als.add(s);
            }
            als.sort(String::compareTo);

            for (int i = 0; i < als.size(); i++) {
                if(i==1){
                    s1=als.get(i);
                }
                s1=s1+"\n"+als.get(i);
            }
            text_sort.setText(s1);
        });
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}


////////////////////////////////////////////



public class Main {
    public static void main(String[] args) {
        new Windows();
    }
}
```

# 前端框架

> ***bootcdn引入***

## Vue2

> vue2的标签引入

```html
  <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.6.13/vue.js"></script>
```

> 前提:安装node.js(版本大于16.0)
>
> 使用npm进行vue项目的创建或者直接使用标签引入

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>for vue</title>
  <link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css">
  <script src="https://cdn.bootcdn.net/ajax/libs/axios/1.3.6/axios.min.js"></script>
  <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.6.13/vue.js"></script>
</head>

<body>
  <div id="app">
  </div>
  <script>
    const vue1 = new Vue({
      el: '#app',//指定挂载点
      data: {
          //数据域用于存放变量
      },
      methods: {
        //methods用于存放方法,可以使用this.变量进行调用
      },
    })


  </script>
</body>
</html>
```

### vue2代码实例

```html
<!DOCTYPE html>
<html lang="zh" xmlns:th="http://www.thymeleaf.org">

<head>
  <meta charset="UTF-8">
  <title>demo</title>
</head>
<style>
  .big {
    height: 100px;
    width: 100px;
    /* 边框实线 */
    border: 1px solid black;
  }

  .pink {
    background-color: pink;
    height: 100px;
    width: 100px;
    border: 1px solid pink;
  }

  /* 添加表格边框每个单元格都是单实线 */
  table,
  th,
  td {
    width: 500px;
    height: 30px;
    border: 1px solid black;
    text-align: center;
    border-collapse: collapse;
  }

  /* div加边框线 */
</style>

<body>



  <div id="app">
    <template>
      <!-- 插值表达式:利用表达式插值 -->
      <!-- 不能在标签中使用 -->
      {{msg}}
      <br>
      <!-- 动态设置innerHTML -->
      <div v-html="location"></div>
      <!-- show -->
      <!-- 切换样式的隐藏,display:none -->
      <div v-show="flag">v-show</div>
      <!-- 条件渲染 -->
      <!-- 直接不显示 -->
      <div v-if="flag==1">条件渲染</div>
      <div v-else-if="flag==2">那就渲染</div>
      <div v-else>否则渲染</div>
      <!-- v-on事件绑定 -->
      <button v-on:click="count--">--</button>
      {{count}}
      <button @click="add">++</button>
      <br>
      <button @>取反</button>
      <!-- v-bind -->
      <div :title="title">你好</div>
      <!-- v-for -->
      <ul>
        <li v-for="(item,index) in name_list" :key="index" :title="item">
          {{item}}
        </li>
      </ul>
      <!-- v-model数据的双向绑定 -->
      <!-- trim自动去首尾空格 -->
      <!-- stop阻止冒泡,prevent阻止默认行为 -->
      <input type="text" v-model.trim="username">
      <span>{{username}}</span>
      <br>
      <!-- keyup.enter回车监听 -->
      <input @keyup.enter="password=''" type="password" v-model="password">
      <span>{{password}}</span>
      <br>
      <button @click="username='',password=''">重置</button>
      <!-- 控制类选择器,大括号的键值对选择和(类名的来回切换),中括号的类名全选(class列表) -->
      <div :class="{big:true,pink:pink_disp}">big</div>
      <button @click="ret">粉色切换{{pink_disp}}</button>
      <div :class="['big','pink']">big</div>
      <!-- 动态操作css样式 -->
      <!-- 加粗 -->
      <button :style="{color:'red',fontSize:'20px',bold:'normal'}">一行红字</button>
      <br>
      <!-- v-model多种绑定 -->
      <input type="text" v-model="words" value="text">{{words}}
      <br>
      <input type="checkbox" v-model="isCheck" value="checkbox">{{isCheck}}
      <br>
      <input type="radio" name="gender" v-model="gender" value="男">男
      <input type="radio" name="gender" v-model="gender" value="女">女
      <br>
      <div>性别:{{gender}}</div>
      <br>
      <select v-model="countryId">
        <option value="001">中国</option>
        <option value="002">美国</option>
        <option value="003">意大利</option>
      </select>
      <div>国家:{{countryId}}</div>
      <br>
      <textarea v-model="cv"></textarea>
      <p>简历:{{cv}}</p>
      <!-- computed计算属性和methods计算属性 -->
      <!-- computed封装了对数据的处理,求得了一个结果
      写在computed配置项中,作为属性直接使用
      拥有缓存特性
      -->
      姓:<input type="text" style="width: 15px;" v-model="firstName">
      名:<input type="text" style="width: 15px;" v-model="lastName">
      <br>
      <div>顺序全名:{{ fullName }}</div>
      <div>倒转全名:{{ secondName }}</div>
      <table>
        <thead>
          <tr>
            <th>学号</th>
            <th>姓名</th>
            <th>年龄</th>
            <th>性别</th>
            <th>分数</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody v-if="stuList.length>0">
          <tr v-for="(item,index) in stuList" :key="index">
            <td>{{item.stuId}}</td>
            <td>{{item.姓名}}</td>
            <td>{{item.年龄}}</td>
            <td>{{item.性别}}</td>
            <td>{{item.分数}}</td>
            <td>
              <button v-if="stuList.length>0" @click="delStu(index)">删除</button>
            </td>
          </tr>

        </tbody>
        <tbody v-else>
          <tr>
            <td colspan="7">暂无数据</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="7">
              学号<input type="text" style="width: 30px;" v-model="stuId">
              姓名<input type="text" style="width: 50px;" v-model="stuName">
              年龄<input type="text" style="width: 30px;" v-model="stuAge">
              性别<input type="text" style="width: 20px;" v-model="stuGender">
              分数<input type="text" style="width: 20px;" v-model="stuScore">
              <button @click="stuAdd()">添加</button>
            </td>
          </tr>
          <tr>
            <td v-if="stuList.length>0" colspan="7">学生共{{stuList.length}}人,平均分{{avg_score}}</td>
          </tr>
        </tfoot>
      </table>
      <br>
      <br>
      <!-- watch监听器 -->
      <!-- 存在深度监听可将对象数组的每一层属性同时监听 -->
      <textarea v-model="translate" name="trans">
      </textarea>
      <br>
      <input type="text" v-model="objRed.name">
      <br>
      <br>
      <!-- vue的生命周期的4个阶段 -->
      <!-- 创建阶段created,挂载阶段mounted,更新阶段updated,销毁阶段destroyed -->
      <!-- 创建阶段进行数据的初始化,挂载阶段进行实例的挂载,更新阶段数据不断在修改与更新视图中进行切换,销毁阶段vue实例会被销毁,各类定时器等资源会被释放,被卸载后不会进行任何的更新视图等操作 -->
      <!-- 分别对应8个相应的钩子函数 -->
      <!-- 搜索输入框案例:mounted后自动获取焦点 -->
      <input type="text" v-model="words" id="inp">
      <br>
      <br>
      <div id="eg" style="height: 450px;width: 500px;border: 1px solid black;"></div>



    </template>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue@2.7.14/dist/vue.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
  <script>
    const app = new Vue({
      // 指定挂载点
      el: '#app',
      // 数据渲染
      data: {
        msg: 'Hello Vue!',
        location: `<a href="https://www.baidu.com">百度</a>`,
        flag: 2,
        count: 0,
        title: '你好啊',
        name_list: ["张三", "李四", "王五"],
        username: '',
        password: '',
        pink_disp: false,
        words: '',
        isCheck: true,
        gender: '',
        countryId: '002',
        cv: '',
        firstName: '张',
        lastName: '三',
        stuAge: '',
        stuId: '',
        stuName: '',
        stuGender: '',
        stuScore: '',

        stuList: [
          { stuId: "001", 姓名: "张三", 年龄: 18, 性别: '男', 分数: 100 },
          { stuId: "002", 姓名: "李四", 年龄: 19, 性别: '女', 分数: 88 },
          { stuId: "003", 姓名: "王五", 年龄: 20, 性别: '男', 分数: 92 }
        ],
        translate: '',
        objRed: {
          name: 'redBox',
          style: {
            color: 'red'
          }
        },
        words: '',
      },
      computed: {
        fullName() {
          return this.firstName + this.lastName
        },
        // 计算属性两种写法,简易写法是属性值(),全写法(属性值:{get(){},set(){}},其中get代表是属性计算,而set是属性赋值)
        secondName: {
          get() {
            return this.lastName + this.firstName
          },
          set(value) {
            this.firstName = value.slice(0, 1)
            this.lastName = value.slice(1)
          }
        },
        avg_score() {
          // var sum = 0
          // this.stuList.forEach(item => {
          //   return item.分数 + sum
          // })
          // 求学生分数均值
          return (this.stuList.reduce((sum, item) => {
            return item.分数 + sum
          }, 0) / this.stuList.length).toFixed(1)
        }
      },
      methods: {
        add() {
          this.count++
        },
        ret() {
          this.pink_disp = !this.pink_disp
        },
        delStu(index) {
          this.stuList.splice(index, 1)
        },
        stuAdd() {
          if (isNaN(this.stuId) || isNaN(this.stuAge) || isNaN(this.stuScore) || (this.stuGender != '男' && this.stuGender != '女')) {
            alert('数据非法')
            return
          }
          if (this.stuId == '' || this.stuName == '' || this.stuAge == '' || this.stuGender == '' || this.stuScore == '') {
            alert('请填写完整信息')
            return
          } else {
            this.stuList.push({
              stuId: this.stuId,
              姓名: this.stuName,
              年龄: this.stuAge,
              性别: this.stuGender,
              分数: this.stuScore
            })
            // 再次置空
            this.stuId = this.stuName = this.stuAge = this.stuGender = this.stuScore = ''
          }
        },
      },
      watch: {
        translate(newValue, oldValue) {
          console.log(newValue, oldValue);
        },
        objRed: {
          deep: true,
          handler(newValue, oldValue) {
            console.log(newValue, oldValue);
          }
        },
      },
      mounted() {
        // document.querySelector('#inp').focus()
        var myChart = echarts.init(document.getElementById('eg'))
        var option = {
          title: {
            text: 'Referer of a Website',
            subtext: 'Fake Data',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: 'Access From',
              type: 'pie',
              radius: '50%',
              data: [
                { value: 1048, name: 'Search Engine' },
                { value: 735, name: 'Direct' },
                { value: 580, name: 'Email' },
                { value: 484, name: 'Union Ads' },
                { value: 300, name: 'Video Ads' }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
      }

    })

  </script>
</body>

</html>
```

## axios

> axios的标签引入

```html
<script src="https://cdn.bootcdn.net/ajax/libs/axios/1.3.6/axios.min.js"></script>
```

# JavaWeb

## JDBC

***(Java DataBase Connectivity)***

***面向接口编程,操作所有关系型数据库,对于不同的数据库进行不同的jar包进行导入***

### 基础实例

***1.导入对应数据库的jar包(以下使用MYSQL)***

```java
package org.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class Main {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
//        1.注册驱动
        Class.forName("com.mysql.jdbc.Driver");//可以省略
        String url = "jdbc:mysql://localhost:3306/jdbc_learning";
        String username = "root";
        String psw = "123456";
        //2.获取链接
        Connection connection = DriverManager.getConnection(url, username, psw);
//        3.定义sql语句
        String sql = "update student set age=25 where id=2  ";
//      4.获取执行sql对象
        Statement statement = connection.createStatement();
//        5.执行sql语句
        int update = statement.executeUpdate(sql);
//        6.返回处理结果
        System.out.println(update);
//        7.释放资源
        statement.close();
        connection.close();

    }
}

```

### API详解

#### DriverManager

***1.注册驱动***

***2.建立连接***

***在本机状态,默认端口可以直接写jdbc:mysql:///数据库名称,配置useSSL=false参数,解决警告提示***

#### Connection

***1.获取执行sql对象***

> 普通执行sql对象
>
> ```java
> Statement createStatement()
> ```
>
> 预编译sql执行的sql对象:防止sql注入
>
> ```java
> PreparedStatement prepareStatement(sql)
> ```
>
> 执行存储过程的对象
>
> ```java
> CallableStatement prepareCall(sql)
> ```
>
> 

***2.事务管理***

> JDBC事务管理:Connection接口中定义了3个对象的方法
>
> 开启事务:setAutocommit(boolean autoCommit):true为自动提交事务,false为手动提交
>
> 提交事务:commit()
>
> 回滚事务:rollback()

#### Statement

***1.执行sql语句***

> int excuteUpdate(sql):执行DML,DDL语句
>
> ResultSet excuteQuery(sql):执行DQL语句,返回值为结果集对象

#### ResultSet

***1.封装了DQL语句的查询结果***

> ```java
> boolean next():光标向下移动一行,判断当前行是否为有效行
> xxxgetInt(参数)
> xxxgetString(参数):int,列的编号从一开始;String,列的名称
> ```
>
> 

#### PreparedStatement

***1.预编译sql语句的对象,PreparedStatement继承于Statement***

***2.设置参数值***

> ```java
> PreparedStatement对象:setXxx(参数1,参数2):给?赋值
> 	Xxx:数据类型;如setInt(参数1,参数2)
> 	参数:
> 		参数1:?位置标号,1开始
> 		参数2:?的值
> ```

***3.执行sql***

> ```java
> excuteUpdate();/excuteQuery();:不需要传递sql
> ```

### 数据库连接池

> 标准接口(任何连接池都需要实现):DataSource
>
> ```java
> Connection getConnection()
> ```
>
> 常见数据库连接池:DBCP,C3P0,Druid



## HTML

### 常见标签

| 标签名              | 用法                                                         |
| ------------------- | ------------------------------------------------------------ |
| <br                 | html源码中换行                                               |
| <p</p               | 段落标签，用于在展示效果中划分段落，并自动在段前段后添加空白行<br />align参数：段落的对齐方式 |
| <h1</h1             | 标题标签，一共六级，h6最小                                   |
| &nbsp               | html源码中的多个空格，效果中最终合并为一个                   |
| <img/               | 图片标签  src参数：文件路径  weight，height：宽高            |
| <ul</ul             | 无序列表标签                                                 |
| <li</li             | 列表条目项标签，定义列表的条目                               |
| <ol</ol             | 有序列表标签                                                 |
| <a</a               | 超链接标签  href参数：超链接跳转路径  （可以跳转到网站链接，文件链接） |
| <table</table       | 表格标签，定义一个表格，  border：表格边框粗细，  width属性：设置表格的宽度 |
| <tr</tr             | 表格行标签                                                   |
| <td</td             | 表格单元格标签                                               |
| <th</th             | 表格的表头单元格标签，用于在效果中定义一个表格行中的表头单元格，<th  <td区别在于<th内容居中加粗<br />colspan属性：跨列合并单元格  rowspan属性：跨行合并单元格<br />属性值为需要合并的单元格的数量 |
| <span</span         | 行级的块标签，用于在效果中定义一个块，span有多少内容就会占多大空间，不会自动换行 |
| <div</div           | 块级的块标签，用于在效果中定义一块，默认占满一行，进行内容的展示，默认占满一行会自动换行 |
| <frameset</frameset | 框架标签，多个窗口页面整合在一起的一个集合（框架集），每个页面（框架）都是一个单独文档，都需要用子标签<frame来确定页面的位置，<frameset通过列和行来确定整体布局，使用cols确定列数，使用rows确定行数，多个<frameset可以嵌套使用<br /><frameset与<body不可以并存 |
| <frame              | src属性：确定页面的路径  noresize属性：框架分割线不移动<br />target属性：确定需要显示的页面在何处显示 |
|                     |                                                              |
|                     |                                                              |



## JavaScript

### jQuery库的在线引用

```html
  <script src="https://code.jquery.com/jquery-3.0.0.min.js"></script>
```

### 引入方式

#### 内部脚本

```html
<script>
	alert("hello world")
</script>
<!--可以出现任意次-->
```

#### 外部脚本

```html
<script src="test.js"></script>
<!--不能自闭合-->
```

### 基础语法

#### 输出

***Ps：1.单行注释和多行注释与Java相同  ***

***2.分号可有可无***

```html
<script>
    window.alert("hello world");//浏览器弹出警告框
	
	document.write("hello js!")//写入html在浏览器显示

	console.log("hello my js ")//写入浏览器控制台
 </script>
```

#### 变量

```js
//弱类型语言，用var关键字声明变量
var a=20
a=“test”

//var定义的变量为全局变量，可以重复声名


//在ECMAScript中新增了let关键字，其声名的变量仅在let代码块内有效，不允许重复声名
//新增const关键字，一旦声名不可更改
```

#### 数据类型

```js
//原始类型
number	//数字（整数，小数，NaN（Not a number））
string	//字符串（单双引号皆可）
boolean	//布尔
null	//空
undefined	//当声名的变量未初始化时默认为undefined

//引用类型

```

#### 运算符

```js
//算数运算符：	+ - * / % ++ --
//赋值运算符：	= += -= *= /= %=
//比较运算符：	> < >= <= != == ===		
//==会进行类型转换  ===不会进行类型转换
//逻辑运算符：	&& || ！
//三元运算符：	条件表达式?true_value:false_value

/*
类型转换
将字符串字面值转换为数字，如果字面值不是数字转为NaN
其他类型转boolean：1.Number：0，NaN均为false，其他true
					2.string：空字符串为false
					3.Null和undefined均为false
利用parseInt进行转数值操作
*/
//插值表达式：{{表达式}},内容可以是变量，三元运算符，函数调用，算术运算

```

#### 函数

```js
//定义方式1：利用function关键字进行定义
function func(a,b){
    console.log(a+b);
} 

//定义方式2：
var sum=function(a,b){
    return a+b
}
//形式参数不需要类型，返回值不需要定义类型，在内部直接进行返回
//如果参数传递超过形参接受数量只会接受前几个（取决于形参数量）
```

#### 对象

```js
//Array
//定义
	var arr1=new Array(1,"world")
	var arr2=[1,"hello"]
//访问
	var a=arr[index]
//特点：长度可变,类型可变
//属性：length
/*
   方法：forEach():遍历每个有值的元素，并调用一次传入的函数
    	push():追加元素到末尾并返回新数组长度
        splice():删除元素
        */
//forEach
	arr3[5]=[1,2,3,4,5]
	arr3.froEach(function(e){
    	console.log(e)
	})
//可优化为Lambda表达式
	arr3.froEach(e=>console.log(e))
//push
	var len=arr3.push(4)
//splice
    arr3.splice(begin_index,count_delete)

//String
//定义
	var str1=new String("hello world")
    var str2="hello world"
//属性：length
/*方法：
		charAt()：返回指定位置字符
		indexOf()：检索字符串
		trim()：去除头尾的空格
		substring():提取指定索引间的字符
	*/
//自定义对象
    var obj={
        name:"tom",
        age:20,
        learn:function(){
            alert("learning")
        }
    }
    obj.learn()
//JSON
//定义:JavaScript对象标记法
/*
	{
		"name":"Tom",
		"age":20
	}
	要求键值对的键使用双引号包含，多用于数据载体在网络进行数据传输
*/
    var var1='{"key1":"value1","key2":"value2"}'
/*
	value数据类型为：数字，字符串（在双引号中），逻辑值（true或false），数组（在中括号中），对象（在大括号中），null
*/
//属性
/*方法
	JSON.parse(jsStr):将JSON字符串转换为JS对象
	JSON。stringify(obj):将JS对象转换为JSON字符串
*/
//BOM
//定义：浏览器的每个部分被封装成BOM对象
/*属性：window：浏览器窗口对象	
		Navigator：浏览器对象	
		Screen：屏幕对象	         		
		History：历史记录对象
		Location：地址栏对象
*/
    /*
    	Window属性：history，location，navigator
    	Window方法：alert(),
    				confirm(),显示一段消息以及确认取消按钮的对话框,返回值为bool
    				setInterval(),在指定周期调用函数或计算式（ms）
    				setTimeout()，在指定的时间调用（ms）
    	
    	Location属性：href（设置返回完整的URL）
    	
    
    */
//DOM
//将标记型语言的每个部分标记为DOM对象
/*
	属性：Document：整个文档
			Element：元素对象（标签）
				Attribute：属性对象（标签的属性）
					Text:文本对象（标签的文本）
		Comment：注释对象

	Core DOM-所有文档类型的标注模型
	XML DOM-XML-XML文档的标准模型
	HTML DOM-HTML文档的标准模型
	
	方法:document.getElemnetById(),
		document.getElementBygetName(),
		document.getElementByName(),
		document.getElementByClassname()
*/

```

#### 时间监听

```js
/*
事件绑定
	方式1：通过HTML标签的事件属性 eg:<onclick>
	方式2：通过DOM的元素属性绑定 eg:document.getElementById('id').onclick=function(){
		alert("hello world")
	}
*/
/*
常见事件：
		onclick：鼠标点击事件
		onblur：元素失去焦点
		onfocus：元素获得焦点
		onload：某个页面或图像被完成加载
		onsubmit：当表单被提交触发
		onkeydown：键盘某个键按下
		onmouseover：鼠标被移到某元素上
		onmouseout:鼠标从某元素移开
*/
```

### Vue

```html
<!--新建文件引入Vue.js-->
<script src="js/vue.js"></script>

<!--定义Vue对象，el：Vue接管的区域，data对象-->
<script>
    new Vue({
        el: "#test",
        data: {
            message: "hello world"
        }
    })
</script>

<!--数据绑定-->
<div id="test">
    <input type="TEXT" v-model="message">
    {{ message }}
</div>
```

#### 常用指令

| 指令名    | 作用                                                         |
| --------- | ------------------------------------------------------------ |
| v-bind    | 为HTML标签绑定属性值<a v-bind:href="test”>                   |
| v-model   | 在表单元素上创建数据的双向数据绑定                           |
| v-on      | 为HTML绑定事件<input type="text" value="text...",v-on:click="handle()"> |
| v-if      |                                                              |
| v-else-if | 条件性的渲染某元素，绑定为true渲染                           |
| v-else    |                                                              |
| v-show    | 根据条件展示某元素，区别在于切换的是display属性的值          |
| v-for     | 列表渲染，遍历容器的元素或者对象的属性                       |
|           |                                                              |

#### 生命周期

| 状态（钩子方法） | 阶段周期 |
| ---------------- | -------- |
| beforeCreate     | 创建前   |
| created          | 创建后   |
| beforeMount      | 挂载前   |
| mounted          | 挂载后   |
| beforeUpdate     | 更新前   |
| updated          | 更新后   |
| beforeDestroy    | 销毁前   |
| destroyed        | 销毁后   |

## JSP

### 基础语法

#### 注释方式

```jsp
显示注释
	继承html中的注释语法,能够在客户端查看的注释
	<!--这是显式注释-->
隐式注释
	不能在客户端查看的注释
	1.&lt;%--JSP的自带注释--%&gt;
	2.继承JAVA风格的注释,需要写在JAVA的代码段中
	<%
		//这是java注释(单行)
		/*java多行注释*/
	%>
```

#### Scriptlet

```JSP
第一种
	<%     %>:java脚本段
第二种
	<%!    %>:声明,可以定义全局成员变量,方法,类
第三种
	<%=    %>:输出表达式,数据一个变量或者具体内容
```

#### JSP的指令标签

##### include静态包含

```JSP
<%@ include file="path" %> <!--相对路径-->
静态包含是将内容直接进行替换,不能出现同名变量
```

##### 动态包含

```jsp
<jsp:include page="path"></jsp:include>
可以包含同名的变量
```

### 四大域对象(在合理范围内尽可能小)

#### page范围

***pageContext:只能在一个页面保存属性,跳转之后无效***

> 

#### request范围

***request:只在一次请求中保存,服务器跳转仍然有效***

> 

#### session范围

***session:在一次会话范围中,无论何种跳转都可能使用***

> 

#### application范围

***application:在整个服务器中保存***

> 

### 跳转

#### 服务端跳转

```JSP
<jsp:forward page="path"></jsp:forward>
```



#### 客户端跳转

```jsp
<a href="link">jump</a>
```

## Maven

***专门用于构建项目的工具***

> 提供标准项目构建工具
>
> 提供项目一整套打包流程
>
> 提供项目的依赖

***对于java版本不同的解决***

**方法一**

```xml
<properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
</properties>

```

**方法二,Maven的setting.xml配置文件**

```xml
<profile>
     <id>jdk-13</id>
     <activation>
         <activeByDefault>true</activeByDefault>
         <jdk>13</jdk>
     </activation>
     <properties>
         <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
         <maven.compiler.source>17</maven.compiler.source>
         <maven.compiler.target>17</maven.compiler.target> 
     </properties> 
</profile>
<!-- jdk自行选择--!>
```



### 仓库

> ***本地仓库:本地的目录***
>
> ***中央仓库:Maven维护的仓库***
>
> ***远程仓库:私人,公司维护的仓库***

### 常用命令

```shell
compile,test,package,install
```

### 坐标详解

> groupid:当前的Maven项目的隶属机构(包名)
>
> artifactid:定义当前的Maven项目名称(通常是模块名)
>
> version:定义当前版本号
>
> scope依赖范围
>
> ```xml
> <dependency>
>  <groupid>mysql</groupid>
>  <artifactid>mysql-connector-java</artifactid>
>  <version>5.1.46</version>
>  <scope>runtime</scope>
> </dependency>
> 
> ```



# Tomcat

## 安装配置

配置Tomcat环境变量前一定要配置好java的环境变量，尤其是JAVA_HOME

以下环境变量均在系统环境变量中设置。

> ***新建 CATALINA_HOME 环境变量，变量：CATALINA_HOME 值：D:\DevelopmentTool\apache-tomcat-9.0.43***
> ***修改 Path ，在 Path 后添加(新建)：***
>
> *** %CATALINA_HOME%\lib、%CATALINA_HOME%\bin%CATALINA_HOME%\lib\servlet-api.jar***

*环境变量中，环境变量名对大小写不敏感，可将CATALINA_HOME小写，但需要保持一致*
*注意：在环境变量中，如果新建有两个相同仅大小写不同的的变量名，会覆盖设置。如：path和PATH*

> Tomcat文件目录
>
> bin：可执行文件（启动文件startup.bat、关闭文件shutdown.bat）
> conf：配置文件（修改端口号：server.xml，建议将server.xml备份）
> lib：依赖的jar包
> log：日志文件（记录出错等信息）
> temp：临时文件
> webapps：可执行的项目。默认作为存放开发项目的目录
> work：存放由jsp翻译成的.java源文件,以及编译的.class字节码文件(jsp ->java ->class)
> 其他文件

## 常见问题

### 闪退

> 可能原因是：环境变量配置不正确
>
> JAVA_HOME中的路径不能用分号结尾，如C:\Program Files\Java\jdk1.8.0_121
> JAVA_HOME的路径是JDK路径，而不是JRE的路径。
> CATALINA_HOME中的路径不能以\结尾。
> 在环境变量中修改添加变量时，一定要注意分号、空格，是否有多余的字母。

### 乱码

> 问题描述：打开startup.bat后汉字乱码
> 解决方法：在.\apache-tomcat-9.0.43\conf下打开logging.properties文件
>
> 将java.util.logging.ConsoleHandler.encoding = UTF-8
> 替换为java.util.logging.ConsoleHandler.encoding = GBK

### 与其他服务的端口号冲突

**tomcat端口号默认8080，如果和其他服务的端口号冲突，则可对端口号进行修改**
**在.\apache-tomcat-9.0.43\conf下打开server.xml文件，在文件的69行左右，将port="8080"修改为指定的某一端口号，重新启动。**

```properties
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
```

### 常见状态码

> 200：一切正常
> 300/301：页面重定向 （跳转）
> 404：资源不存在
> 403：权限不足 （如果访问a目录，但是a目录设置 不可见）
> 500：服务器内部错误（代码有误）
> 其他编码：积累

## 启动Tomcat

***方法一**：**在.\apache-tomcat-9.0.43\bin目录下，双击startup.bat打开窗口，双击shutdown.bat关闭窗口。***

***如果点startup.bat窗口的×直接关闭，可能会造成关闭异常***

***方法二：***通过命令行窗口打开。cmd命令cd到.\apache-tomcat-9.0.43\bin，然后输入命令：startup，出现如下对话框，表明服务启动成功。

# Servlet

## 入门案例

### Servlet Demo1.java

```java
package com.zoe;

import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import java.io.IOException;

@WebServlet("/demo1")
public class ServletDemo1 implements Servlet {
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {

    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {

        System.out.println("hello Servlet,coming!");
    }

    @Override
    public String getServletInfo() {
        return null;
    }

    @Override
    public void destroy() {

    }
}



```

### 依赖

***解决servlet-api冲突***

```xml
<dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
</dependency>
```

## Servlet生命周期

> 加载和实例化:默认下,当Servlet第一次被访问,由容器创建Servlet对象
>
> ​	loadOnStartup属性:何时调用init方法
>
> 初始化:Servlet实例化后,容器调用init方法,初始化Servlet对象(只执行一次)
>
> 请求处理:每次请求Servlet,都会调用service方法
>
> 服务终止:调用destroy方法,释放init申请的资源
>
> ​	调用时机:内存释放和服务关闭的时候

> getServletConfig() :获取ServletConfig对象
>
> getServletInfo():获取Servlet的信息

## Servlet体系结构

> Servlet(Servlet体系根接口)
>
> GenericServlet(Servlet抽象实现类)
>
> HttpServlet(对HTTP协议封装的Servlet实现类)

## Servlet的urlPattern配置

> 1.一个Servlet可以配置多个urlPattern
>
> 2.匹配规则
>
> ​	精确匹配:
>
> ```java
> @WebServlet(urlPatterns="/demo")
> ```
>
> ​	目录匹配
>
> ```java
> @WebServlet(urlPatterns="/demo/*")
> ```
>
> ​	扩展名匹配
>
> ```java
> @WebServlet(urlPatterns="*.do")
> ```
>
> ​	任意匹配
>
> ```java
> @WebServlet(urlPatterns="/")
> @WebServlet(urlPattern="/*")
> ```

## XML配置方式编写Servlet

```xml
    <servlet>
        <servlet-name>demo2</servlet-name>
        <servlet-class>com.zoe.ServletDemo2</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>demo2</servlet-name>
        <url-pattern>/demo2</url-pattern>
    </servlet-mapping>
```

## Request

### Request获取请求数据

```JAVA
请求行
	String getmethod();//获取请求方式
	String getContextPath();获取虚拟目录(项目访问路径)
	StringBuffer getRequestURL();获取URL(统一资源定位符)
	String getRequestURI();获取URI(统一资源标识符)
	String getQueryString();获取请求参数(GET)
    
请求头
    String getHeader(String name);根据请求头名称获取值
请求体
    ServletInputStream getInputStream();获取字节输入流
    BufferedReader getReader();获取字符输入流
        
        
```

### Request获取请求参数

```java
Map<String,String []> getParameterMap();获取所有参数的集合
String [] getParameterValues(String name);根据名称获取参数值(数组)
String getParameter(String name);根据名称获取参数值(单个)
```

### Request请求转发

```java
request.getRequestDispacher("/path").forward(request,response)
```

```java
//请求转发资源间共享:使用Request对象
void setAttribute(String name,Object o);//存储数据在request域中
Object getAtttribute(String name);//根据key 获取值
void removeAttribute(String name);根据key删除键值对
```

> 特点:1.网址栏不变 2.只能在服务器内部转发 3.一次转发可在转发的资源间使用request共享数据

## Response

### Redirect重定向

```java
response.setHeader("Location","/path-module/resp");
//或者
response.sendRedirect("/path");

```

> 特点:1.地址栏发生变化  2.可以重定向任意位置 3.两次请求不能在多个资源使用request贡献数据

#### 路径问题

> 浏览器使用:需要加虚拟目录
>
> 服务端使用:不需要加虚拟目录

### Response响应字符数据

```java
resp.getWriter().write("test");
```



### Response响应字节数据

```java
resp.getOutputStream().write("qwe");
```

## MVC

> M:module
>
> V:view
>
> C:Contoller

## 三层架构

> 表现层:接受请求,封装数据,调用业务逻辑层,响应数据
>
> 业务逻辑层:对业务逻辑进行封装组合数据访问层层中的基本功能,形成复杂的业务逻辑功能
>
> 数据访问层:对数据CURD进行基本的操作

## Cookie

> Cookie:客户端会话技术,将数据保存在客户端,以后每次请求都携带Cookie数据进行访问

```java
//发送Cookie
Cookie cookie=new Cookie("key","value");
response.addCookie(cookie);

//获取Cookies
Cookie [] cookies=request.getCookies();
cookie.getName();
cookie.getValue();
```

### Cookie原理(基于HTTP)

> 响应头:set-cookie
>
> 请求头:cookie

### Cookie使用细节

> Cookie存活时间:默认状态下,存在浏览器中,当浏览器关闭,内存释放,Cookie销毁,setMaxAge(int seconds)设置存活时间
>
> Cookie存储中文

## Session

> 服务端会话跟踪技术,JavaEE的HttpSessioon技术
>
> void setAttribute(String name,Object o);存储到session域中
>
> Object getAttribute(String name);根据key,获取值
>
> void removeAttribute(String name);根据key,删除该键值对

### Session原理

> 基于Cookie实现

### Session使用细节

> 钝化:服务器正常关闭后,Tomcat会自动将Session数据写入硬盘的文件中
>
> 活化:再次启动服务器后,从文件中加载Session
>
> Session销毁:默认下无操作30min自动销毁 ,或者调用invalidate()方法

> 小结:
>
> ​	存储位置:Cookie存储在客户端,Session存储在服务端
>
> ​	安全性:Cookie不安全,Session安全
>
> ​	数据大小:Cookie最大3KB,Session大小无限制
>
> ​	存储时间:Cookie无时间限制,Session默认30min
>
> ​	服务器性能:Cookie不占服务器资源,Session占服务器资源

## Fileter

```java
//定义类实现Fileter接口,并重写所有方法
public class FilterDemo implements Filter {
	public void init(FilterConfig filterConfig);
	public void doFilter(ServletRequest request);
	public void destroy();
}

//配置Filter拦截的资源路径,在类上定义@Webservlet注解
@WebFilter("/*")

//在doFilter方法中输出一句话,并放行
public void doFilter(ServletRequest request,Ser.........){
	System.out.println("filter被执行");
	chain.doFilter(request,response);
}
```

#### Filter拦截路径

> 拦截具体资源:/index.jsp:只有访问index.jsp会被拦截
>
> 目录拦截:/user/*:拦截/user下的所有资源,都会被拦截
>
> 后缀名拦截:*.jsp:访问后缀名为jsp的资源,都会被拦截
>
> 拦截所有:/*:拦截所有的资源,都会被拦截

#### 过滤器链

> 根据XML决定顺序,没有配置XML就由类名决定(字符串类名自然排序)

## Listener

> 监听application,session,request的创建,销毁,其中属性添加修改的删除属性时自动执行代码功能的组件

## AJAX

> 异步的JavaScript和XML
>
> 使用AJAX和HTML替换JSP页面

# Spring框架

## 第一部分核心容器

### 核心概念

***Ioc  DI***

### 项目实例

#### 文件实例

```xml
<dependencies>
        <!-- https://mvnrepository.com/artifact/org.springframework/spring-context -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>5.2.10.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
<!--导入依赖-->
```

```xml
<!--1. import spring-context,map the 5.2.10 RELEASE-->

<!--   2. bean config-->
    <bean id="bookDao" class="Spring_Learning.mysping_program.dao.impl.BookDaoImpl">
    </bean>
    <bean id="booService" class="Spring_Learning.mysping_program.service.impl.BookServiceImpl">
    </bean>
```

***提供依赖对象的setter方法***

```java
public class BookServiceImpl implements BookService {


    //5.
    private BookDao bookDao;

    @Override
    public void save() {
        System.out.println("book service save");
        bookDao.save();
    }


    //6.set method
    public void setBookDao(BookDao bookDao) {
        this.bookDao = bookDao;
    }
}

```

***配置service与dao之间的关系***

```xml
<!--   2. bean config-->
    <bean id="bookDao" class="Spring_Learning.mysping_program.dao.impl.BookDaoImpl"/>

    <bean id="booService" class="Spring_Learning.mysping_program.service.impl.BookServiceImpl">
<!--        set the relation of bean,property:obj  ref :reference-->
        <property name="bookDao" ref="bookDao"/>
    </bean>
```

#### ***实例化bean三种方法：***

> *1.构造方法：空参*
>
> *2.使用静态工厂实例化bean，即用bean标签的factory-method参数指定方法*
>
> *3.实例工厂造bean，非静态*

##### Bean的生命周期

> **初始化容器**
>
> *创建对象（内存分配）*
>
> *执行构造方法*
>
> *执行属性注入*
>
> ***执行bean初始化方法***
>
> **使用bean**
>
> *执行业务操作*
>
> **关闭/销毁容器**
>
> 执行销毁方法
>
> 方式：
>
> ​		1.手动关闭
>
> ​		2.注册关闭钩子
>
> **依赖注入**
>
> ​		1.setter注入
>
> ​					简单类型：可访问的set方法和property标签设置
>
> ```xml
> <bean id="bookDao" class="Spring_Learning.myspring_program.dao.impl.BookDaoImpl" init-method="init" destroy-method="destroy">
>      <property name="connectionCount" value="10"/>
>      <property name="mysql" value="database"/>
>  </bean>
> ```
>
> ​					引用类型
>
> ​		2.构造器注入
>
> ​					简单类型
>
> ​					引用类型
>
> ***Ps：依赖注入setter较为灵活***
>
> ##### 依赖自动装配
>
> ***Ps:1.自动装配用于引用类型的依赖注入，不对简单类型操作  2.使用ByType必须保证容器中相同类型的数据唯一  3.使用byName时必须保证容器中有指定名称的bean  4.自动装配优先级低于setter注入与构造器注入***
>
> ##### 集合注入

### 标签介绍

> bean标签
>
> id：别名，可以使用一个或多个，多个需用空格 分号和逗号隔开  
> class：全类名 
> scope：多例与单例（默认）切换，控制对象创建 ,作用范围 (request,session,globalsession)
> factory-method：静态工厂创建  
> factory-bean：实例化工厂对象 
> init-method destroy-method 初始化和销毁方法
> autowire：自动装配

> property标签:属性注入
>
> name:属性名称
>
> value:普通属性值
>
> ref:对象引用值

> list标签,map标签,properties标签,constructor-arg标签

> import标签:导入其他Spring的配置文件

### Spring相关API

> getBean()方法:1.使用ID匹配	2.使用Class字节码

> ApplicationContext可以用XML或者File实例化

### Spring原始注解

| 注解           | 说明                                           |
| -------------- | ---------------------------------------------- |
| @Component     | 类上实例化Bean                                 |
| @Controller    | 使用web层类上用于实例化Bean                    |
| @Service       | 使用Service层类上用于实例化Bean                |
| @Repository    | 使用在dao层类上用于实例化                      |
| @Autowired     | 使用在字段上用于根据类型依赖注入               |
| @Qualifier     | 结合@Autowired一起使用用于根据名称进行依赖注入 |
| @Resource      | 相当于@Autowired+@Qualfier,按照名称进行注入    |
| @Value         | 注入普通属性                                   |
| @Scope         | 标注Bean的作用范围                             |
| @PostConstruct | 使用在方法上标注该方法是Bean的初始化方法       |
| @PreDestroy    | 使用在方法上标注该方法是Bean的销毁方法         |

### Spring新注解

| @Configuration  | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| @ConponentScan  | 用于指定当前类是一个Spring配置类,创建容器时会从该类上加载注解 |
| @Bean           | 用与指定Spring在初始化容器哦时要扫描的包,作用和在Spring的xml文件中的<context:comonent-scan-base-package="com.zoe"/>一样 |
| @PropertySource | 用于加载properties文件中的配置                               |
| @Import         | 用于导入其他配置类                                           |



### 容器基本操作

## 第二部分整合

### 整合数据层技术MyBatis

#### Json格式获取

> Controller:
>
> ​	获取普通pojo的json信息:
>
> ```json
> {
> 	"name":"Jhon",
> 	"age":"15",
> 	"address":{
> 		"province":"shanxi",
> 		"city":"xian"
> 	}
> }
> ```
>
> ```java
> @ResponseBody
> @Requestmapping
> public String pojoParamForJson(@RequestBody User user){
> 	return user;
> }
> ```
>
> ​	获取pojo集合的json信息:
>
> ```json
> 	[	
> 
> 		{"name":"Jhon","age":28},
> 
> 		{"name":"Kitty","age":18}
> 
> 	]
> ```

#### Restful风格处理

> 1. 使用HTTP动词来代表不同的操作：
>    - `GET /users`：获取所有用户列表。
>    - `GET /users/{id}`：获取指定id的用户信息。
>    - `POST /users`：添加新用户。
>    - `PUT /users`：更新单个用户信息。
>    - `PUT /users/batch`：批量更新多个用户信息。
>    - `DELETE /users/{id}`：删除指定id的用户。
> 2. URL中使用名词表示资源，避免使用动词：
>    - 不推荐使用`/select`、`/insert`、`/update`、`/delete`等动词表示操作，而是直接使用资源名`/users`，并通过HTTP动词来表示操作类型。
> 3. 使用复数名词来表示集合资源：
>    - `/users`表示所有用户列表。
>    - `/users/{id}`表示单个用户。

## 第三部分AOP

### 核心概念

### AOP基础操作

### AOP实用开发

## 第四部分事务

### 事务实用开发

# MyBatis

***JavaEE三层架构：表现层，业务层，持久层(MyBatis)***

## 核心配置文件

***Program-config.xml***

| 字段            | 使用       |
| --------------- | ---------- |
| mapper          | 映射       |
| environment     | 环境控制   |
| typeAliases     | 引入别名   |
| settingsplugins | 设置       |
| properties      | 属性       |
| plugins         | 插件       |
| typeHandlers    | 类型处理器 |
| objectFactory   | 对象工厂   |

## 基础步骤

***编写接口方法：Mapper接口----编写SQL语句：SQL映射文件----执行方法，测试***

```java
//导入配置文件
String resource = "MyBatis_program-config.xml";
        InputStream inputStream = Resources.getResourceAsStream(resource);
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

//获取SqlSession对象
        SqlSession sqlSession = sqlSessionFactory.openSession();

//使用SQL语句



//关闭流


sqlsession.close();
```

### 数据库的字段名称与实体类的名字不同步

***1.可以在SQL数据库中给字段起别名，即在Mapper映射文件中的SQl语句使用as对字段起别名      缺点：效率过低，每次查询需要重写***

***对于上述方法推出在xml文件中使用sql标签，对字段取别名，再在原语句进行引用***

```xml
<sql id="newname">id as name</sql>

<select id="selectALl" resultType="classname">
	select
    	<include refid="newname"/>
    from table_class;
    
</select>
```

***2.resultMap(灵活操作)***

```xml
<!--id：唯一标识   type：类的别名-->
<resultMap id="nameresultMap" type="table_newname">
	<result> column="name in database column" property="property in class"</result>
</resultMap>


<!--id: 主键字段的标签   result：一般字段的标签，分别有两个属性：column,property-->

<select id="method name" resultMap="nameresultMap">
	select
    	*
    from tablename;

</select>
```

### 查询案例

### 方法映射文件xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "https://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="mybatis_test.mapper.BrandMapper">
    <select id="selectAll" resultType="Brand">
        select * from Brand;
    </select>

    <!--selectByid方法映射文件-->
	<select id="selectByid" parameterType="int "resultType="Brand">    
        select *
        <!--在参数查询使用小于号‘<’可以使用&lt -->
        <!--可以使用<![CDATA[内容]]，简写CD-->
        from Brand where id = #{id};
    <!--此处使用#{id} 可以保证运行是为?占位符   使用${id}会直接出现参数会有Sql注入安全隐患-->
    </select>
    
    <select id="selectByCondition" resultType="Brand">
        select *
        from Brand
        where status_now = #{status_now}
        and name_company like #{name_company}
        and name_goods like #{name_goods}
    </select>
    
     <!--dynamic sql-->
    <select id="selectByCondition" resultType="Brand">
        
        select *
        from Brand
        where
            1=1
        
        <!--if标签，用于判断参数是否有值，使用test属性进行条件判断，存在问题：第一个条件不需要逻辑运算符，使用where标签保证语句的正确性，可以使用恒等式解决-->
            <if test="status_now != null">and status_now = #{status_now}</if>
            <if test="name_company != null and name_company != ''">and name_company like #{name_company}</if>
            <if test="name_goods != null and name_goods != ''">and name_goods like #{name_goods}</if>


    </select>
    
    
     <select id="selectByCondition" resultType="Brand">
        select *
        from Brand
        <where>
<!--使用where标签，自动补全语句，-->
            <if test="status_now != null">status_now = #{status_now}</if>
            <if test="name_company != null and name_company != ''">and name_company like #{name_company}</if>
            <if test="name_goods != null and name_goods != ''">and name_goods like #{name_goods}</if>

        </where>
    </select>
    
    <!--单条件的动态查询-->
    <select id="selectByConditionSingle" resultType="Brand">

        <
        select *
        from Brand
        <where>
            <choose>
                <!--choose标签相当于switch语句，同样的when是case,otherwise相当于default,可以不写oherwise标签加上where标签-->
                <when test="status_now != null ">
                    status_now= #{status_now}
                </when>
                <when test="name_company != null and name_company != '' ">
                    name_company=#{name_company}
                </when>
                <when test="name_goods != null and name_goods != '' ">
                    name_goods = #{name_goods}
                </when>
                <otherwise>
                    1=1
                </otherwise>
            </choose>
        </where>;
    </select>



<!--添加操作，添加了useGenerateKeys属性和keyproperty属性使得id属性可以主键传递-->
    <insert id="add" useGeneratedKeys="true" keyProperty="id" >
        insert into Brand (name_goods, name_company, status_now, logo, id)
        VALUES(#{name_goods}, #{name_company}, #{status_now}, #{logo}, #{id})
    </insert>
<!--修改操作，使用了动态语句，if标签的test对输入进行判断-->
    <update id="update" useGeneratedKeys="true" keyProperty="id" >
        update Brand
        <set>
            <if test="status_now != null">status_now = #{status_now},</if>
            <if test="name_company != null and name_company != ''">name_company = #{name_company},</if>
            <if test="name_goods != null and name_goods != ''">name_goods = #{name_goods},</if>
            <if test="logo != null">logo = #{logo},</if>
        </set>
        where id = #{id}
    </update>
<!--删除操作，删除指定id的数据-->
    <delete id="deleteByid">
        delete from Brand
        where id = #{id}
    </delete>

<!--批量删除，设定一个集合或者列表，利用foreach标签对其进行遍历，collections是集合名，也可以添加注解使用array,separate为分隔符，open,close分别表示开头与结尾字符，例中为(?,?)-->
    <delete id="deleteByids">
        delete from Brand
        where id in 
        <foreach collection="ids" item="id" separator="," open="(" close=")">
            #{id}
        </foreach>
    </delete>


</mapper>
```

### 核心配置文件xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "https://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>

    <typeAliases>
        <package name="mybatis_test.pojo"/>
    </typeAliases>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <!--database connection info-->
                <property name="driver" value="org.mariadb.jdbc.Driver"/>
                <property name="url" value="jdbc:mariadb://localhost:3306/mybatis"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
<!--    waiting :    load sql mapper file-->
<!--        <mapper resource="mybatis_test/mapper/userMapper.xml"/>-->
            <package name="mybatis_test.mapper"/>
        
    </mappers>
</configuration>
```

### 方法接口

```java
package mybatis_test.mapper;

import mybatis_test.pojo.Brand;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

public interface BrandMapper {

    //select all
    @Select("select * from Brand")
    List<Brand> selectAll();


    //check info of brand
    Brand selectByid(int id);

    //tiaojian chaxun

    //unpacked property


    /**
     *
     * @param status_now
     * @param name_company
     * @param name_goods
     * @return
     */

    List<Brand> selectByCondition(@Param("status_now") int status_now,@Param("name_company") String name_company, @Param("name_goods")String name_goods);


    //make it a duixiang
    List<Brand> selectByCondition2(Brand brand);
    List<Brand> selectByCondition3(Map map);



    //single condition
    @Select("select * from brand where status_now = #{status_now} and name_company = #{name_company} and name_goods = #{name_goods}")
    List<Brand> selectByConditionSingle(Brand brand);


    //add brand
    void add(Brand brand);

    //update brand
    Integer update(Brand brand);

    //delete Byid
    void deleteByid(int id);

    //delete By ids
    void deleteByids(@Param("ids") List<Integer> ids);


}


```

### 实体类

```java
package mybatis_test.pojo;

public class Brand {
//    name_goods varchar(10),
//    name_company varchar(10),
//    status_now boolean

    private int id;
    private String logo;
    private String name_goods;
    private String name_company;
    private int status_now;


    public Brand() {
    }

    public Brand(int id, String logo, String name_goods, String name_company, int status_now) {
        this.id = id;
        this.logo = logo;
        this.name_goods = name_goods;
        this.name_company = name_company;
        this.status_now = status_now;
    }

    public Brand(int statusNow, String nameCompany, String nameGoods) {
        this.status_now=statusNow;
        this.name_company=nameCompany;
        this.name_goods=nameGoods;
    }

    public Brand(int id, int statusNow, String nameCompany, String nameGoods, String logo) {
        this.id = id;
        this.status_now = statusNow;
        this.name_company = nameCompany;
        this.name_goods = nameGoods;
        this.logo = logo;
    }


    /**
     * 获取
     * @return id
     */
    public int getId() {
        return id;
    }

    /**
     * 设置
     * @param id
     */
    public void setId(int id) {
        this.id = id;
    }

    /**
     * 获取
     * @return logo
     */
    public String getLogo() {
        return logo;
    }

    /**
     * 设置
     * @param logo
     */
    public void setLogo(String logo) {
        this.logo = logo;
    }

    /**
     * 获取
     * @return name_goods
     */
    public String getName_goods() {
        return name_goods;
    }

    /**
     * 设置
     * @param name_goods
     */
    public void setName_goods(String name_goods) {
        this.name_goods = name_goods;
    }

    /**
     * 获取
     * @return name_company
     */
    public String getName_company() {
        return name_company;
    }

    /**
     * 设置
     * @param name_company
     */
    public void setName_company(String name_company) {
        this.name_company = name_company;
    }

    /**
     * 获取
     * @return status_now
     */
    public int getStatus_now() {
        return status_now;
    }

    /**
     * 设置
     * @param status_now
     */
    public void setStatus_now(int status_now) {
        this.status_now = status_now;
    }

    public String toString() {
        return "Brand{id = " + id + ", logo = " + logo + ", name_goods = " + name_goods + ", name_company = " + name_company + ", status_now = " + status_now + "}";
    }
}

```





## mybatis概念

### mybatis事务

***openSession():默认开启事务，进行增删改操作后需要使用sqlSession.commit手动提交事务***

***openSession(true)：可以设置为自动提交事务（关闭事务）***  

### mybaitis参数封装

***常规单个参数可以使用arg,param代替，即arg0,param0-9，也可以使用@param(“eg”)注解变量***

***Map集合：直接使用，键名与参数占位符名称一致***

***Collection，List,Array都是封装为Map集合，可以使用@Param注解，替换集合中的默认atg键名***

> 批量更新是一次执行多个update语句，所以mybatis需要额外的配置：
>
> 在`spring.datasource.url`后加上`allowMultiQueries=true`
>
> 如：`jdbc:mysql://10.10.20.36:3306/test?allowMultiQueries=true`

# 计算机科学(computer-science)

## 计算机网络体系

### OSI体系结构（七层）（Open System Interconnection Reference Model）

***应用层***：**为应用程序或用户请求提供各种请求服务**。OSI参考模型最高层，也是最靠近用户的一层，为计算机用户、各种应用程序以及网络提供接口，也为用户直接提供各种网络服务。

***表示层***：**数据编码、格式转换、数据加密**。提供各种用于应用层数据的编码和转换功能,确保一个系统的应用层发送的数据能被另一个系统的应用层识别。如果必要，该层可提供一种标准表示形式，用于将计算机内部的多种数据格式转换成通信中采用的标准表示形式。数据压缩和加密也是表示层可提供的转换功能之一。

***会话层***：**创建、管理和维护会话**。接收来自传输层的数据，负责建立、管理和终止表示层实体之间的通信会话，支持它们之间的数据交换。该层的通信由不同设备中的应用程序之间的服务请求和响应组成。

***传输层***：**数据通信**。建立主机端到端的链接，为会话层和网络层提供端到端可靠的和透明的数据传输服务，确保数据能完整的传输到网络层。

***网络层***：**IP选址及路由选择**。通过路由选择算法，为报文或通信子网选择最适当的路径。控制数据链路层与传输层之间的信息转发，建立、维持和终止网络的连接。数据链路层的数据在这一层被转换为数据包，然后通过路径选择、分段组合、顺序、进/出路由等控制，将信息从一个网络设备传送到另一个网络设备。

***数据链路层***：**提供介质访问和链路管理**。接收来自物理层的位流形式的数据，封装成帧，传送到网络层；将网络层的数据帧，拆装为位流形式的数据转发到物理层；负责建立和管理节点间的链路，通过各种控制协议，将有差错的物理信道变为无差错的、能可靠传输数据帧的数据链路。

***物理层***：**管理通信设备和网络媒体之间的互联互通**。传输介质为数据链路层提供物理连接，实现比特流的透明传输。实现相邻计算机节点之间比特流的透明传送，屏蔽具体传输介质和物理设备的差异。

### TCP/IP结构（四层）

***应用层***：主要有负责web浏览器的HTTP协议， 文件传输的FTP协议，负责电子邮件的SMTP协议，负责域名系统的DNS等。

***传输层***：主要是有可靠传输的TCP协议，特别高效的UDP协议。主要负责传输应用层的数据包。

***网络层***：主要是IP协议。主要负责寻址（找到目标设备的位置）

***链路层***：主要是负责转换数字信号和物理二进制信号。

### 五层协议体系结构

***应用层***：应用层是网络协议的最高层，主要任务通过进程间的交互完成特定网络应用。应用层协议定义的是应用程序（进程）间通信和交互的规则。

***传输层***：：它负责为两台主机中的进程提供通信服务。该层主要有以下两种协议：

传输控制协议 (Transmission Control Protocol，TCP)：提供面向连接的、可靠的数据传输服务，数据传输的基本单位是报文段（segment）：用户数据报协议 (User Datagram Protocol，UDP)：提供无连接的、尽最大努力的数据传输服务，但不保证数据传输的可靠性，数据传输的基本单位是用户数据报。

***网络层***：网络层负责为分组网络中的不同主机提供通信服务，并通过选择合适的路由将数据传递到目标主机。在发送数据时，网络层把运输层产生的报文段或用户数据封装成分组或 包进行传送。

​				*PS*：在TCP/IP体系中，由于网络层使用IP协议，因此分组也叫IP数据报

***数据链路层***：数据链路层通常简称为链路层。数据链路层在两个相邻节点传输数据时，将网络层交下来的IP数据报组装成帧，在两个相邻节点之间的链路上传送帧

***物理层***：保数据可以在各种物理媒介上进行传输，为数据的传输提供可靠的环境。

******

## 网络协议（Internet protocol）

#### TCP协议（Transmission Protocol）

***应用层次：传输层***

TCP/IP协议是互联网的基础协议，包括传输控制协议（TCP）和网络协议（IP），它们共同构成了互联网的通信协议标准。

#### 三次握手

三次握手的过程如下：
客户端发送SYN包（SYN=1，ACK=0）给服务器端，进入SYN_SENT状态。

服务器端收到SYN包，发送一个SYN包（SYN=1，ACK=1）和确认包ACK（ACK=1）给客户端，进入SYN_RCVD状态。

客户端收到服务器端的SYN和ACK包，发送一个确认包ACK（ACK=1）给服务器端，建立连接，进入ESTABLISHED状态。

#### 四次挥手

四次挥手的过程如下：
客户端发送一个FIN包（FIN=1）给服务器端，请求关闭连接，进入FIN_WAIT_1状态。

服务器端收到FIN包，发送一个确认包ACK（ACK=1）给客户端，进入CLOSE_WAIT状态。

服务器端关闭连接，发送一个FIN包（FIN=1）给客户端，进入LAST_ACK状态。

客户端收到服务器端的FIN包，发送一个确认包ACK（ACK=1）给服务器端，进入TIME_WAIT状态。在等待2MSL（最大报文段寿命）后，进入CLOSED状态。服务器端收到客户端的确认包ACK后，进入CLOSED状态。

#### http协议（HyperText Transfer Protocol）

***应用层次：应用层***

超文本传输协议（HTTP）是一种用于传输超媒体文档（如HTML）的协议，是Web的基础协议。

***架构在TCP协议上***

> 请求数据分三部分
>
> 请求行:GET表示请求方式,HTTP/1.1 表示协议版本
>
> 请求头:格式为键值对形式
>
> 请求体:POST请求的最后一部分,存放请求参数
>
> ***GET与POST的请求区别:GET的请求参数在请求行中,没有请求体,POST请求请求参数在请求体中,GET请求参数大小有限制***

> 响应数据分3部分
>
> 响应行:HTTP/1.1表示协议版本,响应状态码,状态码描述
>
> 响应头:键值对形式
>
> 响应体:存放响应数据
>
> | 状态码分类 | 说明       |
> | ---------- | ---------- |
> | 1XX        | 响应中     |
> | 2XX        | 成功       |
> | 3XX        | 重定向     |
> | 4XX        | 客户端错误 |
> | 5XX        | 服务端错误 |
>
> 

#### https协议（HyperText Transfer Protocol over Secure Socket Layer）

HTTP+SSL/TLS， 即 HTTP 下加入 SSL 层，HTTPS 的安全基础是 SSL，因此加密的详细内容就需要 SSL，用于安全的 HTTP 数据传输。

#### DNS协议（Domain Name System）

***应用层次：应用层***

DNS（Domain Name System：域名系统），与 HTTP、FTP 和 SMTP 一样，DNS 协议也是应用层的协议，用于将用户提供的主机名（域名）解析为 IP 地址。

简单来说，DNS 就像是一个自动的电话号码簿，我们可以直接拨打 47.105.127.0 呼叫对方，但这不方便记录、记忆，DNS 提供一种手段能够让我们直接拨打对方的域名找到对方

#### FTP协议（File Transfer Protocol）

***应用层次：传输层***

***B/S架构***

***默认端口：22***

是应用层的一个**文件传输协议** 。主要作用是在服务器和客户端之间实现文件的传输和共享。FTP协议运行在TCP连接上，保证了文件传输的可靠性。在传输时，传输双方的操作系统、磁盘文件系统类型可以不同。

允许TCP/IP网络上的两台计算机之间进行文件传输。而FTP服务是基于FTP协议的文件传输服务。工作时，一台计算机上运行FTP客户端应用程序，另一台计算机上需要运行FTP服务器端程序。只有拥有了FTP服务，客户端才能进行文件传输。

#### SMTP协议（Simple Mail Transfer Protocol）

***默认端口：25***

SMTP是一种提供可靠且有效的电子邮件传输的协议。SMTP是建立在FTP文件传输服务上的一种邮件服务，主要用于系统之间的邮件信息传递，并提供有关来信的通知。SMTP独立于特定的传输子系统，且只需要可靠有序的数据流信道支持，SMTP的重要特性之一是其能跨越网络传输邮件，即“SMTP邮件中继”。使用SMTP，可实现相同网络处理进程之间的邮件传输，也可通过中继器或网关实现某处理进程与其他网络之间的邮件传输。

#### POP3协议（Post Office Protocol - Version 3）

POP3，全名为“Post Office Protocol - Version 3”，即“邮局协议版本3”。是TCP/IP协议族中的一员，由RFC1939 定义。本协议主要用于支持使用客户端远程管理在服务器上的电子邮件。提供了SSL加密的POP3协议被称为POP3S。
POP 协议支持“离线”邮件处理。其具体过程是：邮件发送到服务器上，电子邮件客户端调用邮件客户机程序以连接服务器，并下载所有未阅读的电子邮件。这种离线访问模式是一种存储转发服务，将邮件从邮件服务器端送到个人终端机器上，一般是PC机或 MAC。一旦邮件发送到 PC 机或MAC上，邮件服务器上的邮件将会被删除。但POP3邮件服务器大都可以“只下载邮件，服务器端并不删除”，也就是改进的POP3协议。

#### IMAP协议（Internet Message Access Protocol）

***应用层次：应用层***

***默认端口：143	***

IMAP（Internet Message Access Protocol）以前称作交互邮件访问协议（Interactive Mail Access Protocol），是一个应用层协议。IMAP是斯坦福大学在1986年开发的一种邮件获取协议。它的主要作用是邮件客户端可以通过这种协议从邮件服务器上获取邮件的信息，下载邮件等。当前的权威定义是RFC3501。IMAP协议运行在TCP/IP协议之上，使用的端口是143。它与POP3协议的主要区别是用户可以不用把所有的邮件全部下载，可以通过客户端直接对服务器上的邮件进行操作。

#### SSL协议（Secure Socket Layer）

***应用层次：传输层***

SSL（Secure Socket Layer）安全套接层是Netscape公司率先采用的网络安全协议。它是在传输通信协议（TCP/IP）上实现的一种安全协议，采用公开密钥技术。SSL广泛支持各种类型的网络，同时提供三种基本的安全服务，它们都使用公开密钥技术。

#### TLS协议（Transport Layer Security）

***应用层次：传输层***

安全传输层协议（TLS）用于在两个通信应用程序之间提供保密性和数据完整性。
该协议由两层组成： TLS 记录协议（TLS Record）和 TLS 握手协议（TLS Handshake）

#### UDP协议（User Datagram Protocol）	

***应用层次：传输层***

是一个简单的面向消息的传输层协议，尽管UDP提供标头和有效负载的完整性验证（通过校验和），但它不保证向上层协议提供消息传递，并且UDP层在发送后不会保留UDP 消息的状态。因此，UDP有时被称为不可靠的数据报协议。如果需要传输可靠性，则必须在用户应用程序中实现。

UDP使用具有最小协议机制的简单无连接通信模型。UDP提供数据完整性的校验和，以及用于在数据报的源和目标寻址不同函数的端口号。它没有握手对话，因此将用户的程序暴露在底层网络的任何不可靠的方面。如果在网络接口级别需要纠错功能，应用程序可以使用为此目的设计的传输控制协议（TCP）。

