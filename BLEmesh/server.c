#include <stdio.h>
#include <stdlib.h>
#include "btlib.h"
#include <string.h>
#include <unistd.h>
#include <curl/curl.h>

int mesh_callback(int clientnode,char *data,int datlen);


int main()
  {

	if(init_blue("hellodev.txt") == 0)
      return(0);
	// MESH SERVER
	mesh_server(mesh_callback);

  }

int mesh_callback(int clientnode,char *data,int datlen)
  {
  int n; 
  printf("Mesh packet from %s\n",device_name(clientnode));
  
  // char *delimiter = strchr(data, ':');
  // if (delimiter != NULL) {
  //   // Extract scope name
  //   char name[32];
  //   memcpy(name, data, delimiter - data);
  //   name[delimiter - data] = '\0';
  //   printf("%s\n", name);
    
  //   // Extract rssi
  //   char rssi[32];
  //   strcpy(rssi, delimiter + 1);
  //   printf("%s\n", rssi);
  // }

  // Send to Flask
  CURL *curl;
  CURLcode res;

  curl = curl_easy_init();
  if(curl) {
    char postData[100];
    sprintf(postData,"%s,%s",device_name(clientnode),data);
    curl_easy_setopt(curl, CURLOPT_URL, "http://172.30.142.110:8015/updateValues");
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData);
    res = curl_easy_perform(curl);
    if(res != CURLE_OK)
      fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    curl_easy_cleanup(curl);
  }
  // sleep(1);
  
  //~ if(data[0] == 'D')   // 'D' programmed as exit command
    //~ return(SERVER_EXIT);
  return(SERVER_CONTINUE);  // wait for another packet
  }
