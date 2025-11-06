def first_fit(allocator, size, process_id):
    for i, block in enumerate(allocator.memory):
        if block.status == 'free' and block.size >= size:
            allocator._split_block(i, size, process_id)
            return True
    return False

def next_fit(allocator, size, process_id):
    n = len(allocator.memory)
    for i in range(allocator.next_fit_pointer, n):
        if allocator.memory[i].status == 'free' and allocator.memory[i].size >= size:
            allocator._split_block(i, size, process_id)
            allocator.next_fit_pointer = (i + 1) % n
            return True
    for i in range(0, allocator.next_fit_pointer):
        if allocator.memory[i].status == 'free' and allocator.memory[i].size >= size:
            allocator._split_block(i, size, process_id)
            allocator.next_fit_pointer = (i + 1) % n
            return True
    return False

def best_fit(allocator, size, process_id):
    best_idx = -1
    best_size = float('inf')
    for i, block in enumerate(allocator.memory):
        if block.status == 'free' and block.size >= size and block.size < best_size:
            best_size = block.size
            best_idx = i
    if best_idx != -1:
        allocator._split_block(best_idx, size, process_id)
        return True
    return False

def worst_fit(allocator, size, process_id):
    worst_idx = -1
    worst_size = -1
    for i, block in enumerate(allocator.memory):
        if block.status == 'free' and block.size >= size and block.size > worst_size:
            worst_size = block.size
            worst_idx = i
    if worst_idx != -1:
        allocator._split_block(worst_idx, size, process_id)
        return True
    return False