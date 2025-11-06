import argparse
from allocator import Allocator
from visualizer import visualize_memory
from utils import read_input_file, calculate_stats
from stats import save_stats

def main():
    parser = argparse.ArgumentParser(description="Memory Allocator Simulator")
    parser.add_argument('--algorithm', required=True, choices=['first_fit', 'next_fit', 'best_fit', 'worst_fit'])
    parser.add_argument('--input', required=False, help="Input file with commands")
    parser.add_argument('--total_memory', type=int, default=1024, help="Total memory size")
    parser.add_argument('--output', default='data/results', help="Output directory")
    parser.add_argument('--compact_threshold', type=float, default=50.0, help="Fragmentation threshold for auto compaction")
    args = parser.parse_args()

    allocator = Allocator(args.total_memory)
    step = 0
    total_time_alloc = 0
    total_time_dealloc = 0

    if args.input:
        commands = read_input_file(args.input)
        for cmd in commands:
            if cmd[0] == 'allocate':
                success, t = allocator.allocate(cmd[1], cmd[2], args.algorithm)
                if success:
                    total_time_alloc += t
            elif cmd[0] == 'deallocate':
                success, t = allocator.deallocate(cmd[1])
                if success:
                    total_time_dealloc += t
            elif cmd[0] == 'compact':
                allocator.compact()
            visualize_memory(allocator.get_memory_map(), args.algorithm, step, args.output)
            step += 1
            stats = calculate_stats(allocator)
            if stats['fragmentation'] > args.compact_threshold:
                print(f"Fragmentation exceeds threshold ({stats['fragmentation']:.2f}%), performing auto compaction...")
                allocator.compact()
                visualize_memory(allocator.get_memory_map(), args.algorithm, step, args.output)
                step += 1

    save_stats(allocator, args.algorithm, total_time_alloc, total_time_dealloc, args.output)
    stats = calculate_stats(allocator)
    print(f"Final stats: Total Free: {stats['total_free']}, Allocated: {stats['total_allocated']}, Fragmentation: {stats['fragmentation']:.2f}%")
    print(f"Total allocation time: {total_time_alloc:.6f}s, deallocation: {total_time_dealloc:.6f}s")

if __name__ == "__main__":
    main()