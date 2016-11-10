#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <queue>
#include <stack>
#include <cmath>
#include <climits>
using namespace std;

struct Edge
{
  int targetIndex;
  int length;
  Edge(int t,int l): targetIndex(t), length(l) {}
};

struct Node
{
  string name;
  int sundayDistance;
  int pathLength;
  vector<Node *> path;
  vector<Edge *> nexts;
  Node(string n) : name(n) {}
};


int main () {
  string algo;
  string start;
  string end;
  int num;
  int sundayNum;
  vector<Node *> nodes;
  map<string,int> hashTable;
  ifstream in ("input.txt");
  ofstream out ("output.txt");
  if (in.is_open())
  {
    vector<string> trafficOrder;
    in>>algo;
    in>>start;
    in>>end;
    in>>num;
    for(int i = 0;i<num;++i){
      string from;
      string to;
      int distance;
      in>>from;
      in>>to;
      in>>distance;
      if(hashTable.find(from)!=hashTable.end()){
        int index = hashTable[from];
        if(hashTable.find(to)!=hashTable.end()){
          nodes[index]->nexts.push_back(new Edge(hashTable[to],distance));
        }
        else{
          trafficOrder.push_back(to);
          hashTable[to] = nodes.size();
          nodes.push_back(new Node(to));
          nodes[index]->nexts.push_back(new Edge(hashTable[to],distance));
        }
      }
      else{
        trafficOrder.push_back(from);
        hashTable[from] = nodes.size();
        nodes.push_back(new Node(from));
        int index = hashTable[from];
        if(hashTable.find(to)!=hashTable.end()){
          nodes[index]->nexts.push_back(new Edge(hashTable[to],distance));
        }
        else{
          trafficOrder.push_back(to);
          hashTable[to] = nodes.size();
          nodes.push_back(new Node(to));
          nodes[index]->nexts.push_back(new Edge(hashTable[to],distance));
        }
      }
    }
    in>>sundayNum;
    for(int i = 0;i<sundayNum;i++){
        string nodeName;
        int sun;
        in>>nodeName;
        in>>sun;
        nodes[hashTable[nodeName]]->sundayDistance = sun;
    }

    if(algo=="BFS"){

      queue<Node *> q;
      map<string,int> visited;

      q.push(nodes[hashTable[start]]);
      nodes[hashTable[start]]->pathLength = 0;
      nodes[hashTable[start]]->path.push_back(nodes[hashTable[start]]);
      visited[start] = 0;

      while(!q.empty()){
        Node* top = q.front();
        visited[top->name] = 0;
        for(int i = 0;i<trafficOrder.size();++i){
          for(int j = 0;j<top->nexts.size();++j){
            int target = top->nexts[j]->targetIndex;
            if(nodes[target]->name == trafficOrder[i] && visited.find(trafficOrder[i]) == visited.end()){
              q.push(nodes[target]);
              nodes[target]->pathLength = top->pathLength+1;
              nodes[target]->path = top->path;
              nodes[target]->path.push_back(nodes[target]);
              if(nodes[target]->name == end){
                for(int k = 0;k<nodes[target]->path.size();++k){
                  out<<nodes[target]->path[k]->name<<" "<<nodes[target]->path[k]->pathLength<<endl;
                }
                return 0;
              }
            }
          }
        }
        q.pop();
      }
      return 0;
    }
    else if(algo=="DFS"){

      stack<Node *> q;
      map<string,int> visited;
      map<string,int> queued;

      q.push(nodes[hashTable[start]]);
      nodes[hashTable[start]]->pathLength = 0;
      nodes[hashTable[start]]->path.push_back(nodes[hashTable[start]]);
      visited[start] = 0;

      while(!q.empty()){
        Node* top = q.top();
        visited[top->name] = 0;
        q.pop();
        for(int i = trafficOrder.size()-1;i>=0;i--){
          for(int j = 0;j<top->nexts.size();++j){
            int target = top->nexts[j]->targetIndex;
            if(nodes[target]->name == trafficOrder[i] && visited.find(trafficOrder[i]) == visited.end() && queued.find(trafficOrder[i]) == queued.end()){
              queued[nodes[target]->name] = 0;
              q.push(nodes[target]);
              nodes[target]->pathLength = top->pathLength+1;
              nodes[target]->path = top->path;
              nodes[target]->path.push_back(nodes[target]);
              if(nodes[target]->name == end){
                for(int k = 0;k<nodes[target]->path.size();++k){
                  out<<nodes[target]->path[k]->name<<" "<<nodes[target]->path[k]->pathLength<<endl;
                }
                return 0;
              }
            }
          }
        }
      }
      return 0;
    }

    else if(algo=="UCS"){
      map<Node *,int> q;
      map<string,int> visited;

      q[nodes[hashTable[start]]] = 0;
      nodes[hashTable[start]]->pathLength = 0;
      nodes[hashTable[start]]->path.push_back(nodes[hashTable[start]]);
      visited[start] = 0;

      map<Node *,int> age;
      age[nodes[hashTable[start]]] = 0;


      int counter = 0;
      while(!q.empty()){
        counter++;
        Node* top = q.begin()->first;
        int minDistance = q.begin()->second;
        for(map<Node *, int>::iterator it = q.begin();it!=q.end();it++){
          if(it->second<minDistance){
            top = it->first;
            minDistance = it->second;
          }
          else if(it->second==minDistance){
            if(age[it->first]<age[top]){
              top = it->first;
            }
            else if(age[it->first]==age[top]){
              int topIndex = 0;
              for(int i = 0;i<trafficOrder.size();++i){
                if(trafficOrder[i]==top->name){
                  topIndex = i;
                  break;
                }
              }

              int itIndex = 0;
              for(int i = 0;i<trafficOrder.size();++i){
                if(trafficOrder[i]==it->first->name){
                  itIndex = i;
                  break;
                }
              }
              if(itIndex<topIndex){
                top = it->first;
              }
            }
          }
        }
        if(top->name == end){
          for(int k = 0;k<top->path.size();++k){
            out<<top->path[k]->name<<" "<<top->path[k]->pathLength<<endl;
          }
          return 0;
        }
        q.erase(top);
        visited[top->name] = 0;
        for(int j = 0;j<top->nexts.size();++j){
          int target = top->nexts[j]->targetIndex;

          if(visited.find(nodes[target]->name) == visited.end()){
            if(q.find(nodes[target]) == q.end()){
              q[nodes[target]] = top->pathLength+top->nexts[j]->length;
              nodes[target]->pathLength = q[nodes[target]];
              nodes[target]->path = top->path;
              nodes[target]->path.push_back(nodes[target]);
              age[nodes[target]] = counter;
              //cout<<nodes[target]->name<<" "<<q[nodes[target]]<<endl;
            }
            else{
              if(q[nodes[target]]>top->pathLength+top->nexts[j]->length){
                q[nodes[target]] = top->pathLength+top->nexts[j]->length;
                nodes[target]->pathLength = q[nodes[target]];
                nodes[target]->path = top->path;
                nodes[target]->path.push_back(nodes[target]);
                age[nodes[target]] = counter;
                //cout<<nodes[target]->name<<" "<<q[nodes[target]]<<endl;
              }
            }
          }

        }

      }
      return 0;
    }
    else if(algo=="A*"){
      map<Node *,int> q;
      map<string,int> visited;

      q[nodes[hashTable[start]]] = nodes[hashTable[start]]->sundayDistance;
      nodes[hashTable[start]]->pathLength = 0;
      nodes[hashTable[start]]->path.push_back(nodes[hashTable[start]]);
      visited[start] = 0;

      map<Node *,int> age;
      age[nodes[hashTable[start]]] = 0;
      int counter = 0;
      while(!q.empty()){
        counter++;
        Node* top = q.begin()->first;
        int minDistance = q.begin()->second;
        for(map<Node *, int>::iterator it = q.begin();it!=q.end();it++){
          if(it->second<minDistance){
            top = it->first;
            minDistance = it->second;
          }
          else if(it->second==minDistance){
            if(age[it->first]<age[top]){
              top = it->first;
            }
            else if(age[it->first]==age[top]){
              int topIndex = 0;
              for(int i = 0;i<trafficOrder.size();++i){
                if(trafficOrder[i]==top->name){
                  topIndex = i;
                  break;
                }
              }

              int itIndex = 0;
              for(int i = 0;i<trafficOrder.size();++i){
                if(trafficOrder[i]==it->first->name){
                  itIndex = i;
                  break;
                }
              }
              if(itIndex<topIndex){
                top = it->first;
              }
            }
          }
        }
        if(top->name == end){
          for(int k = 0;k<top->path.size();++k){
            out<<top->path[k]->name<<" "<<top->path[k]->pathLength<<endl;
          }
          return 0;
        }
        q.erase(top);
        visited[top->name] = 0;
        for(int j = 0;j<top->nexts.size();++j){
          int target = top->nexts[j]->targetIndex;
          if(visited.find(nodes[target]->name) == visited.end()){
            if(q.find(nodes[target]) == q.end()){
              q[nodes[target]] = top->pathLength+top->nexts[j]->length+nodes[target]->sundayDistance;
              nodes[target]->pathLength = top->pathLength+top->nexts[j]->length;
              nodes[target]->path = top->path;
              nodes[target]->path.push_back(nodes[target]);
              age[nodes[target]] = counter;
            }
            else{
              if(q[nodes[target]]>top->pathLength+top->nexts[j]->length){
                q[nodes[target]] = top->pathLength+top->nexts[j]->length+nodes[target]->sundayDistance;
                nodes[target]->pathLength = top->pathLength+top->nexts[j]->length;
                nodes[target]->path = top->path;
                nodes[target]->path.push_back(nodes[target]);
                age[nodes[target]] = counter;
              }
            }
          }

        }

      }
      return 0;
    }

  }
  else cout << "Unable to open file"<< '\n'; 
  return 0;
}
