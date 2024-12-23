---
title: "이분 검색"
date: 2024-12-24
draft: false
description: "정수 이분 검색 알고리즘을 우아하게 구현하는 방법"
summary: "정수 이분 검색 알고리즘을 우아하게 구현하는 방법"
tags: [ "알고리즘", "이분 검색", "알고리즘 템플릿" ]
categories: [ "알고리즘 및 자료 구조" ]
---
{{< katex >}}

# 이분 검색

정렬된 시퀀스에서 특정 요소를 찾을 때, 이분 검색을 사용하여 빠르게 완료할 수 있습니다. 선형 검색의 시간 복잡도 $O(n)$에 비해, 이분 검색은 $O(\log n)$의 시간만 필요하므로 데이터 규모가 큰 경우 매우 효율적입니다.

## 이분 검색의 핵심 아이디어

이분 검색의 기본 아이디어는 검색 범위를 계속해서 반으로 나누는 것입니다. 매번 중간 요소와 목표 값의 크기를 비교하여, 중간 요소가 조건을 충족하지 않으면 한쪽 범위를 제외할 수 있습니다. 반대로, 다른 절반 범위에서 계속 검색합니다. 매번 검색 범위를 반으로 줄이기 때문에 검색 시간 복잡도는 $O(\log n)$에 도달할 수 있습니다.

"**가능한 해답을 정렬된 구간(조건 충족)과 다른 정렬된 구간(조건 불충족)으로 나눌 수 있는**" 문제에 대해 이분 검색은 매우 유용합니다. 예를 들어:

- 정렬된 배열에서 특정 요소의 존재 여부를 찾을 때
- 어떤 숫자가 나타나는 "첫 번째 위치" 또는 "마지막 위치"를 찾을 때

## 예제 문제: 요소의 시작 위치와 종료 위치 찾기

**문제 설명:**  
오름차순으로 정렬된 길이가 $n$인 정수 배열과 $q$개의 쿼리가 주어집니다. 각 쿼리는 정수 $k$를 제공하며, 배열에서 $k$의 "시작 위치"와 "종료 위치"(인덱스는 0부터 시작)를 찾아야 합니다. 배열에 해당 숫자가 없으면 $-1$ $-1$을 반환합니다.

**입력 형식:**

1. 첫 번째 줄: 배열 길이와 쿼리 횟수를 나타내는 두 정수 $n$과 $q$입니다.
2. 두 번째 줄: 전체 배열을 나타내는 $n$개의 정수(1 ~ 10000 범위)이며, 오름차순으로 정렬되어 있습니다.
3. 다음 $q$개의 줄: 각 줄에는 쿼리 요소를 나타내는 정수 $k$가 포함됩니다.

**출력 형식:**  
각 쿼리에 대해, 해당 요소가 배열에서 시작하고 끝나는 위치를 한 줄에 출력합니다. 배열에 해당 요소가 없으면 $-1$ $-1$을 출력합니다.

**예제:**

```
입력:
6 3
1 2 2 3 3 4
3
4
5

출력:
3 4
5 5
-1 -1
```

설명:

- 요소 3이 나타나는 범위는 `[3, 4]`입니다.
- 요소 4는 한 번만 나타나며, 위치 5에 있습니다.
- 요소 5는 배열에 존재하지 않으므로 `-1 -1`을 반환합니다.

## 이분 검색 응용 아이디어

이 문제에서 특정 값의 "왼쪽 경계"와 "오른쪽 경계"를 찾기 위해 이분 검색에 의존할 수 있습니다. 핵심은 검색 범위를 어떻게 정의하고, 비교 결과에 따라 포인터를 어떻게 이동할지 이해하는 것입니다.

- **"왼쪽 경계" 찾기:**  
  즉, $k$보다 크거나 같은 첫 번째 위치를 찾습니다. 배열을 두 부분으로 나눌 수 있습니다:
    - 왼쪽의 모든 숫자는 $k$보다 "작습니다"
    - 오른쪽의 모든 숫자는 $k$보다 "크거나 같습니다"

- **"오른쪽 경계" 찾기:**  
  즉, $k$보다 작거나 같은 마지막 위치를 찾습니다. 배열을 두 부분으로 나눌 수 있습니다:
    - 왼쪽의 모든 숫자는 $k$보다 "작거나 같습니다"
    - 오른쪽의 모든 숫자는 $k$보다 "큽니다"

이 두 범위를 올바르게 유지할 수 있다면 이분 검색을 통해 빠르게 결과를 얻을 수 있습니다.

## 추천 템플릿: 데드락을 피하는 이분 검색 작성법

다음은 우아하고 오류가 발생하기 쉬운 이분 템플릿입니다. $l$과 $r$이 점진적으로 수렴하도록 하여, 두 값이 인접할 때 루프가 항상 종료되도록 보장합니다:

두 포인터 $l, r$을 정의하고, 불변량: 닫힌 구간 $[0, l]$은 왼쪽 부분에 속하고, 닫힌 구간 $[r, n - 1]$은 오른쪽 부분에 속합니다. $l$과 $r$은 모두 $-1$과 $n$으로 초기화됩니다.

알고리즘이 종료될 때, $l$과 $r$은 인접하며, 각각 왼쪽 부분의 최대값과 오른쪽 부분의 최소값을 가리킵니다.

우리가 원하는 해답이 존재하지 않을 수도 있으므로, $l$ 또는 $r$을 반환할 때, 해당하는 값이 우리가 원하는 값인지, 범위를 벗어나는지 확인해야 합니다. 예를 들어, $l$은 $\leq k$의 최대값을 나타내며, `l != -1 && nums[l] == k`를 확인해야 합니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, q;
    cin >> n >> q;
    vector<int> nums(n);
    for(int i = 0; i < n; i++) cin >> nums[i];

    while(q--) {
        int k;
        cin >> k;

        // 1. k의 시작 위치(왼쪽 경계) 찾기
        //    배열을 두 부분으로 나누어 왼쪽은 < k, 오른쪽은 >= k
        //    왼쪽 경계는 오른쪽 부분의 최소 인덱스입니다.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // r이 범위를 벗어나거나 nums[r] != k이면 k가 존재하지 않음
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r; // k의 왼쪽 경계 기록

        // 2. k의 종료 위치(오른쪽 경계) 찾기
        //    배열을 두 부분으로 나누어 왼쪽은 <= k, 오른쪽은 > k
        //    오른쪽 경계는 왼쪽 부분의 최대 인덱스입니다.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // k가 존재하는지 이미 확인했으므로 여기에서 다시 확인할 필요 없음
        int rightPos = l; // 오른쪽 경계
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### 이렇게 작성하면 오류가 발생하기 어려운 이유는 무엇일까요?

1. 이 작성법은 엄격하게 정의된 불변량을 갖습니다.
2. 왼쪽 경계와 오른쪽 경계를 모두 찾을 수 있으므로 모든 시나리오에 적용할 수 있습니다.
3. 일부 작성법에서는 $l == r$을 종료 조건으로 사용합니다. $l$과 $r$이 1만큼 차이날 때 $mid$가 `l` 또는 `r`과 같게 계산됩니다. 올바르게 처리하지 않으면 `l` 또는 `r`을 `mid`로 업데이트하여 검색 범위가 줄어들지 않아 데드락이 발생할 수 있습니다. 반대로, 여기의 작성법은 $l$과 $r$이 인접할 때 종료되므로 이 문제를 피할 수 있습니다.

## STL 해법: `lower_bound` 및 `upper_bound`

C++ STL에서 제공하는 `lower_bound` 및 `upper_bound` 함수를 사용하면 같은 작업을 쉽게 완료할 수 있습니다:

- `lower_bound(first, last, val)`은 "val보다 크거나 같은 첫 번째 위치"를 반환합니다.
- `upper_bound(first, last, val)`은 "val보다 큰 첫 번째 위치"를 반환합니다.

예를 들어, `nums = {1,2,3,4,4,4,4,4,5,5,6}`이라고 가정하고 4가 나타나는 구간을 알고 싶다면 다음과 같습니다:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // 배열에 4가 존재하지 않음을 나타냄
    cout << "4 appears 0 times" << endl;
} else {
    cout << "first 4 is at " << it1 - nums.begin() << endl;
    cout << "last 4 is at " << it2 - nums.begin() - 1 << endl;
    cout << "4 appears " << it2 - it1 << " times" << endl;
}
```

- `it1`은 값 4보다 크거나 같은 첫 번째 위치를 가리킵니다.
- `it2`는 값 4보다 큰 첫 번째 위치를 가리킵니다.  
  따라서 `it2 - it1`은 배열에서 4가 나타나는 횟수이고, `it2 - nums.begin() - 1`은 4의 오른쪽 경계입니다.

이 두 함수는 구간을 찾거나 나타나는 횟수를 통계할 때 특히 편리합니다.

## 추가 사항

이분 검색은 부동 소수점 범위 검색(예: 방정식 근 구하기)과 단봉 함수의 최댓값을 찾는 삼분 검색으로 확장될 수도 있습니다. "정렬된 구간에서 매번 절반을 제외할 수 있다"는 핵심 원리를 이해하면 이분 검색이 많은 시나리오에서 문제를 효율적으로 해결하는 데 도움이 된다는 것을 알게 될 것입니다.

## 과제

LeetCode 33. Search in Rotated Sorted Array

힌트: 첫 번째 단계에서 이분 검색을 사용하여 회전점을 찾고, 두 번째 단계에서 이분 검색을 사용하여 목표 값을 찾습니다.