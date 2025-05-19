from collections import deque

class TodoQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, task):
        self.queue.append(task)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        return None

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def get_all_tasks(self):
        return list(self.queue)
