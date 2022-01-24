class mokey:

    def __init__(self, key):

        self.upkey(key)        
        self.DEBUG = False
    
    def upkey(self, key):

        self.key = key
        self.key_len = len(key)
        self.keypub = 0x00
        for k in self.key: self.keypub ^= ord(k) # 计算 pub 用于产生大不一样的结果

    def enkey(self, content):

        # control => [预置] [预置] [前补零] [两位内容]

        pub = 0x00
        result = ''
        word_index = 0

        for word in content: pub ^= ord(word) # 计算 pub 用于产生大不一样的结果
        for word in content:

            control = 0b0 # 控制参数, 暂时用来识别补0和中文
            this_word = ord(word) # 取数值
            key_index = word_index % self.key_len # 计算需要选用的key_index
            
            this_result = this_word ^ pub ^ ord(self.key[key_index]) ^ key_index ^ self.keypub # 加密算法

            if this_result > 0xFF: # 判断两位内容
                control |= 0b0001 # 两位的内容(一般为中文)
                byte_high = this_result >> 8 # 高位是否需要补0
                if byte_high <= 0xF: control |= 0b0010 # 写入控制位
            elif this_result <= 0xF: control |= 0b0010 # 写入控制位

            if self.DEBUG: print(
                '{}({})[{}][{}] => {}'.format(
                    chr(this_word), hex(this_word).replace('0x', ''),
                    hex(pub).replace('0x', ''), key_index,
                    hex(this_result).replace('0x', ''))
                )

            pub ^= this_result # 计算 pub
            result += '{}{}'.format(control, hex(this_result).replace('0x', '')) # 拼接结果
            
            word_index += 1
        
        return '{}{:>04}'.format(result, hex(pub).replace('0x', ''))
    
    def dekey(self, content):
        
        word_index = 0
        key_index = 0
        keys = []
        words = []
        result = ''
        pub = int(content[-4:], 16)
        content = content[:-4]

        while content:
            if not '0' <= content[0] <= '9': return ''

            control = int(content[0])

            if control & 0b0001: word_index = 4 if control & 0b0010 else 5
            else: word_index = 2 if control & 0b0010 else 3

            keys.append(len(words) % self.key_len)
            words.append(int(content[1:word_index], 16))
            content = content[word_index:]
        
        words = words[::-1]
        keys = keys[::-1]
        
        for word in words:
            pub ^= word
            this_word = word ^ pub ^ ord(self.key[keys[key_index]]) ^ keys[key_index] ^ self.keypub
            result += chr(this_word)
        
            key_index += 1
        return result[::-1]
