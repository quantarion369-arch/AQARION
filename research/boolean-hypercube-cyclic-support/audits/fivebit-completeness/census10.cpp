#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;
using i64 = int64_t;
constexpr i64 P = 2147483629LL;

using Row = array<i64,16>;

Row rows[32];

i64 power(i64 a, i64 e) {
    i64 r=1;
    while(e) {
        if(e&1) r=r*a%P;
        a=a*a%P;
        e>>=1;
    }
    return r;
}

void init() {
    for(int x=0;x<32;x++) {
        int b[5];
        for(int i=0;i<5;i++) b[i]=(x>>i)&1;
        rows[x][0]=1;
        for(int i=0;i<5;i++) rows[x][1+i]=b[i];
        int k=6;
        for(int i=0;i<5;i++)
            for(int j=i+1;j<5;j++)
                rows[x][k++]=b[i]*b[j];
    }
}

int rank_mod(int *s) {
    Row a[10];
    for(int i=0;i<10;i++) a[i]=rows[s[i]];
    int r=0;
    for(int c=0;c<16 && r<10;c++) {
        int p=r;
        while(p<10 && a[p][c]==0) p++;
        if(p==10) continue;
        swap(a[p],a[r]);
        i64 inv=power(a[r][c],P-2);
        for(int j=c;j<16;j++) a[r][j]=a[r][j]*inv%P;
        for(int i=0;i<10;i++) if(i!=r) {
            i64 f=a[i][c];
            if(f) for(int j=c;j<16;j++)
                a[i][j]=(a[i][j]-f*a[r][j]%P+P)%P;
        }
        r++;
    }
    return r;
}

int main(int argc,char**argv) {
    init();
    const string out = argc>1 ? argv[1] : "census10-progress.txt";
    ofstream log(out);
    if(!log) { cerr<<"Cannot open output\n"; return 2; }

    uint64_t total=0, deficient=0;
    int s[10];
    for(int i=0;i<10;i++) s[i]=i;

    while(true) {
        total++;
        if(rank_mod(s)<10) deficient++;

        if(total%1000000==0) {
            log<<total<<" "<<deficient<<"\n";
            log.flush();
            cerr<<"checked "<<total<<" deficient "<<deficient<<"\n";
        }

        int i=9;
        while(i>=0 && s[i]==32-10+i) i--;
        if(i<0) break;
        s[i]++;
        for(int j=i+1;j<10;j++) s[j]=s[j-1]+1;
    }

    log<<"FINAL "<<total<<" "<<deficient<<"\n";
    log.flush();
    cout<<"FINAL "<<total<<" "<<deficient<<"\n";
}
