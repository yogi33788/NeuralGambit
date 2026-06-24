#include<bits/stdc++.h>
#include"chess-library/include/chess.hpp"
using namespace std;
using namespace chess;
vector<Move> history;
const int inf=9999999;
const int checkmate=999999;

int negmax(Board& board,int depth,int alpha,int beta,vector<Move> &path,int no_of_moves=0){
    Movelist moves;
    movegen::legalmoves(moves,board);
    if(moves.size()==0){
        //Checkmate
        if(board.inCheck()){
            return -checkmate+no_of_moves;
        }
        //Stalemate
        return 0;
    }
    if(depth==0){
        return 0;
    }
    vector<Move> bestpath;
    for(int i=0;i<moves.size();i++){
        Move move=moves[i];
        vector<Move> childpath;
        board.makeMove(move);
        int score = -negmax(board,depth-1,-beta,-alpha,childpath,no_of_moves + 1);
        board.unmakeMove(move);
        if (score>alpha){
            alpha=score;
            bestpath.clear(); 
            bestpath.push_back(move);  // Current best move
            // Append continousion moves
            for (int j = 0; j < childpath.size(); j++) {
                bestpath.push_back(childpath[j]);
            }
        }
        // prune
        if(alpha>=beta){
            break;
        }
    }
    path=bestpath;
    return alpha;
}

bool is_mate(Board &board,int no_of_moves){
    int depth=2*no_of_moves-1;
    history.clear();
    int score=negmax(board,depth,-inf,inf,history);
    if(score>=checkmate-depth){
        return true;
    }
    else{
        return false;
    }
}

void printLine(){
    for(int i=0;i<history.size();i++) {
        if(i%2==0){
            cout<<i/2+1<<". ";
        }
        cout<<uci::moveToUci(history[i])<<" ";
        if(i%2==1){
            cout<<'\n';
        }
    }
    cout<<'\n';
}

