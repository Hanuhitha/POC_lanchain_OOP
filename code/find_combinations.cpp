
#include <iostream>
#include <vector>
#include <algorithm>

std::vector<std::vector<int>> combinationSum(std::vector<int>& candidates, int target) {
    std::sort(candidates.begin(), candidates.end());
    std::vector<std::vector<int>> result;
    findCombinations(candidates, target, 0, std::vector<int>(), &result);
    return result;
}

void findCombinations(const std::vector<int>& candidates, int target, int start, std::vector<int> current, std::vector<std::vector<int>>& result) {
    if (target < 0) {
        return;
    }
    if (target == 0) {
        result.push_back(current);
        return;
    }
    for (int i = start; i < candidates.size(); ++i) {
        int num = candidates[i];
        if (num > target) {
            break;
        }
        findCombinations(candidates, target - num, i + 1, current.push_back(num), &result);
    }
}

int main() {
    std::vector<int> candidates = {2,3,6,7};
    int target = 7;
    std::vector<std::vector<int>> result = combinationSum(candidates, target);
    for (const auto& combination : result) {
        std::cout << 