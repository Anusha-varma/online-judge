n = int(input())
m = int(input())
conflictingPairs = [tuple(map(int, input().split())) for _ in range(m)]

def count_valid_subarrays(n, conflicts):
    last_seen = [-1] * (n + 1)
    total = 0
    j = 0
    conflict_map = [[] for _ in range(n + 1)]
    for a, b in conflicts:
        conflict_map[a].append(b)
        conflict_map[b].append(a)
    for i in range(n):
        while j < n:
            valid = True
            for b in conflict_map[j + 1]:
                if last_seen[b] >= i:
                    valid = False
                    break
            if not valid:
                break
            last_seen[j + 1] = j
            j += 1
        total += (j - i)
        if last_seen[i + 1] == i:
            last_seen[i + 1] = -1
    return total

max_subarrays = 0
for i in range(len(conflictingPairs)):
    reduced = conflictingPairs[:i] + conflictingPairs[i + 1:]
    max_subarrays = max(max_subarrays, count_valid_subarrays(n, reduced))

print(max_subarrays)
