#include "mate_solver.hpp"
int main(){
    string s;
    cout << "Enter Board:\n";
    getline(cin,s);
    Board board(s);
    if(is_mate(board,2)){
        printLine();
    }
    else {
        cout <<"No mate in 2 moves\n";
    }
    return 0;
}
