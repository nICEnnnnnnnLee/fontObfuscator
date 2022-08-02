from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools import subset
import random


"""
# 参考了https://github.com/solarhell/fontObfuscator
# 一个简单的使用示例
font = TTFont("华康方圆体W7-GB.ttc", fontNumber =0)
ob_font = ObfusedFont(font)
ob_font.obfuscate('测', '试') # 相当于 ob_font.obfuscateUnicode(ord('测'), ord('试'))
ob_font.obfuscate('试', '测')
ob_font.obfuscate('A', 'C')
# ob_font.save('test.ttf')
ob_font.save('test.ttf', xmlPath = "test.xml")
"""
class ObfusedFont:

    def __init__(self, font, meta=None):
        glyph_set = font.getGlyphSet()
        self.meta = meta
        self.origin = {
            'font': font,
            'cmap': font.getBestCmap(),
            'glyph_set': glyph_set,
            'pen': TTGlyphPen(glyph_set),
            'glyph_order': font.getGlyphOrder(),
        }
        self.obfused = {
            'glyphs' :{},
            'metrics' :{},
            'cmap' :{},
            'text' : [],
        }
        # 为新的font设置 null / notdef
        if 'null' in self.origin['glyph_order']:
            self.origin['glyph_set']['null'].draw(self.origin['pen'])
            self.obfused['glyphs']['null'] = self.origin['pen'].glyph()
            self.obfused['metrics']['null'] = self.origin['font']['hmtx']['null']
            self.obfused['text'] += ['null']
        if '.notdef' in self.origin['glyph_order']:
            self.origin['glyph_set']['.notdef'].draw(self.origin['pen'])
            self.obfused['glyphs']['.notdef'] = self.origin['pen'].glyph()
            self.obfused['metrics']['.notdef'] = self.origin['font']['hmtx']['.notdef']
            self.obfused['text'] += ['.notdef']

    def containsUnicode(self, unicode):
        return unicode in self.origin['cmap']

    def obfuscate(self, actualCharactor, displayCharactor):
        return self.obfuscateUnicode(ord(actualCharactor), ord(displayCharactor))

    def obfuscateUnicode(self, actualUnicode, displayUnicode):
        if displayUnicode in self.origin['cmap'] and actualUnicode in self.origin['cmap']:
            displayCmapName = self.origin['cmap'][displayUnicode]
            actualCmapName = self.origin['cmap'][actualUnicode]
            self.origin['glyph_set'][displayCmapName].draw(self.origin['pen'])
            self.obfused['glyphs'][actualCmapName] = self.origin['pen'].glyph()
            self.obfused['metrics'][actualCmapName] = self.origin['font']['hmtx'][displayCmapName]
            self.obfused['text'] += [actualCmapName]
            self.obfused['cmap'][actualUnicode] = actualCmapName
            return True
        else:
            return False
    
    def save(self, ttfPath, woffPath=None, woff2Path=None, xmlPath=None):
        horizontal_header = {
            'ascent': self.origin['font']['hhea'].ascent,
            'descent': self.origin['font']['hhea'].descent,
        }
        meta = self.meta if self.meta else {
            'familyName': 'ObfusedFont',
            'styleName': 'Regular',
            'psName': 'ObfusedFont-Regular',
            'copyright': 'Created by nICEnnnnnnnLee',
            'version': 'Version 1.0',
        }
        fb = FontBuilder(self.origin['font']['head'].unitsPerEm, isTTF=True)
        fb.setupGlyphOrder(self.obfused['text'])
        fb.setupCharacterMap(self.obfused['cmap'])
        fb.setupGlyf(self.obfused['glyphs'])
        fb.setupHorizontalMetrics(self.obfused['metrics'])
        fb.setupHorizontalHeader(**horizontal_header)
        fb.setupNameTable(meta)
        fb.setupOS2()
        fb.setupPost()
        fb.save(ttfPath)
        if woffPath or woff2Path:
            options = subset.Options()
            font = subset.load_font(ttfPath, options)
        if woffPath:
            options.flavor = 'woff'
            subset.save_font(font, woffPath, options)
        if woff2Path:
            options.flavor = 'woff2'
            subset.save_font(font, woff2Path, options)
        if xmlPath:
            font = TTFont(ttfPath, fontNumber = 0)
            font.saveXML(xmlPath)




def obfuscateSpecificList(unicodeList, font, ttfPath, woffPath=None, woff2Path=None, xmlPath=None):
    ob_font = ObfusedFont(font)
    # 将不在字体里面的unicode删除
    tmp_filter = filter(lambda unicode:ob_font.containsUnicode(unicode), unicodeList)
    origin_unicodes = list(tmp_filter)
    
    # 随机洗牌
    obfused_unicodes = origin_unicodes.copy()
    random.shuffle(obfused_unicodes)

    # 建立两个map，表示实际值和显示值的映射关系
    real_to_display, display_to_real = {}, {}
    for index in range(0, len(origin_unicodes)):
        unicode_origin = origin_unicodes[index]
        unicode_obfuse = obfused_unicodes[index]
        real_to_display[unicode_origin] = unicode_obfuse
        display_to_real[unicode_obfuse] = unicode_origin

        # 将unicode_origin 显示为 unicode_obfuse
        ob_font.obfuscateUnicode(unicode_origin, unicode_obfuse)
    ob_font.save(ttfPath, woffPath, woff2Path, xmlPath)
    font.close()
    return real_to_display, display_to_real

def obfuscateChinese(font, ttfPath, woffPath=None, woff2Path=None, xmlPath=None):
    # 中文字符集 \u4e00 - \u9fa5
    # 19968 40869
    ob_font = ObfusedFont(font)
    chinese_unicodes = range(19968, 40869 + 1)
    return obfuscateSpecificList(chinese_unicodes, font, ttfPath, woffPath, woff2Path, xmlPath)

if __name__=='__main__':
    font = TTFont("fonts/simhei.ttf", fontNumber =0)
    origin = '测试字体'
    unicodes = [ ord(x) for x in origin]
    real_to_display, display_to_real = obfuscateChinese(font, 'fonts/obfused-chinese.ttf')

    with open('dict_real_display.txt', mode = 'w', encoding = 'utf-8') as f:
        f.write('以下每行第一个字符为真实字符，第二个字符为显示字符\r\n')
        for key, value in real_to_display.items():
            f.write(chr(key))
            f.write(chr(value))
            f.write('\n')
    with open('dict_display_real.txt', mode = 'w', encoding = 'utf-8') as f:
        f.write('以下每行第一个字符为显示字符，第二个字符为真实字符\n')
        for key, value in real_to_display.items():
            f.write(chr(value))
            f.write(chr(key))
            f.write('\n')
    displays = ''.join([ chr(real_to_display[x]) for x in unicodes])
    reals =''.join([ chr(display_to_real[x]) for x in unicodes])
    print(f'{origin} 将显示为 {displays}')
    print(f'{reals} 将显示为 {origin}')

    """
    font = TTFont("fonts/simhei.ttf", fontNumber =0)
    origin = '测试字体ABCDefg123'
    unicodes = [ ord(x) for x in origin]
    real_to_display, display_to_real = obfuscateSpecificList(unicodes, font, 'fonts/obfused-specific.ttf')
    
    displays = ''.join([ chr(real_to_display[x]) for x in unicodes])
    reals =''.join([ chr(display_to_real[x]) for x in unicodes])
    print(f'{origin} 将显示为 {displays}')
    print(f'{reals} 将显示为 {origin}')
    """