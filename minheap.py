# Min Heap

def movedown(heap, spos, pos):
    newitem = heap[pos]
    while pos > spos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem

def moveup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    childpos = 2*pos + 1  
    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    heap[pos] = newitem
    movedown(heap, startpos, pos)

def push(heap, arrayval):
    heap.append(arrayval)
    movedown(heap, 0, len(heap)-1)

def pop(heap):
    lastitem = heap.pop()
    if heap:
        returnitem = heap[0]
        heap[0] = lastitem
        moveup(heap, 0)
        return returnitem
    return lastitem