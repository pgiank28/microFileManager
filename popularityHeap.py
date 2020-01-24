def rightchild(node):
    return 2*node + 2

def leftChild(node):
    return 2*node + 1

def parent(node):
    return (node-1)/2

def maxHeapify(lst,node):
    l = leftChild(node)
    r = rightchild(node)

    largest = node

    if(l<len(lst) and lst[l][1]>lst[node][1]):
        largest = l
    else:
        largest = node

    if(r<len(lst) and lst[r][1]>lst[node][1]):
        largest = r

    if largest != node :
        tmp = lst[largest]
        lst[largest] = lst[node]
        lst[node] = tmp
        return maxHeapify(lst,largest)

    return lst

def updateHeap(lst,node):
    val = lst[node][1]
    while val>lst[parent(node)][1]:
        tmp = lst[node]
        lst[node] = lst[parent(node)]
        lst[parent(node)] = tmp
        node = parent(node)
    return lst

def increasePopularity(pheap,dir):
    for k in range(len(pheap)):
        if pheap[k][0].path == dir.path:
            pheap[k] = (pheap[k][0],pheap[k][1]+1)
            break

    if k+1==len(pheap):
        pheap.append((dir,0))
    return pheap,k+1
