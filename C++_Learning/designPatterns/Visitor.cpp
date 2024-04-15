#include <iostream>
#include <vector>

// 前向声明访问者类
class Visitor;

// 元素接口
class Shape {
public:
    virtual void accept(const Visitor& visitor) const = 0;
};

// 具体元素类：圆形
class Circle : public Shape {
private:
    double radius;

public:
    Circle(double radius) : radius(radius) {}

    double getRadius() const {
        return radius;
    }

    void accept(const Visitor& visitor) const override;
};

// 具体元素类：矩形
class Rectangle : public Shape {
private:
    double width;
    double height;

public:
    Rectangle(double width, double height) : width(width), height(height) {}

    double getWidth() const {
        return width;
    }

    double getHeight() const {
        return height;
    }

    void accept(const Visitor& visitor) const override;
};

// 访问者接口
class Visitor {
public:
    virtual void visitCircle(const Circle& circle) const = 0;
    virtual void visitRectangle(const Rectangle& rectangle) const = 0;
};

// 具体访问者类：计算面积和周长
class AreaPerimeterVisitor : public Visitor {
public:
    void visitCircle(const Circle& circle) const override {
        double area = 3.14 * circle.getRadius() * circle.getRadius();
        double perimeter = 2 * 3.14 * circle.getRadius();
        std::cout << "Circle - Area: " << area << ", Perimeter: " << perimeter << std::endl;
    }

    void visitRectangle(const Rectangle& rectangle) const override {
        double area = rectangle.getWidth() * rectangle.getHeight();
        double perimeter = 2 * (rectangle.getWidth() + rectangle.getHeight());
        std::cout << "Rectangle - Area: " << area << ", Perimeter: " << perimeter << std::endl;
    }
};

// 实现元素类的 accept 方法
void Circle::accept(const Visitor& visitor) const {
    visitor.visitCircle(*this);
}

void Rectangle::accept(const Visitor& visitor) const {
    visitor.visitRectangle(*this);
}

int main() {
    Circle circle(5.0);
    Rectangle rectangle(3.0, 4.0);

    AreaPerimeterVisitor visitor;
    circle.accept(visitor);
    rectangle.accept(visitor);

    return 0;
}
