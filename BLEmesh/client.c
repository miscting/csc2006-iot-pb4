#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "btlib.h"
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>
#include <pthread.h>

int mesh_callback(int clientnode,char *data,int datlen);

void *meshThread(void *vargp)
{
    mesh_server(mesh_callback);
}

int main()
  {
	char endo_jw[] = "C6:29:09:6D:9F:E8";
	char endo_shyam[] = "66:8D:CB:25:75:4C";
	  
	if(init_blue("hellodev.txt") == 0)
	  return(0);

	pthread_t tid;
	pthread_create(&tid, NULL, meshThread, NULL);
		
	//RSSI stuff
	int dev_id = hci_get_route(NULL);
	int sock = hci_open_dev(dev_id);
	hci_le_set_scan_parameters(sock, 0x01, htobs(0x0010), htobs(0x0010), 0x00, 0x00, 1000);
    hci_le_set_scan_enable(sock, 0x01, 1, 1000);
    
    struct hci_filter nf, of;
    hci_filter_clear(&nf);
    hci_filter_set_ptype(HCI_EVENT_PKT, &nf);
    hci_filter_set_event(EVT_LE_META_EVENT, &nf);
    setsockopt(sock, SOL_HCI, HCI_FILTER, &nf, sizeof(nf));

	while(1) {
		unsigned char buf[HCI_MAX_EVENT_SIZE], *ptr;
		int len;

		len = read(sock, buf, sizeof(buf));
		ptr = buf + (1 + HCI_EVENT_HDR_SIZE);
		len -= (1 + HCI_EVENT_HDR_SIZE);

		evt_le_meta_event *meta = (evt_le_meta_event *) ptr;
		if(meta->subevent != 0x02) continue;

		le_advertising_info *info = (le_advertising_info *) (meta->data + 1);
		int rssi = (signed char)info->data[info->length];
		// printf("Device %s\n", batostr(&info->bdaddr));
		
		char dataBuf[32];
		if(strcmp(batostr(&info->bdaddr),endo_jw) == 0) {
			sprintf(dataBuf,"endo_jw:%d",rssi);
			//~ printf("Device endo_jw has RSSI %d\n", (rssi*-1)+120);
			// broadcast mesh packet
			write_mesh(dataBuf, strlen(dataBuf));
			sleep(3);
		} else if(strcmp(batostr(&info->bdaddr),endo_shyam) == 0) {
			sprintf(dataBuf,"endo_shyam:%d",rssi);
			//~ printf("Device endo_shyam has RSSI %d\n", (rssi*-1)+120);
			// broadcast mesh packet
			write_mesh(dataBuf, strlen(dataBuf));
			sleep(3);
		}
	}
	close(sock);
	pthread_exit(NULL);
	// broadcast D disconnect command
	//~ char cmd = 'D'; // Use a char variable instead of a string literal
	//~ write_mesh(&cmd, 1);
	//~ sleep(1);  // 1 second delay to allow packet to be sent

  }

int mesh_callback(int clientnode,char *data,int datlen)
  {
  int n; 
  printf("Mesh packet from %s : %s\n",device_name(clientnode), data);

  return(SERVER_CONTINUE);  // wait for another packet
  }
