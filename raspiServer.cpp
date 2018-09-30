#include <iostream>
#include <fstream>

#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

using namespace std;

int main(){
    cout << "run\r\n";
    char  addr[19]={0};
    char  name[248]={0};

    int dev_id=hci_get_route(NULL);
    int sock=hci_open_dev(dev_id);

    if(dev_id<0 || sock<0){
        perror("opening socket error");
        exit(1);
    }

    int len=8;
    int max_rsp=255;
    int flags=IREQ_CACHE_FLUSH;
    inquiry_info *ii = new inquiry_info[max_rsp*sizeof(inquiry_info)];

    int num_rsp=hci_inquiry(dev_id, len, max_rsp, NULL, &ii, flags);
    if(num_rsp<0)perror("hci_inquiry");

    for(int it=0; it<num_rsp; it++){
        ba2str(&(ii+it)->bdaddr, addr);
        memset(name, 0, sizeof(name));
        if(hci_read_remote_name(sock, &(ii+it)->bdaddr, sizeof(name), name, 0)<0){
            strcpy(name,"[unknown]");
        }
        cout << addr << "\t" << name << endl;
    }

    delete[] ii;
    close(sock);
    cout<<"end\r\n";
    return 0;
}
