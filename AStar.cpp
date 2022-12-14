/**************erik****************/
#include "bits-stdc++.h"
#include <cstdio>
#include <iostream>
#include <algorithm>
using namespace std;
typedef long long ll;
typedef unsigned long long int ull;
typedef pair<int,int> Pair;
typedef pair<double, pair<int,int>> pPair;
#define maxm(a,b,c)  max(a,max(c,b))
#define minm(a,b,c)  min(a,min(c,b))
#define f(i,n)  for(ll i=0;i<n;i++)
#define rf(i,n) for(ll i=n-1;i>=0;i--)
#define ROW 50
#define COL 50
#define inf 1e9
struct cell {
    int parent_i, parent_j;
    double f,g,h;
};
bool isUnblocked() {

}
bool isDestination() {
    
}
void calculateH(int x, int y, Pair dest) { //manhattan distance
    return abs(x - dest.first) + abs(y - dest.second);
}
void astar() { // add parameters here
    bool closed[ROW][COL];
    memset(closed, false, sizeof(closed));

    cell cellDetails[ROW][COL];
    for(int i=0;i<ROW;i++) {
        for(int j=0;j<COL;j++) {
            cellDetails[i][j].parent_i = inf;
            cellDetails[i][j].parent_j = inf;
            cellDetails[i][j].f = -1;
            cellDetails[i][j].g = -1;
            cellDetails[i][j].h = -1;
        }
    }
    int x = src.first; int y = src.second;
    cellDetails[x][y].parent_i = x;
    cellDetails[x][y].parent_j = y;
    cellDetails[x][y].f = 0.0;
    cellDetails[x][y].g = 0.0;
    cellDetails[x][y].h = 0.0;

    set<pPair> open;
    open.insert({0.0, {ix, y}});

    vector<vector<int>> dis = {{0,1},{1,0},{-1,0},{0,-1}};

    while(!open.empty()) {
        pPair p = *open.begin();
        open.erase(open.begin());
        x = p.second.first;
        y = p.second.second;
        closed[x][y] = true;

        double gN, hN, fN;

        for(int i=0;i<4;i++) {
            x = x + dis[i][0];
            y = y + dis[i][0]; 
            if(x>=0 && x<ROW && y>=0 && y<COL) {
                if (isDestination(x,y,dest)) {
                    cellDetails[x][y].parent_i = i;
                    cellDetails[x][y].parent_j = j;
                    // trace the path -->
                    traceIt(cellDetails, dest);
                    foundDest = true;
                    return;
                } 
                
                else if(!closed[x][y] && isUnblocked(grid, x, y)) {
                    gN = cellDetails[x][y].g + 1.0;
                    hN = calculateH(x,y,dest);
                    fN = gN + hN;

                    if(cellDetails[x][y].f == inf || cellDetails[x][y].f > fN) {
                        open.insert({fN, {x, y}});

                        cellDetails[x][y].parent_i = x;
                        cellDetails[x][y].parent_j = y;
                        cellDetails[x][y].f = fN;
                        cellDetails[x][y].g = gN;
                        cellDetails[x][y].h = hN;
                    }
                }
            }
        }
    }
    if(!foundDest) {
        cout<<"No Destination present";
    }
    return;
}
int main()
{
    
}