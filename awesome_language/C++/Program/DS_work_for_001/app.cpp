#include "ClothesOrder.h"
#include "List.h"
#include "Sort.h"
#include "Stack.h"
#include <iostream>
#include <ostream>
#include <utility>
#include <vector>

void menuMsg()
{
  std::cout << "====================================" << std::endl;
  std::cout << "< Clothing Order Management System >" << std::endl;
  std::cout << "====================================" << std::endl;
  std::cout << "Enter the corresponding key for functionality:" << std::endl;
  std::cout << "1: View existing clothing order list" << std::endl;
  std::cout << "2: Add a new order" << std::endl;
  std::cout << "3: Modify a specific order" << std::endl;
  std::cout << "4: Delete a specific order" << std::endl;
  std::cout << "5: Search for a specific order" << std::endl;
  std::cout << "6: View order list in ascending order of price" << std::endl;
  std::cout << "7: View order list in descending order of price" << std::endl;
  std::cout << "0: Exit the Clothing Order System" << std::endl;
  std::cout << "======================" << std::endl;
}

int initOrderList(LinkedList<ClothesOrder> *&list)
{
  ClothesOrder order1(1, "Nike", "Lisa", "2022-3-3", 1000);
  ClothesOrder order2(2, "adidas", "Jack", "2021-2-1", 777);
  ClothesOrder order3(3, "CONVERSE", "Tom", "2021-1-3", 469);
  ClothesOrder order4(4, "Anta", "Lucy", "2022-4-3", 339);
  ClothesOrder order5(5, "LiNing", "Lucas", "2022-4-3", 500);
  ClothesOrder order6(6, "puma", "Bob", "2022-4-3", 590);
  list->append(order1);
  list->append(order2);
  list->append(order3);
  list->append(order4);
  list->append(order5);
  list->append(order6);
  ClothesOrder::orderCount = 6;
  return 0;
}

int showListAsc(LinkedList<ClothesOrder> *&list)
{
  std::vector<ClothesOrder> order_arr;
  std::vector<std::pair<int, int>> price_arr;
  for (auto &temp : list->forEach(order_arr))
  {
    price_arr.push_back(std::make_pair(temp.getId(), temp.getPrice()));
    std::cout << temp << std::endl;
  }
  quickSort(price_arr, 0, price_arr.size() - 1);
  for (auto num : price_arr)
  {
    std::cout << list->find(ClothesOrder(num.first))->data;
  }

  return 0;
}

int showListDesc(LinkedList<ClothesOrder> *&list)
{
  std::vector<ClothesOrder> order_arr;
  std::vector<std::pair<int, int>> price_arr;
  for (auto &temp : list->forEach(order_arr))
  {
    price_arr.push_back(std::make_pair(temp.getId(), temp.getPrice()));
    std::cout << temp << std::endl;
  }
  bubbleSort(price_arr);
  for (auto num : price_arr)
  {
    std::cout << list->find(ClothesOrder(num.first))->data;
  }
  return 0;
}

int appFunction(LinkedList<ClothesOrder> *&list)
{
  initOrderList(list);
  menuMsg();
  int menuChoose;
  do
  {
    std::cin >> menuChoose;
    switch (menuChoose)
    {
    case 0:
      std::cout << "正在退出服装管理系统..." << std::endl;
      break;
    case 1:
      list->print();
      break;
    case 2:
      insertOrder(list);
      break;
    case 3:
      ModifyOrder(list);
      break;
    case 4:
      deleteOrder(list);
      break;
    case 5:
      searchOrder(list);
      break;
    case 6:
      showListAsc(list);
      break;
    case 7:
      showListDesc(list);
      break;
    default:
      std::cout << "错误参数请重新输入..." << std::endl;
    }
    std::cout << "============================" << std::endl;
  } while (menuChoose);
  return 0;
}
