---
title: "द्विआधारी खोज"
date: 2024-12-24
draft: false
description: "द्विआधारी खोज एल्गोरिथ्म को सुरुचिपूर्ण ढंग से कैसे लागू करें।"
summary: "द्विआधारी खोज एल्गोरिथ्म को सुरुचिपूर्ण ढंग से कैसे लागू करें।"
tags: [ "एल्गोरिथम", "द्विआधारी खोज", "एल्गोरिथम टेम्पलेट" ]
categories: [ "एल्गोरिदम और डेटा संरचनाएं" ]
---

यदि एक क्रमबद्ध समाधान स्थान को दो भागों में विभाजित किया जाता है, जिनमें से एक भाग शर्त को संतुष्ट करता है, और दूसरा भाग नहीं करता है। तो द्विआधारी खोज का उपयोग क्रमबद्ध समाधान स्थान में महत्वपूर्ण बिंदु को खोजने के लिए किया जा सकता है।

द्विआधारी खोज का मूल विचार खोज अंतराल को लगातार आधा करना है। प्रत्येक जांच में मध्य तत्व की जाँच की जाती है। यदि मध्य तत्व शर्त को पूरा नहीं करता है, तो आधे अंतराल को समाप्त किया जा सकता है; अन्यथा, अन्य आधे अंतराल में खोज जारी रखी जाती है। चूंकि प्रत्येक बार खोज अंतराल का आधा भाग हटा दिया जाता है, इसलिए खोज की समय जटिलता $O(\log n)$ तक पहुँच सकती है।

## उदाहरण प्रश्न

**प्रश्न विवरण:**
एक आरोही क्रम में व्यवस्थित $n$ लंबाई की पूर्णांक सरणी दी गई है, और $q$ प्रश्न हैं। प्रत्येक प्रश्न एक पूर्णांक $k$ देता है, और हमें सरणी में $k$ के "प्रारंभिक स्थान" और "अंतिम स्थान" (अनुक्रमणिका 0 से शुरू) को खोजने की आवश्यकता है। यदि सरणी में यह संख्या मौजूद नहीं है, तो `-1 -1` लौटाएँ।

### इनपुट प्रारूप

1. पहली पंक्ति: दो पूर्णांक $n$ और $q$, जो क्रमशः सरणी की लंबाई और प्रश्नों की संख्या दर्शाते हैं।
2. दूसरी पंक्ति: $n$ पूर्णांक, जो पूर्ण सरणी को दर्शाते हैं, आरोही क्रम में व्यवस्थित हैं।
3. अगली $q$ पंक्तियाँ: प्रत्येक पंक्ति में एक पूर्णांक $k$ होता है, जो एक प्रश्न तत्व का प्रतिनिधित्व करता है।

## डेटा रेंज

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### आउटपुट प्रारूप

प्रत्येक प्रश्न के लिए, सरणी में तत्व का प्रारंभिक और अंतिम स्थान एक पंक्ति में आउटपुट करें। यदि सरणी में तत्व मौजूद नहीं है, तो `-1 -1` आउटपुट करें।

**उदाहरण:**

```
इनपुट:
6 3
1 2 2 3 3 4
3
4
5

आउटपुट:
3 4
5 5
-1 -1
```

**स्पष्टीकरण:**

- तत्व $3$ की सीमा $[3, 4]$ है;
- तत्व $4$ केवल एक बार, स्थान $5$ पर दिखाई देता है;
- तत्व $5$ सरणी में मौजूद नहीं है, इसलिए $-1$ $-1$ लौटाएँ।

---

## उत्तर

- **"प्रारंभिक स्थान" खोजना:**
  अर्थात, $k$ से पहले या उसके बराबर पहली स्थिति खोजें। सरणी को दो भागों में विभाजित किया जा सकता है:
    - बाईं ओर सभी संख्याएँ $k$ से "कम" हैं
    - दाईं ओर सभी संख्याएँ $k$ से "अधिक या उसके बराबर" हैं
    - उत्तर दाईं ओर का पहला स्थान है

- **"अंतिम स्थान" खोजना:**
  अर्थात, $k$ से कम या उसके बराबर अंतिम स्थिति खोजें। सरणी को दो भागों में विभाजित किया जा सकता है:
    - बाईं ओर सभी संख्याएँ $k$ से "कम या उसके बराबर" हैं
    - दाईं ओर सभी संख्याएँ $k$ से "अधिक" हैं
    - उत्तर बाईं ओर का अंतिम स्थान है

---

## अनुशंसित टेम्पलेट

नीचे एक सुरुचिपूर्ण और त्रुटि-रहित द्विआधारी टेम्पलेट है। यह $l$ और $r$ को धीरे-धीरे एक-दूसरे के करीब लाकर सुनिश्चित करता है कि लूप दोनों के आसन्न होने पर समाप्त हो जाए:

दो पॉइंटर्स $l$ और $r$ को परिभाषित करें, जिनमें अपरिवर्तनीय हैं: बंद अंतराल $[0, l]$ सभी बाएं भाग से संबंधित हैं, और बंद अंतराल $[r, n - 1]$ सभी दाएं भाग से संबंधित हैं। $l$ और $r$ दोनों को $-1$ और $n$ पर प्रारंभ किया जाता है।

एल्गोरिथ्म समाप्त होने पर, $l$ और $r$ आसन्न होते हैं, क्रमशः बाएं भाग के अंतिम तत्व और दाएं भाग के पहले तत्व की ओर इशारा करते हैं।

क्योंकि वांछित समाधान मौजूद नहीं हो सकता है, इसलिए यदि प्रश्न में यह नहीं बताया गया है कि कोई समाधान निश्चित रूप से मौजूद है, तो हमें यह जांचने की आवश्यकता है कि क्या `l` या `r` सीमा से बाहर है, और क्या वह सही मान की ओर इशारा कर रहा है।

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

        // 1. k का प्रारंभिक स्थान खोजें
        //    सरणी को दो भागों में विभाजित करें, बाईं ओर सभी < k, दाईं ओर सभी >= k।
        //    उत्तर दाईं ओर का न्यूनतम सूचकांक है।
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // यदि r सीमा से बाहर है या nums[r] != k है, तो इसका मतलब है कि k मौजूद नहीं है
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. k का अंतिम स्थान खोजें
        //    सरणी को दो भागों में विभाजित करें, बाईं ओर सभी <= k, दाईं ओर सभी > k।
        //    उत्तर बाएं भाग का अधिकतम सूचकांक है।
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        int rightPos = l;
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### इस तरह क्यों लिखें

1. इस लेखन में अपरिवर्तनीयों की सख्त परिभाषा है।
2. यह "प्रारंभिक स्थान" और "अंतिम स्थान" दोनों स्थितियों को खोजने के लिए एक साथ लागू होता है, बिना किसी अतिरिक्त प्रसंस्करण और परिवर्तन की आवश्यकता के।
3. कुछ लेखन `l == r` का उपयोग समापन स्थिति के रूप में करते हैं। जब $l$ और $r$ में $1$ का अंतर होता है, तो यह $mid$ और $l$ या $r$ के बराबर की गणना करेगा। यदि सही ढंग से संसाधित नहीं किया गया, तो $l$ या $r$ को $mid$ के रूप में अपडेट करने पर, खोज अंतराल कम नहीं होगा, जिससे एक अनंत लूप हो सकता है। इसके विपरीत, यहां लिखने की शैली $l$ और $r$ के आसन्न होने पर समाप्त हो जाती है, यह सुनिश्चित करते हुए कि $mid$, $l$ से छोटा और $r$ से बड़ा है। $l$ या $r$ को अपडेट करते समय खोज अंतराल निश्चित रूप से कम हो जाएगा।

---

## STL

यदि C++ STL द्वारा प्रदान किए गए `lower_bound` और `upper_bound` फ़ंक्शंस का उपयोग करते हैं, तो वही काम पूरा किया जा सकता है:

- `lower_bound(first, last, val)` "val से पहले या उसके बराबर पहले स्थान" को लौटाएगा।
- `upper_bound(first, last, val)` "val से पहले स्थान" को लौटाएगा।

उदाहरण के लिए, मान लें कि `nums = {1,2,3,4,4,4,4,4,5,5,6}` है, और हम जानना चाहते हैं कि 4 किस सीमा में है:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 appears 0 times" << endl;
} else {
    cout << "first 4 is at " << it1 - nums.begin() << endl;
    cout << "last 4 is at " << it2 - nums.begin() - 1 << endl;
    cout << "4 appears " << it2 - it1 << " times" << endl;
}
```

- `it1` पहले मान को इंगित करता है जो $4$ से अधिक या उसके बराबर है।
- `it2` पहले मान को इंगित करता है जो $4$ से अधिक है।  
  इसलिए `it2 - it1` सरणी में $4$ की उपस्थिति की संख्या है; `it2 - nums.begin() - 1` $4$ की दाईं सीमा है।

---

## अतिरिक्त

द्विआधारी खोज को फ़्लोटिंग-पॉइंट संख्या श्रेणी (जैसे समीकरण के मूल की खोज) और त्रिकोणीय खोज को एकल-शिखर वाले फ़ंक्शन के चरम मान को खोजने के लिए भी बढ़ाया जा सकता है।
जब तक आप "**क्रमबद्ध अंतराल में, आप हर बार आधे भाग को बाहर निकाल सकते हैं**" के मूल सिद्धांत को समझते हैं, तो आप पाएंगे कि द्विआधारी खोज कई परिदृश्यों में समस्याओं को कुशलतापूर्वक हल करने में आपकी मदद कर सकती है।

---

## अभ्यास

LeetCode 33. Rotated Sorted Array में खोजें

संकेत: पहला चरण घुमाव बिंदु को खोजने के लिए द्विआधारी खोज का उपयोग करना है, और दूसरा चरण लक्ष्य मान को खोजने के लिए द्विआधारी खोज का उपयोग करना है।