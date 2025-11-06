import time
from algorithms import first_fit, next_fit, best_fit, worst_fit

class MemoryBlock:
    def __init__(self, start, size, status='free', process_id=None):
        self.start = start
        self.size = size
        self.status = status
        self.process_id = process_id

class Allocator:
    def __init__(self, total_memory):
        self.memory = [MemoryBlock(0, total_memory)]
        self.next_fit_pointer = 0
        self.alloc_algorithms = {
            'first_fit': first_fit,
            'next_fit': next_fit,
            'best_fit': best_fit,
            'worst_fit': worst_fit
        }

    def allocate(self, size, process_id, algorithm):
        if algorithm not in self.alloc_algorithms:
            raise ValueError("Invalid algorithm!")
        start_time = time.time()
        success = self.alloc_algorithms[algorithm](self, size, process_id)
        end_time = time.time()
        time_taken = end_time - start_time
        if success:
            print(f"Allocated {size} for process {process_id} ({algorithm}) - Time: {time_taken:.6f}s")
        else:
            print(f"Cannot allocate {size} for process {process_id} ({algorithm})")
        return success, time_taken

    def _split_block(self, i, size, process_id):
        block = self.memory[i]
        if block.size > size:
            new_free = MemoryBlock(block.start + size, block.size - size)
            self.memory.insert(i + 1, new_free)
            block.size = size
        block.status = 'allocated'
        block.process_id = process_id

    def deallocate(self, process_id):
        start_time = time.time()
        found = False
        for block in self.memory:
            if block.process_id == process_id and block.status == 'allocated':
                block.status = 'free'
                block.process_id = None
                found = True
                break
        if found:
            self._merge_free_blocks()
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Deallocated process {process_id} - Time: {time_taken:.6f}s")
            return True, time_taken
        print(f"Process {process_id} not found")
        return False, 0

    def _merge_free_blocks(self):
        i = 0
        while i < len(self.memory) - 1:
            if self.memory[i].status == 'free' and self.memory[i + 1].status == 'free':
                self.memory[i].size += self.memory[i + 1].size
                del self.memory[i + 1]
            else:
                i += 1

    def compact(self):
        new_memory = []
        current_start = 0
        for block in sorted(self.memory, key=lambda b: b.start if b.status == 'allocated' else float('inf')):
            if block.status == 'allocated':
                block.start = current_start
                new_memory.append(block)
                current_start += block.size
        total_memory = self.memory[0].size + sum(b.size for b in self.memory[1:])
        free_size = total_memory - current_start
        if free_size > 0:
            new_memory.append(MemoryBlock(current_start, free_size))
        self.memory = new_memory
        self.next_fit_pointer = 0
        print("Compaction performed")

    def get_memory_map(self):
        return [(b.start, b.size, b.status, b.process_id) for b in self.memory]