#include <iostream>
#include <map>
#include <string>
#include <vector>

class LowerBuilding {
public:
  void add_part(std::string part) { parts.push_back(part); }

  void catParts() {
    for (auto& part :parts) {
      std::cout<<part<<" ";
    }
  }

private:
  std::vector<std::string> parts;
};

class HighBuilding {
public:
  void add_part(std::string partF,std::string partS) { parts[partF]=partS;}

  void catParts() {
    for (auto& part :parts) {
      std::cout<<part.first<<":"<<part.second<<std::endl;
    }
  }

private:
  std::map<std::string,std::string> parts;
};

// 两个基本产品(低水平建筑,高水平建筑)
// 产品类不提供生产方法将其代理到生成器

// 生成器基类(abstract)-> 两个派生类
class BuildingGenerator {
public:
  virtual void reset() = 0;
  virtual void buildFoundation() = 0;
  virtual void buildFitment() = 0;
  virtual void buildUpdate()=0;
};

class BuildHigh :public BuildingGenerator{
public:
  BuildHigh() {
    reset();
  }
  void reset() override {
    building=new HighBuilding;
  }

  void buildFoundation() override {
    building->add_part("地基","宇宙无敌钛合金地基");
  }
  void buildFitment() override { building->add_part("装修", "宇宙无敌精装修"); }

  void buildUpdate() override {
    building->add_part("加装", "宇宙无敌升级精致加装");
  }

  HighBuilding* getBuilding() {
    auto temp = building;
    building = nullptr;
    return temp;
  }
  

private:
  HighBuilding* building=nullptr;
};

class BuildLow:public BuildingGenerator {
public:
  BuildLow() {
    reset();
  }
  void reset() override { building = new LowerBuilding; }
  void buildFoundation() override { building->add_part("基础地基"); }
  void buildFitment() override { building->add_part("基础建筑装修"); }
  void buildUpdate() override { building->add_part("升级版的基础加装"); }

   LowerBuilding* getBuilding() {
    auto temp = building;
    building = nullptr;
    return temp;
  }
  
  private :
      LowerBuilding * building=nullptr;
};

class Director {
public:
  
  void serGenerator(BuildingGenerator * generator) {
    buildingGenerator=generator;
  }
  void buildSimple() {
    buildingGenerator->buildFoundation();
  }
  void buildHigh() {
    buildSimple();
    buildingGenerator->buildFitment();
  }
  void buildUltra() {
    buildHigh();
    buildingGenerator->buildUpdate();
  }
private:
  BuildingGenerator *buildingGenerator=nullptr;
};

int main() {
  Director *director = new Director;
  BuildHigh *builder = new BuildHigh;
  director->serGenerator(builder);
  director->buildUltra();
  // std::cout<<"test"<<std::endl;
  auto result = builder->getBuilding();
  result->catParts();


  BuildLow *builder__=new BuildLow;
  director->serGenerator(builder__);
  director->buildHigh();
  auto res = builder__->getBuilding();
  res->catParts();

}
