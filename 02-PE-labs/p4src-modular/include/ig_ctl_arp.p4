#ifndef _IG_CTL_ARP_P4_                                                                          
#define _IG_CTL_ARP_P4_                                                                          
                                                                                                  
control IngressControlARP(inout headers hdr,                                                     
               inout ingress_metadata_t ig_md, 
                          inout standard_metadata_t ig_intr_md) {                   
                                                                                                  
   action send_to_cpu() {                                                                         
      /*                                                                                          
       * Prepend pkt_in header to pkt sent to controller                                          
       * by calling setValid() so it is tekne into account by deparser                            
       */                                                                                         
        ig_md.nexthop_id = CPU_PORT;                                                                   
   }                                                                                              

   apply {                                            
        /*                                            
         * It is a dataplane packet                   
         */                                           
        if (ig_md.arp_valid==1)  { 
           send_to_cpu();
        }                                             
   }                                                  

}

#endif // _IG_CTL_ARP_P4_
