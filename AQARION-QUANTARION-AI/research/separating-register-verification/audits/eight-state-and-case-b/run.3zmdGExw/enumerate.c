
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint8_t cm[37];
    int nc = 0;

    cm[nc++] = 0;

    for (int i = 0; i < 8; i++)
        cm[nc++] = 1u << i;

    for (int i = 0; i < 8; i++)
        for (int j = i + 1; j < 8; j++)
            cm[nc++] = (1u << i) | (1u << j);

    unsigned separating_count = 0;
    unsigned deficient_count = 0;

    FILE *f = fopen("cand.txt", "w");

    if (!f) {
        perror("cand.txt");
        return 2;
    }

    for (uint32_t code = 0; code < 16777216u; code++) {
        if ((code & 1048575u) == 0) {
            printf("C_PROGRESS=%u/16777216\n", code);
            fflush(stdout);
        }

        uint32_t z = code;
        int T[8];

        for (int i = 0; i < 8; i++) {
            T[i] = z & 7u;
            z >>= 3;
        }

        uint8_t words[8];
        int separating = 1;

        for (int s = 0; s < 8; s++) {
            int x = s;
            uint8_t word = 0;

            for (int t = 0; t < 8; t++) {
                if (x >= 4)
                    word |= 1u << t;

                x = T[x];
            }

            words[s] = word;
        }

        for (int a = 0; a < 8 && separating; a++)
            for (int b = a + 1; b < 8; b++)
                if (words[a] == words[b]) {
                    separating = 0;
                    break;
                }

        if (!separating)
            continue;

        separating_count++;

        uint64_t basis[37] = {0};
        int rank = 0;

        for (int s = 0; s < 8; s++) {
            uint64_t vector = 0;

            for (int c = 0; c < 37; c++)
                if ((words[s] & cm[c]) == cm[c])
                    vector |= 1ULL << c;

            while (vector) {
                int pivot = 63 - __builtin_clzll(vector);

                if (basis[pivot]) {
                    vector ^= basis[pivot];
                } else {
                    basis[pivot] = vector;
                    rank++;
                    break;
                }
            }
        }

        if (rank < 8) {
            deficient_count++;

            if (fprintf(f, "%u\n", code) < 0) {
                fclose(f);
                return 3;
            }
        }
    }

    if (fclose(f))
        return 4;

    printf("MAPS_ENUMERATED=16777216\n");
    printf("SEPARATING_MAPS=%u\n", separating_count);
    printf("F2_DEGREE2_DEFICIENT=%u\n", deficient_count);

    return 0;
}
