# monkey_encryption
一个憨批的猴子加密, 不知道为什么可以修改一部分的密文但是原文不变???
### 使用方法
```python

mk = mokey(key) # 随意的字符串作为key, 理论上来说越长越好
mk.upkey(newkey) # 用来更新key值
mk.enkey(content) # 将content(字符串)传入用于加密
mk.dekey(encry_content) # 将加密的内容传入以求得原文

```
