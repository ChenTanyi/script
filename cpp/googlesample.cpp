#include <bits/stdc++.h>

#define DEBUG

#ifdef DEBUG
#define debug(...)                            \
    std::cerr << "LINE " << __LINE__ << ": "; \
    _dbg(#__VA_ARGS__, __VA_ARGS__)
#else
#define debug(...)
#endif

template <typename T>
void _dbg(const char* sdbg, T h) {
    std::cerr << sdbg << '=' << h << std::endl;
}
template <typename T, typename... Aargs>
void _dbg(const char* sdbg, T h, Aargs... a) {
    while (*sdbg != ',') std::cerr << *sdbg++;
    std::cerr << '=' << h << ',';
    _dbg(sdbg + 1, a...);
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& v) {
    os << "[";
    for (auto x : v) {
        os << x << ",";
    }
    return os << "]";
}

template <typename L, typename R>
std::ostream& operator<<(std::ostream& os, const std::pair<L, R>& p) {
    return os << "(" << p.first << "," << p.second << ")";
}

using namespace std;

typedef long long ll;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int tests;
    std::cin >> tests;
    for (int test = 0; test < tests; ++test) {
        std::cout << "Case #" << test + 1 << ": ";
    }
}