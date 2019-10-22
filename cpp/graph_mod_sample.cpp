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

template <typename T>
class Graph {
   private:
    int size;

   public:
    struct Edge {
        int from;
        int to;
        T cost;
    };

    vector<Edge> edges;
    vector<vector<int>> graph;

    Graph(int n) : size(n), graph(n) {}
    void add(int from, int to, T cost = T()) {
        assert(0 <= from && from < size && 0 <= to && to < size);
        int id = edges.size();
        graph[from].push_back(id);
        edges.push_back({from, to, cost});
    }
    Graph reverse() const {
        Graph g(size);
        for (auto& edge : edges) {
            g.add(edge.to, edge.from, edge.cost);
        }
        return g;
    }
    vector<int> scc(vector<vector<int>>& nodes) const {
        vector<int> low(size), order(size);
        stack<int> living;
        int idx = 0;
        vector<int> result(size, -1);
        int count = 0;
        nodes.clear();
        function<void(int)> dfs = [&](int node) {
            low[node] = order[node] = ++idx;
            living.push(node);
            for (int eid : graph[node]) {
                auto& edge = edges[eid];
                if (!order[edge.to]) {
                    dfs(edge.to);
                    low[node] = min(low[node], low[edge.to]);
                } else if (result[edge.to] == -1) {
                    low[node] = min(low[node], order[edge.to]);
                }
            }
            if (low[node] == order[node]) {
                nodes.push_back({});
                while (true) {
                    int x = living.top();
                    living.pop();
                    result[x] = count;
                    nodes.back().push_back(x);
                    if (x == node) break;
                }
                ++count;
            }
        };
        for (int i = 0; i < size; ++i) {
            if (result[i] == -1) {
                dfs(i);
            }
        }
        return result;
    }
};

template <typename T, T __v>
class Module {
   private:
    static const T _mod = __v;
    T _value;

   public:
    Module(T v = T()) : _value(v) { _value = ((_value % _mod) + _mod) % _mod; }
    T mod() const { return _mod; }
    T& value() { return _value; }
    const T& value() const { return _value; }
    Module& operator+=(const Module& a) {
        _value += a._value;
        if (_value >= _mod) {
            _value -= _mod;
        }
        return *this;
    }
    Module& operator-=(const Module& a) {
        _value -= a._value;
        if (_value < 0) {
            _value += _mod;
        }
        return *this;
    }
    template <typename U>
    Module& operator+=(const U& a) {
        return *this += Module(a);
    }
    template <typename U>
    Module& operator-=(const U& a) {
        return *this -= Module(a);
    }
    Module operator*(const Module& a) { return Module(_value * a._value); }

    template <typename U>
    Module operator*(const U& a) {
        return *this * Module(a);
    }
};

template <typename T, T __v>
ostream& operator<<(ostream& os, const Module<T, __v>& a) {
    return os << a.value();
}

const ll MOD = 1e9 + 7;
using Modl = Module<ll, MOD>;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int tests;
    std::cin >> tests;
    for (int test = 0; test < tests; ++test) {
        std::cout << "Case #" << test + 1 << ": ";
    }
}