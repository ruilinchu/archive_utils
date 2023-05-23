#include <sw/redis++/redis++.h>
#include <iostream>
using namespace sw::redis;
using namespace std;

int main(int argc, char* argv[]) {

  string str_put("put");
  string str_get("get");
  string str_del("del");
  string aput("arcput");
  string aget("arcget");
  string adel("arcdel");

  string sa("aa");
  string sb("bb");
  string sc("cc");
  string sd("dd");
  string se("ee");
  string sf("ff");
  string sg("gg");
  string sh("@127.0.0.1:6379/0");
  string si("tcp://default:");

  string fu=si + sa + sb + sc + sd + se + sf + sg + sh;
 // cout << fu << endl;
  
  auto redis = Redis(fu);

  if(argv[1] == str_put){
//    cout << "putting a file: " << argv[2] << endl;
    redis.sadd(aput, argv[2]);
  } else if(argv[1] == str_get){
//    cout << "getting a file: " << endl;
    redis.sadd(aget, argv[2]);
  } else if(argv[1] == str_del){
//    cout << "deleting a file" << endl;
    redis.sadd(adel, argv[2]);
  }
  
}
//g++ -std=c++17 -o sendit sendredis.cpp /usr/local/lib64/libredis++.a /usr/local/lib/libhiredis.a -pthread
