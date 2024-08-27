def reverseKGroup(head, k):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    while True:
        curr = prev.next
        count = 0
        for _ in range(k):
            if curr is None:
                break
            curr = curr.next
            count += 1
        if count < k:
            break
        next_head = curr
        prev.next = reverse(prev.next, count)
        prev = next_head
    return dummy.next

def reverse(head, count):
    prev = None
    curr = head
    for _ in range(count):
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev