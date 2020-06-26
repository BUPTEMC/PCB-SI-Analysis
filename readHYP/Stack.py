<<<<<<< HEAD

class Stack:

    def __init__(self):  # 初始化空栈
        self.items = []

    def isEmpty(self):  # 是否为空
        return self.items == []

    def push(self, item):  # 入栈
        self.items.append(item)

    def pop(self):  # 出栈
        return self.items.pop()

    def peek(self):  # 查看栈顶元素
        return self.items[len(self.items) - 1]

    def size(self):  # 查看栈的大小
        return len(self.items)

    def clear(self):  # 清空栈
        self.items = []

    # 当前对象的表现形式，此法给python解释器运行
    def __repr__(self):
        return 'Stack_' + str(self.items)

    # 当前对象的字符串表示，使用print()时会调用，此法给人阅读
    def __str__(self):
        return 'Stack_' + str(self.items)

=======

class Stack:

    def __init__(self):  # 初始化空栈
        self.items = []

    def isEmpty(self):  # 是否为空
        return self.items == []

    def push(self, item):  # 入栈
        self.items.append(item)

    def pop(self):  # 出栈
        return self.items.pop()

    def peek(self):  # 查看栈顶元素
        return self.items[len(self.items) - 1]

    def size(self):  # 查看栈的大小
        return len(self.items)

    def clear(self):  # 清空栈
        self.items = []

    # 当前对象的表现形式，此法给python解释器运行
    def __repr__(self):
        return 'Stack_' + str(self.items)

    # 当前对象的字符串表示，使用print()时会调用，此法给人阅读
    def __str__(self):
        return 'Stack_' + str(self.items)

>>>>>>> 43888ac89e41450472c750f6e8d67c4bfa5e6ee8
