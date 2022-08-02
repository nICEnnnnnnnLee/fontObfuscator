# fontObfuscator



### 使用示例
```
font = TTFont("fonts/simhei.ttf", fontNumber =0)
ob_font = ObfusedFont(font)
ob_font.obfuscate('测', '试') # 相当于 ob_font.obfuscateUnicode(ord('测'), ord('试'))
ob_font.obfuscate('试', '测')
ob_font.obfuscate('A', 'C')
ob_font.save('test.ttf', xmlPath = "test.xml")
```

### 演示
<http://nicennnnnnnlee.github.io/sources/obfuscate-font/>


### Tips
`obfuscate.py`也包装了一下常见的应用实现，具体请参看`if __name__=='__main__':`后面内容

