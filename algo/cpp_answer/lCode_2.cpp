#include <iostream>
#include <list>
using namespace std;

struct ListNode {
  int val;
  ListNode *next;
  ListNode() : val(0), next(nullptr) {}
  ListNode(int x) : val(x), next(nullptr) {}
  ListNode(int x, ListNode *next) : val(x), next(next) {}
};

namespace lCode {
auto addTwoNumbers(ListNode *l1, ListNode *l2) {
  auto res = new ListNode(0);
  auto temp = res;
  auto carry = 0;
  auto sum = carry;
  while (l1 || l2 || carry) {
    if (l1) {
      sum += l1->val;
      l1 = l1->next;
    }
    if (l2) {
      sum += l2->val;
      l2 = l2->next;
    }
    temp->next = (carry + (sum % 10)) == 10 ? new ListNode(0)
                                            : new ListNode(carry + (sum % 10));
    carry = (carry + (sum % 10) == 10) ? (sum / 10) + 1 : sum / 10;
    sum = 0;
    temp = temp->next;
  }
  return res->next;
}
} // namespace lCode

int main() {}