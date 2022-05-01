def lengthOfLIS(nums: 'List[int]') -> int:
    counter = [1 for _ in range(len(nums))]
    for i in range(1, len(nums)):
        j = i
        for j in range(i):
            if nums[j] < nums[i]:
                counter[i] = max(counter[j]+1, counter[i])
    return max(counter)
l = [10,9,2,5,3,7,101,18]
n = lengthOfLIS(l)
print(f"length of the longest increasing sub sequence: is {n} in {l}")