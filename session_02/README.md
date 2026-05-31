## Session 2: Implementing Design Patterns in Python for Robust Architecture

**Goal:**
Learn key design patterns and how to implement them in Python to build maintainable and robust applications.

**Definition:**
Design patterns are standard solutions to common software design problems. They promote reusability and cleaner code structure. Use cases include managing shared resources (Singleton), abstracting object creation (Factory), and handling events (Observer). Mastery of these patterns leads to clearer communication among developers and more scalable applications.

**Documentation Reference:**
- https://refactoring.guru/design-patterns/python
- https://www.tutorialspoint.com/python_design_patterns/index.htm

### Tutorial:
- Introduction to Singleton: Explain why you might need only one instance of a class.
```py
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)
```
- Explanation: Both instances refer to the same object.
- Discussion: Briefly mention other patterns (Factory, Observer) for context.

### Exercise:

- Problem: Implement the Factory pattern to create shape objects (e.g., Circle and Square).

- Steps to Solve:
    - Define an abstract Shape class.
    - Create concrete classes for Circle and Square.
    - Write a factory function to return the correct object.

### Challenge:

- Problem: Implement the Observer pattern to notify multiple observers when a subject’s state changes.
- Hint: Create a Subject class that maintains a list of observers.
