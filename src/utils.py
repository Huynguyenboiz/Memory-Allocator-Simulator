def read_input_file(file_path):
    commands = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 'allocate':
                commands.append(('allocate', int(parts[1]), parts[2]))
            elif parts[0] == 'deallocate':
                commands.append(('deallocate', parts[1]))
            elif parts[0] == 'compact':
                commands.append(('compact',))
    return commands

def calculate_stats(allocator):
    total_free = sum(b.size for b in allocator.memory if b.status == 'free')
    total_allocated = sum(b.size for b in allocator.memory if b.status == 'allocated')
    largest_free = max((b.size for b in allocator.memory if b.status == 'free'), default=0)
    frag = 0 if total_free == 0 else (1 - largest_free / total_free) * 100
    return {
        'total_free': total_free,
        'total_allocated': total_allocated,
        'fragmentation': frag
    }