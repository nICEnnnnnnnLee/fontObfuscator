# fontObfuscator



### ʹ��ʾ��
```
font = TTFont("fonts/simhei.ttf", fontNumber =0)
ob_font = ObfusedFont(font)
ob_font.obfuscate('��', '��') # �൱�� ob_font.obfuscateUnicode(ord('��'), ord('��'))
ob_font.obfuscate('��', '��')
ob_font.obfuscate('A', 'C')
ob_font.save('test.ttf', xmlPath = "test.xml")
```

### ��ʾ
<http://nicennnnnnnlee.github.io/sources/obfuscate-font/>


### Tips
`obfuscate.py`Ҳ��װ��һ�³�����Ӧ��ʵ�֣�������ο�`if __name__=='__main__':`��������

