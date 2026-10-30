/**
 * Runnable demonstrations of ten core object-oriented programming concepts in Java.
 * Compile and run from this directory with:
 *   javac OOPConceptsDemo.java
 *   java OOPConceptsDemo
 */
public class OOPConceptsDemo {

    public static void main(String[] args) {
        demonstrateSingleInheritance();
        demonstrateMultilevelInheritance();
        demonstrateHierarchicalInheritance();
        demonstrateMethodOverloading();
        demonstrateMethodOverriding();
        demonstrateAbstraction();
        demonstrateEncapsulation();
        demonstrateConstructors();
        demonstrateConstructorChaining();
        demonstrateModifiers();
    }

    private static void demonstrateSingleInheritance() {
        heading("1. Single inheritance");
        Dog dog = new Dog();
        dog.eat(); // inherited from Animal
        dog.bark(); // defined in Dog
    }

    private static void demonstrateMultilevelInheritance() {
        heading("2. Multilevel inheritance");
        C object = new C();
        System.out.println("A property: " + object.propertyA);
        object.methodA();
        System.out.println("B property: " + object.propertyB);
        object.methodB();
        object.methodC();
    }

    private static void demonstrateHierarchicalInheritance() {
        heading("3. Hierarchical inheritance");
        Child1 first = new Child1();
        Child2 second = new Child2();
        first.showSharedFeature();
        first.child1Feature();
        second.showSharedFeature();
        second.child2Feature();
    }

    private static void demonstrateMethodOverloading() {
        heading("4. Method overloading (compile-time polymorphism)");
        Calculator calculator = new Calculator();
        System.out.println("add(int, int): " + calculator.add(4, 6));
        System.out.println("add(int, int, int): " + calculator.add(4, 6, 8));
        System.out.println("add(double, double): " + calculator.add(2.5, 3.1));
    }

    private static void demonstrateMethodOverriding() {
        heading("5. Method overriding (runtime polymorphism)");
        Vehicle vehicle = new Car(); // parent reference, child object
        vehicle.start(); // Java selects Car's implementation at runtime
    }

    private static void demonstrateAbstraction() {
        heading("6. Abstraction");
        Shape shape = new Circle();
        shape.draw(); // caller uses the abstract operation without needing its details
    }

    private static void demonstrateEncapsulation() {
        heading("7. Encapsulation");
        BankAccount account = new BankAccount(100.00);
        account.setBalance(150.00);
        System.out.printf("Balance after controlled update: $%.2f%n", account.getBalance());
    }

    private static void demonstrateConstructors() {
        heading("8. Default and parameterized constructors");
        Book defaultBook = new Book();
        Book configuredBook = new Book("Java Basics", 19.99);
        System.out.println(defaultBook);
        System.out.println(configuredBook);
    }

    private static void demonstrateConstructorChaining() {
        heading("9. Constructor chaining with this()");
        Employee defaultEmployee = new Employee();
        Employee namedEmployee = new Employee("Maya");
        Employee fullyConfiguredEmployee = new Employee("Arun", 42000.00);
        System.out.println(defaultEmployee);
        System.out.println(namedEmployee);
        System.out.println(fullyConfiguredEmployee);
    }

    private static void demonstrateModifiers() {
        heading("10. final, static, and abstract modifiers");
        ModifierBase first = new ModifierDemo("Reporting");
        ModifierBase second = new ModifierDemo("Analytics");
        first.showCategory(); // final method: subclasses cannot override it
        first.performTask(); // implemented by the concrete subclass
        second.performTask();
        ModifierBase.showObjectCount(); // static member belongs to the class

        FinalLabel label = new FinalLabel("Read-only label");
        System.out.println("Final class instance: " + label.getText());
        // ModifierBase cannot be instantiated directly because it is abstract.
        // FinalLabel cannot be subclassed because it is final.
    }

    private static void heading(String title) {
        System.out.println("\n" + title);
    }
}

// 1. Single inheritance: Dog receives eat() from Animal.
class Animal {
    public void eat() {
        System.out.println("Animal eats.");
    }
}

class Dog extends Animal {
    public void bark() {
        System.out.println("Dog barks.");
    }
}

// 2. Multilevel inheritance: C inherits from B, and therefore also from A.
class A {
    protected String propertyA = "Inherited from A";

    public void methodA() {
        System.out.println("Method from A.");
    }
}

class B extends A {
    protected String propertyB = "Inherited from B";

    public void methodB() {
        System.out.println("Method from B.");
    }
}

class C extends B {
    public void methodC() {
        System.out.println("Method from C.");
    }
}

// 3. Hierarchical inheritance: both children share Parent's field and method.
class Parent {
    protected String familyName = "Sharma";

    public void showSharedFeature() {
        System.out.println("Shared family name: " + familyName);
    }
}

class Child1 extends Parent {
    public void child1Feature() {
        System.out.println("Child1 has its own feature.");
    }
}

class Child2 extends Parent {
    public void child2Feature() {
        System.out.println("Child2 has its own feature.");
    }
}

// 4. Overloaded methods are selected by their parameter lists at compile time.
class Calculator {
    public int add(int first, int second) {
        return first + second;
    }

    public int add(int first, int second, int third) {
        return first + second + third;
    }

    public double add(double first, double second) {
        return first + second;
    }
}

// 5. The method call is resolved using the actual object type at runtime.
class Vehicle {
    public void start() {
        System.out.println("Vehicle starts.");
    }
}

class Car extends Vehicle {
    @Override
    public void start() {
        System.out.println("Car starts with a push of a button.");
    }
}

// 6. Shape specifies what to do; Circle supplies the drawing implementation.
abstract class Shape {
    public abstract void draw();
}

class Circle extends Shape {
    @Override
    public void draw() {
        System.out.println("Drawing a circle.");
    }
}

// 7. Private state can only be read or changed through the public methods.
class BankAccount {
    private double balance;

    public BankAccount(double openingBalance) {
        setBalance(openingBalance);
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        if (balance < 0) {
            throw new IllegalArgumentException("Balance cannot be negative.");
        }
        this.balance = balance;
    }
}

// 8. Two constructor forms initialize a Book in different ways.
class Book {
    private final String title;
    private final double price;

    public Book() {
        this("Untitled", 0.0);
    }

    public Book(String title, double price) {
        this.title = title;
        this.price = price;
    }

    @Override
    public String toString() {
        return "Book{title='" + title + "', price=$" + String.format("%.2f", price) + "}";
    }
}

// 9. Each shorter constructor delegates initialization to another constructor.
class Employee {
    private final String name;
    private final double salary;

    public Employee() {
        this("Unknown");
    }

    public Employee(String name) {
        this(name, 0.0);
    }

    public Employee(String name, double salary) {
        this.name = name;
        this.salary = salary;
    }

    @Override
    public String toString() {
        return "Employee{name='" + name + "', salary=$" + String.format("%.2f", salary) + "}";
    }
}

// 10. Abstract classes cannot be instantiated; final members restrict changes.
abstract class ModifierBase {
    private static int objectCount = 0;
    private final String category;

    protected ModifierBase(String category) {
        this.category = category;
        objectCount++;
    }

    public static void showObjectCount() {
        System.out.println("ModifierBase objects created: " + objectCount);
    }

    public final void showCategory() {
        System.out.println("Final category value: " + category);
    }

    public abstract void performTask();
}

class ModifierDemo extends ModifierBase {
    public ModifierDemo(String category) {
        super(category);
    }

    @Override
    public void performTask() {
        System.out.println("Concrete subclass performs its task.");
    }
}

final class FinalLabel {
    private final String text;

    public FinalLabel(String text) {
        this.text = text;
    }

    public String getText() {
        return text;
    }
}
