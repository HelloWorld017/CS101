from cs1robots import *
from cs1media import *
from time import sleep

# You can change the target ".png" file for test here.
image = load_picture('images/test_1.png')

create_world(avenues=16, streets=16)
hubo = Robot(beepers=10000)

########################################
# --- Your code starts from here ---

# NenwAheui: Super simple Aheui implementation to use in CS101 Homework
# Warning: As this is created as fast I can, it might differ with official 'Aheui' specification
#          For example, stdio does not work

# Q: Why am I doing this thing?
# A: If I write code very differently from others, I wouldn't get suspected of copying someone else's code

# Letters
class Letters:
    def __init__(self):
        self.jaeum = {
            '': 0,
            'ㄱ': 2, 'ㄴ': 2, 'ㄷ': 3,
            'ㄹ': 5, 'ㅁ': 4, 'ㅂ': 4,
            'ㅅ': 2, 'ㅇ': None, 'ㅈ': 3,
            'ㅊ': 4, 'ㅋ': 3, 'ㅌ': 4,
            'ㅍ': 4, 'ㅎ': None,

            'ㄲ': 4, 'ㄳ': 4, 'ㄵ': 5, 'ㄶ': 5,
            'ㄺ': 7, 'ㄻ': 9, 'ㄼ': 9, 'ㄽ': 7,
            'ㄾ': 9, 'ㄿ': 9, 'ㅀ': 8, 'ㅄ': 6,
            'ㅆ': 4
        }

        self.moeum = {
            'ㅏ': (1, 0),
            'ㅑ': (2, 0),
            'ㅓ': (-1, 0),
            'ㅕ': (-2, 0),
            'ㅗ': (0, -1),
            'ㅛ': (0, -2),
            'ㅜ': (0, 1),
            'ㅠ': (0, 2),
            'ㅡ': None,
            'ㅣ': None,
            'ㅢ': None
        }

        self.choseong = [
            'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
            'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
            'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        ]

        self.jungseong = [
            'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ',
            'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ',
            'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
        ]

        self.jongseong = [
            '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
            'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
            'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
            'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        ]

    def teardown(self, char):
        char_id = ord(char) - 44032
        char_descriptor = {}
        char_descriptor['jongseong'] = self.jongseong[char_id % 28]

        chojung = char_id // 28
        char_descriptor['jungseong'] = self.jungseong[chojung % 21]
        char_descriptor['choseong'] = self.choseong[chojung // 21]

        return char_descriptor

    def combine(self, char_descriptor):
        return chr(
            (
                self.choseong.index(char_descriptor['choseong']) * 21 +
                self.jungseong.index(char_descriptor['jungseong'])
            ) * 28
            + self.jongseong.index(char_descriptor['jongseong'])
            + 44032
        )

letters = Letters()

# Storage Implementation
class Storage:
    def __init__(self, name):
        self.name = name

    def put(self, value):
        pass

    def get(self, value):
        pass


class StorageStack(Storage):
    def __init__(self, name):
        super().__init__(name)
        self.storage = []

    def put(self, value):
        self.storage.append(value)

    def get(self):
        return self.storage.pop()

    def to_list(self):
        return self.storage


class StorageQueue(Storage):
    def __init__(self, name):
        super().__init__(name)
        self.storage = []

    def put(self, value):
        self.storage.append(value)

    def get(self):
        return self.storage.pop()

    def to_list(self):
        return self.storage

# The 'ㅎ' Storage (a.k.a 통로)
class StorageTransit(Storage):
    def __init__(self):
        super().__init__('ㅎ')
        self.current = {
            'operation': None,
            'argcount': 0,
            'args': []
        }

        self.stdin_queue = []
        self.operations = {}
        self.callback = None

    def add_operation(self, op_id, operation, argcount = 0):
        self.operations[op_id] = {
            'handle': operation,
            'argcount': argcount
        }

    def operate(self, op_id, arguments = []):
        result = self.operations[op_id]['handle'](*arguments)

        if self.callback is not None:
            self.callback(op_id, arguments, result)

        self.stdin_queue = self.stdin_queue + result

    def put(self, b):
        if self.current['operation'] is not None:
            self.current['args'].append(b)

            if len(self.current['args']) >= self.current['argcount']:
                self.operate(self.current['operation'], self.current['args'])
                self.current['operation'] = None

            return

        if b in self.operations:
            if self.operations[b]['argcount'] == 0:
                self.operate(b)
                return

            self.current['operation'] = b
            self.current['argcount'] = self.operations[b]['argcount']
            self.current['args'] = []

    def get(self):
        if len(self.stdin_queue) <= 0:
            return 0

        return self.stdin_queue.pop(0)

    def to_list(self):
        return self.stdin_queue

# Interpreter
class Interpreter:
    def __init__(self, code, transit, debug=False):
        self.code = [[letters.teardown(ch) for ch in line] for line in code.splitlines()]
        self.height = len(self.code)

        self.x = 0
        self.y = 0
        self.velocity = [0, 0]

        self.memory = {}

        for letter in letters.jongseong:
            if letters.jaeum[letter] is not None:
                self.memory[letter] = StorageStack(letter)

        self.memory['ㅇ'] = StorageQueue('ㅇ')
        self.memory['ㅎ'] = transit

        self.memory_id = ''
        self.debug = debug

        if self.debug:
            transit.callback = lambda op_code, arguments, ret_val: \
                print("Call", op_code, arguments, ret_val)

    @property
    def width(self):
        return len(self.code[self.y])

    @property
    def cmem(self):
        return self.memory[self.memory_id]

    def move(self):
        (x, y) = self.velocity

        self.y = (self.y + self.height + y) % self.height
        self.x = (self.x + self.width + x) % self.width

    def interpret_char(self):
        char_descriptor = self.code[self.y][self.x]

        if self.debug:
            print(letters.combine(char_descriptor))

        # Move handle
        jungseong = char_descriptor['jungseong']

        if jungseong == 'ㅣ':
            if self.velocity[0] != 0:
                self.velocity[0] *= -1

        elif jungseong == 'ㅡ':
            if self.velocity[1] != 0:
                self.velocity[1] *= -1

        elif jungseong == 'ㅢ':
            self.velocity[0] *= -1
            self.velocity[1] *= -1

        else:
            self.velocity = list(letters.moeum[char_descriptor['jungseong']])

        # Operation Handle
        choseong = char_descriptor['choseong']
        jongseong = char_descriptor['jongseong']

        if choseong == 'ㅎ':
            return False

        elif choseong == 'ㄷ':
            self.cmem.put(self.cmem.get() + self.cmem.get())

        elif choseong == 'ㄸ':
            self.cmem.put(self.cmem.get() * self.cmem.get())

        elif choseong == 'ㅌ':
            c1 = self.cmem.get()
            self.cmem.put(self.cmem.get() - c1)

        elif choseong == 'ㄴ':
            c1 = self.cmem.get()
            self.cmem.put(self.cmem.get() // c1)

        elif choseong == 'ㄹ':
            c1 = self.cmem.get()
            self.cmem.put(self.cmem.get() % c1)

        elif choseong == 'ㅁ':
            self.cmem.get()

        elif choseong == 'ㅂ':
            jongseong_value = letters.jaeum[jongseong]

            if jongseong_value is not None:
                self.cmem.put(jongseong_value)

        elif choseong == 'ㅃ':
            c = self.cmem.get()
            self.cmem.put(c)
            self.cmem.put(c)

        elif choseong == 'ㅍ':
            c1 = self.cmem.get()
            c2 = self.cmem.get()
            self.cmem.put(c1)
            self.cmem.put(c2)

        elif choseong == 'ㅅ':
            self.memory_id = jongseong

        elif choseong == 'ㅆ':
            self.memory[jongseong].put(self.cmem.get())

        elif choseong == 'ㅈ':
            self.cmem.put(1 if self.cmem.get() <= self.cmem.get() else 0)

        elif choseong == 'ㅊ':
            if self.cmem.get() == 0:
                self.velocity[0] = self.velocity[0] * -1
                self.velocity[1] = self.velocity[1] * -1

        elif choseong == 'ㅉ':
            # Same as 'ㅇ', but it prints memory table. It has been added to debug
            if self.debug:
                for key in self.memory:
                    print((key + '*' if self.memory_id == key else key) + ':', self.memory[key].to_list())

        self.move()
        return True

transit = StorageTransit()

# Operation #0: Hubo Move
transit.add_operation(0, lambda: hubo.move() or [])

# Operation #1: Hubo Turn Left
transit.add_operation(1, lambda: hubo.turn_left() or [])

# Operation #2: Hubo Drop Beeper
transit.add_operation(2, lambda: hubo.drop_beeper() or [])

# Operation #3: Hubo Front Is Clear
transit.add_operation(3, lambda: [1 if hubo.front_is_clear() else 0])

# Operation #4: Get Pixel Brightness XY
brightness = lambda c: (c[0] + c[1] + c[2]) / 3
transit.add_operation(4, lambda x, y: [brightness(image.get(x, y))], 2)

# Operation #5: Get Size of Image
transit.add_operation(5, lambda: list(image.size()))

code = """
아삭바산바샇발쌀쌈야박야제야가야되야어야버야린야천야재우
아숙빠쑥타붇타야우차유반투빠쑿야우차순타두삽쑿받분쌋숫유
를빠솔삭포반토아아샵시볻빠뽀샇볻희오받본바쏳살뽀타토쀼어
요나는유쾌하오이런때숳연애까지가유쾌하오육신이분벋섯어유
흐느적흐느두터번벋석버적하도록피로했을때만정신타타뱌초쑣
요우이여은여화여처여럼여맑여소여니여코여버머석쎃쎃섭어우
틴숳삼뿌타붇샇쑫따뚜따누반슏이내횟배앓오는여뱃여속여으여
요붐쏳순솜분쏳숟봄푸복뿌솧텨터로스미면머릿속에으레백지가
준삭뽀빠쏨타토밣봃타봃아초받복비되는법이오그위에다나는위
요어트여와여파여라여독여머스를바둑포석처럼늘어놓소가공할
""".strip()

hubo_interpreter = Interpreter(code, transit, debug=False)
while hubo_interpreter.interpret_char():
    pass

# --- Your code ends here ---
########################################
