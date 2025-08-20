#include "app.h"
#include "ClothesOrder.h"
#include "List.h"
#include "Stack.h"
#include "Sort.h"
#include <iostream>
#include <list>
#include <utility>
#include <vector>

using namespace std;

int main()
{
  LinkedList<ClothesOrder> *list = new LinkedList<ClothesOrder>;
  appFunction(list);
}