
#include <utility>
#include <vector>
int partition(std::vector<std::pair<int, int>> &arr, int low, int high)
{
  int pivot = arr[high].second;
  int i = low - 1;

  for (int j = low; j <= high - 1; j++)
  {
    if (arr[j].second < pivot)
    {
      i++;
      std::swap(arr[i], arr[j]);
    }
  }

  std::swap(arr[i + 1], arr[high]);
  return i + 1;
}

void quickSort(std::vector<std::pair<int, int>> &arr, int low, int high)
{
  if (low < high)
  {
    int pi = partition(arr, low, high);

    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
  }
}

void bubbleSort(std::vector<std::pair<int, int>> &arr)
{
  int n = arr.size();

  for (int i = 0; i < n - 1; ++i)
  {
    for (int j = 0; j < n - i - 1; ++j)
    {
      if (arr[j].second < arr[j + 1].second)
      {
        std::swap(arr[j], arr[j + 1]);
      }
    }
  }
}

void insertionSort(int arr[], int n)
{
  for (int i = 1; i < n; i++)
  {
    int key = arr[i];
    int j = i - 1;

    // 移动元素，为当前元素找到合适的位置
    while (j >= 0 && arr[j] > key)
    {
      arr[j + 1] = arr[j];
      j--;
    }

    arr[j + 1] = key;
  }
}