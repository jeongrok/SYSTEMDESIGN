class ListNode:
    def __init__(self, key = -1, val=-1, next=None) -> None:
        self.key = key
        self.val = val
        self.next = next



class MyHashMap:
    # assuming that our hashmap has a capacity of 1000 keys
    def __init__(self):
        self.map = [ListNode() for i in range(1000)]


    def hash(self, key):
        return key % len(self.map)

    def put(self, key:int, value:int) ->None:
        curr = self.map[self.hash(key)]
        while curr.next:
            if curr.next.key == key:
                curr.next.val = value        
                return
            curr = curr.next
        curr.next = ListNode(key, value)

    def get(self, key):
        curr = self.map[self.hash(key)].next # skipping the dummy Node
        while curr:
            if curr.key == key:
                return curr.val
            curr = curr.next
        return -1
    
    def remove(self, key):
        curr = self.map[self.hash(key)]
        while curr and curr.next:
            if curr.next.key == key:
                curr.next = curr.next.next
                return
            curr = curr.next