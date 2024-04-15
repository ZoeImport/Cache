#include <iostream>
#include <vector>
#include <string>

// 完整定义 User 类
class User {
protected:
    class ChatRoomMediator* mediator;
    std::string name;

public:
    User(ChatRoomMediator* mediator, const std::string& name) : mediator(mediator), name(name) {}

    virtual void sendMessage(const std::string& message) = 0;
    virtual void receiveMessage(const std::string& message) = 0;

    const std::string& getName() const {
        return name;
    }
};

// 中介者接口
class ChatRoomMediator {
public:
    virtual void sendMessage(const std::string& message, User* sender) = 0;
};

// 具体中介者类
class ChatRoom : public ChatRoomMediator {
private:
    std::vector<User*> users;

public:
    void addUser(User* user) {
        users.push_back(user);
    }

    void sendMessage(const std::string& message, User* sender) override {
        for (auto user : users) {
            if (user != sender) {
                user->receiveMessage(message);
            }
        }
    }
};

// 具体同事类 ChatUser
class ChatUser : public User {
public:
    ChatUser(ChatRoomMediator* mediator, const std::string& name) : User(mediator, name) {}

    void sendMessage(const std::string& message) override {
        std::cout << getName() << " sends message: " << message << std::endl;
        mediator->sendMessage(message, this);
    }

    void receiveMessage(const std::string& message) override {
        std::cout << getName() << " receives message: " << message << std::endl;
    }
};

int main() {
    ChatRoom chatRoom;

    ChatUser user1(&chatRoom, "User1");
    ChatUser user2(&chatRoom, "User2");
    ChatUser user3(&chatRoom, "User3");

    chatRoom.addUser(&user1);
    chatRoom.addUser(&user2);
    chatRoom.addUser(&user3);

    user1.sendMessage("Hello, everyone!");
    user2.sendMessage("Hi, User1!");
    user3.sendMessage("Nice to meet you all!");

    return 0;
}
