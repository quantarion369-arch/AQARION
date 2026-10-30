#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

using u64 = uint64_t;
using u128 = __uint128_t;

constexpr u64 P = 2147483629ULL;
constexpr int N = 32, K = 10, C = 16;
constexpr u64 START = 61000000ULL;
constexpr u64 INITIAL_DEFICIENT = 64780ULL;
constexpr u64 TOTAL = 64512240ULL;

int feature[N][C];

u64 mulmod(u64 a, u64 b) {
    return (u128(a) * b) % P;
}
u64 power(u64 a, u64 e) {
    u64 r = 1;
    while (e) {
        if (e & 1) r = mulmod(r, a);
        a = mulmod(a, a);
        e >>= 1;
    }
    return r;
}
u64 choose(int n, int k) {
    if (k < 0 || k > n) return 0;
    u64 r = 1;
    for (int i = 1; i <= k; ++i)
        r = r * (n - k + i) / i;
    return r;
}

// Unrank the zero-based lexicographic combination index.
array<int,K> unrank_combination(u64 index) {
    array<int,K> s{};
    int previous = -1;
    for (int i = 0; i < K; ++i) {
        for (int v = previous + 1; v <= N - (K-i); ++v) {
            u64 block = choose(N-v-1, K-i-1);
            if (index < block) {
                s[i] = v;
                previous = v;
                break;
            }
            index -= block;
        }
    }
    if (index != 0) {
        cerr << "Combination unranking failed\n";
        exit(2);
    }
    return s;
}

int rank_mod(const array<int,K>& s) {
    u64 a[K][C];
    for (int i = 0; i < K; ++i)
        for (int j = 0; j < C; ++j)
            a[i][j] = feature[s[i]][j];

    int rank = 0;
    for (int col = 0; col < C && rank < K; ++col) {
        int pivot = rank;
        while (pivot < K && a[pivot][col] == 0) ++pivot;
        if (pivot == K) continue;

        if (pivot != rank)
            for (int j = 0; j < C; ++j)
                swap(a[pivot][j], a[rank][j]);

        u64 inv = power(a[rank][col], P-2);
        for (int j = col; j < C; ++j)
            a[rank][j] = mulmod(a[rank][j], inv);

        for (int i = rank+1; i < K; ++i) {
            u64 factor = a[i][col];
            if (!factor) continue;
            for (int j = col; j < C; ++j) {
                u64 sub = mulmod(factor, a[rank][j]);
                a[i][j] = (a[i][j] + P - sub) % P;
            }
        }
        ++rank;
    }
    return rank;
}

bool next_combination(array<int,K>& s) {
    for (int i = K-1; i >= 0; --i) {
        if (s[i] < N-K+i) {
            ++s[i];
            for (int j = i+1; j < K; ++j)
                s[j] = s[j-1]+1;
            return true;
        }
    }
    return false;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        cerr << "Usage: census10-resume PROGRESS_FILE\n";
        return 2;
    }

    // Same feature convention: constant, linear, then quadratic monomials.
    for (int h = 0; h < N; ++h) {
        int b[5];
        for (int i = 0; i < 5; ++i) b[i] = (h >> (4-i)) & 1;
        int c = 0;
        feature[h][c++] = 1;
        for (int i = 0; i < 5; ++i) feature[h][c++] = b[i];
        for (int i = 0; i < 5; ++i)
            for (int j = i+1; j < 5; ++j)
                feature[h][c++] = b[i]*b[j];
    }

    ofstream progress(argv[1], ios::app);
    if (!progress) {
        cerr << "Cannot open progress file\n";
        return 2;
    }

    auto s = unrank_combination(START);
    u64 checked = START;
    u64 deficient = INITIAL_DEFICIENT;

    cout << "RESUMING checked=" << checked
         << " deficient=" << deficient << "\n" << flush;

    do {
        if (rank_mod(s) < K) ++deficient;
        ++checked;

        if (checked % 1000000ULL == 0) {
            progress << checked << " " << deficient << "\n";
            progress.flush();
            cout << "checked " << checked
                 << " deficient " << deficient << "\n" << flush;
        }
    } while (checked < TOTAL && next_combination(s));

    if (checked != TOTAL) {
        cerr << "ERROR: enumeration ended at " << checked
             << " rather than " << TOTAL << "\n";
        return 3;
    }

    progress << "FINAL " << checked << " " << deficient << "\n";
    progress.flush();
    cout << "FINAL " << checked << " " << deficient << "\n" << flush;
    return 0;
}
