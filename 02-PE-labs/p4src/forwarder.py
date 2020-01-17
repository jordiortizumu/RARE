#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import argparse, grpc, os, sys, socket
from time import sleep

# set our lib path
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
        './'))
# And then we import
import p4runtime_lib.bmv2
import p4runtime_lib.helper


def writeVrfRules(delete, p4info_helper, ingress_sw, port, vrf):
    table_entry = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_vrf.tbl_vrf",
        match_fields={
            "ig_md.source_id": port
        },
        action_name="ig_ctl.ig_ctl_vrf.act_set_vrf",
        action_params={
            "vrf": vrf
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry, False)


def writeVlanRules(delete, p4info_helper, ingress_sw, port, main, vlan):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_vlan_in.tbl_vlan_in",
        match_fields={
            "ig_intr_md.ingress_port": main,
            "hdr.vlan.vid": vlan
        },
        action_name="ig_ctl.ig_ctl_vlan_in.act_set_iface",
        action_params={
            "src": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_vlan_out.tbl_vlan_out",
        match_fields={
            "ig_md.target_id": port,
        },
        action_name="ig_ctl.ig_ctl_vlan_out.act_set_vlan_port",
        action_params={
            "port": main,
            "vlan": vlan
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeXconnRules(delete, p4info_helper, ingress_sw, port, target, lab_tun, lab_loc, lab_rem):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib",
        match_fields={
            "ig_md.mpls_label": lab_loc
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_decap_l2vpn",
        action_params={
            "port": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib_decap",
        match_fields={
            "ig_md.mpls_label": lab_loc
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_decap_l2vpn",
        action_params={
            "port": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry2, False)
    table_entry3 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_vrf.tbl_vrf",
        match_fields={
            "ig_md.source_id": port
        },
        action_name="ig_ctl.ig_ctl_vrf.act_set_mpls_xconn_encap",
        action_params={
            "target": target,
            "tunlab": lab_tun,
            "svclab": lab_rem
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry3, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry3, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry3, False)


def writeBrprtRules(delete, p4info_helper, ingress_sw, port, bridge):
    table_entry = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_vrf.tbl_vrf",
        match_fields={
            "ig_md.source_id": port
        },
        action_name="ig_ctl.ig_ctl_vrf.act_set_bridge",
        action_params={
            "bridge": bridge
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry, False)


def writeBrlabRules(delete, p4info_helper, ingress_sw, bridge, label):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib",
        match_fields={
            "ig_md.mpls_label": label
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_decap_vpls",
        action_params={
            "bridge": bridge
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib_decap",
        match_fields={
            "ig_md.mpls_label": label
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_decap_vpls",
        action_params={
            "bridge": bridge
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeBrsrvRules(delete, p4info_helper, ingress_sw, glob, dst_addr, bridge):
    table_entry = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_host",
        match_fields={
            "ig_md.vrf": (glob),
            "hdr.ipv6.dst_addr": (dst_addr)
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_srv_decap_evpn",
        action_params={
            "bridge": bridge
        }
    )
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry, False)


def writeBrvplsRules(delete, p4info_helper, ingress_sw, bridge, addr, port, labtun, labsvc):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_bridge.tbl_bridge_learn",
        match_fields={
            "ig_md.bridge_id": bridge,
            "hdr.ethernet.src_mac_addr": addr
        },
        action_name="ig_ctl.ig_ctl_bridge.act_set_bridge_port",
        action_params={
            "port": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_bridge.tbl_bridge_target",
        match_fields={
            "ig_md.bridge_id": bridge,
            "hdr.ethernet.dst_mac_addr": addr
        },
        action_name="ig_ctl.ig_ctl_bridge.act_set_bridge_vpls",
        action_params={
            "port": port,
            "lab_tun": labtun,
            "lab_svc": labsvc
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeBrsrv6rules(delete, p4info_helper, ingress_sw, bridge, addr, port, target):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_bridge.tbl_bridge_learn",
        match_fields={
            "ig_md.bridge_id": bridge,
            "hdr.ethernet.src_mac_addr": addr
        },
        action_name="ig_ctl.ig_ctl_bridge.act_set_bridge_port",
        action_params={
            "port": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_bridge.tbl_bridge_target",
        match_fields={
            "ig_md.bridge_id": bridge,
            "hdr.ethernet.dst_mac_addr": addr
        },
        action_name="ig_ctl.ig_ctl_bridge.act_set_bridge_srv",
        action_params={
            "port": port,
            "target": target
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeBrmacRules(delete, p4info_helper, ingress_sw, bridge, addr, port):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_bridge.tbl_bridge_learn",
        match_fields={
            "ig_md.bridge_id": bridge,
            "hdr.ethernet.src_mac_addr": addr
        },
        action_name="ig_ctl.ig_ctl_bridge.act_set_bridge_port",
        action_params={
            "port": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_bridge.tbl_bridge_target",
        match_fields={
            "ig_md.bridge_id": bridge,
            "hdr.ethernet.dst_mac_addr": addr
        },
        action_name="ig_ctl.ig_ctl_bridge.act_set_bridge_out",
        action_params={
            "port": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeForwardRules4(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, port, vrf):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4.act_ipv4_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4b.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4b.act_ipv4_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeForwardRules6(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, port, vrf):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_ipv6_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6b.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6b.act_ipv6_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeVpnRules4(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, port, vrf, egress_label, vpn_label):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4.act_ipv4_mpls_encap_set_nexthop",
        action_params={
            "vpn_label": vpn_label,
            "egress_label": egress_label,
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4b.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4b.act_ipv4_mpls_encap_set_nexthop",
        action_params={
            "vpn_label": vpn_label,
            "egress_label": egress_label,
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeVpnRules6(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, port, vrf, egress_label, vpn_label):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6b.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6b.act_ipv6_mpls_encap_set_nexthop",
        action_params={
            "vpn_label": vpn_label,
            "egress_label": egress_label,
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_ipv6_mpls_encap_set_nexthop",
        action_params={
            "vpn_label": vpn_label,
            "egress_label": egress_label,
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeSrvRules4(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, port, vrf, target):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4.act_ipv4_srv_encap_set_nexthop",
        action_params={
            "target": target,
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4b.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4b.act_ipv4_srv_encap_set_nexthop",
        action_params={
            "target": target,
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeSrvRules6(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, port, vrf, target):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_ipv6_srv_encap_set_nexthop",
        action_params={
            "target": target,
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6b.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6b.act_ipv6_srv_encap_set_nexthop",
        action_params={
            "target": target,
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeCoppRules4(delete, p4info_helper, ingress_sw, pri, act, pr, prm, sa, sam, da, dam, sp, spm, dp, dpm):
    table_entry = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_copp.tbl_ipv4_copp",
        match_fields={
            "hdr.ipv4.protocol": (pr , prm),
            "hdr.ipv4.src_addr": (sa,sam),
            "hdr.ipv4.dst_addr": (da,dam),
            "ig_md.layer4_srcprt": (sp,spm),
            "ig_md.layer4_dstprt": (dp,dpm)
        },
        action_name="ig_ctl.ig_ctl_copp.act_"+act,
        priority=pri,
        action_params={
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry, False)


def writeMyaddrRules4(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, vrf):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4.act_ipv4_cpl_set_nexthop",
        action_params={
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4b.tbl_ipv4_fib_lpm",
        match_fields={
            "hdr.ipv4b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4b.act_ipv4_cpl_set_nexthop",
        action_params={
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeMyaddrRules6(delete, p4info_helper, ingress_sw, dst_ip_addr, dst_net_mask, vrf):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_ipv6_cpl_set_nexthop",
        action_params={
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6b.tbl_ipv6_fib_lpm",
        match_fields={
            "hdr.ipv6b.dst_addr": (dst_ip_addr,dst_net_mask),
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6b.act_ipv6_cpl_set_nexthop",
        action_params={
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeNexthopRules(delete, p4info_helper, ingress_sw, port, dst_mac_addr, src_mac_addr):
    table_entry = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_nexthop.tbl_nexthop",
        match_fields={
            "ig_md.nexthop_id": port,
        },
        action_name="ig_ctl.ig_ctl_nexthop.act_ipv4_fib_hit",
        action_params={
            "dst_mac_addr": dst_mac_addr,
            "src_mac_addr": src_mac_addr,
            "egress_port": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry, False)


def writeNeighborRules4(delete, p4info_helper, ingress_sw, dst_ip_addr, port, vrf):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4.tbl_ipv4_fib_host",
        match_fields={
            "hdr.ipv4.dst_addr": dst_ip_addr,
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4.act_ipv4_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv4b.tbl_ipv4_fib_host",
        match_fields={
            "hdr.ipv4b.dst_addr": dst_ip_addr,
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv4b.act_ipv4_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeNeighborRules6(delete, p4info_helper, ingress_sw, dst_ip_addr, port, vrf):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_host",
        match_fields={
            "hdr.ipv6.dst_addr": dst_ip_addr,
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_ipv6_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6b.tbl_ipv6_fib_host",
        match_fields={
            "hdr.ipv6b.dst_addr": dst_ip_addr,
            "ig_md.vrf": vrf
        },
        action_name="ig_ctl.ig_ctl_ipv6b.act_ipv6_set_nexthop",
        action_params={
            "nexthop_id": port
        })
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeMplsRules(delete, p4info_helper, ingress_sw, dst_label, new_label, port):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib",
        match_fields={
            "ig_md.mpls_label": (dst_label)
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_swap0_set_nexthop",
        action_params={
            "egress_label": new_label,
            "nexthop_id": port
        }
    )
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib_decap",
        match_fields={
            "ig_md.mpls_label": (dst_label)
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_swap1_set_nexthop",
        action_params={
            "egress_label": new_label,
            "nexthop_id": port
        }
    )
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeMyMplsRules(delete, p4info_helper, ingress_sw, dst_label, vrf):
    table_entry1 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib",
        match_fields={
            "ig_md.mpls_label": (dst_label)
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_decap_ipv4",
        action_params={
            "vrf": vrf
        }
    )
    table_entry2 = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_mpls.tbl_mpls_fib_decap",
        match_fields={
            "ig_md.mpls_label": (dst_label)
        },
        action_name="ig_ctl.ig_ctl_mpls.act_mpls_decap_l3vpn",
        action_params={
            "vrf": vrf
        }
    )
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry1, False)
        ingress_sw.WriteTableEntry(table_entry2, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry1, False)
        ingress_sw.ModifyTableEntry(table_entry2, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry1, False)
        ingress_sw.DeleteTableEntry(table_entry2, False)


def writeMySrv4rules(delete, p4info_helper, ingress_sw, glob, dst_addr, vrf):
    table_entry = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_host",
        match_fields={
            "ig_md.vrf": (glob),
            "hdr.ipv6.dst_addr": (dst_addr)
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_srv_decap_ipv4",
        action_params={
            "vrf": vrf
        }
    )
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry, False)


def writeMySrv6rules(delete, p4info_helper, ingress_sw, glob, dst_addr, vrf):
    table_entry = p4info_helper.buildTableEntry(
        table_name="ig_ctl.ig_ctl_ipv6.tbl_ipv6_fib_host",
        match_fields={
            "ig_md.vrf": (glob),
            "hdr.ipv6.dst_addr": (dst_addr)
        },
        action_name="ig_ctl.ig_ctl_ipv6.act_srv_decap_ipv6",
        action_params={
            "vrf": vrf
        }
    )
    if delete == 1:
        ingress_sw.WriteTableEntry(table_entry, False)
    elif delete == 2:
        ingress_sw.ModifyTableEntry(table_entry, False)
    else:
        ingress_sw.DeleteTableEntry(table_entry, False)


def main(p4info_file_path, bmv2_file_path, p4runtime_address, freerouter_address, freerouter_port):
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect((freerouter_address, int(freerouter_port)))
    fil = sck.makefile('rw')

    sw1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
        name='sw1',
        address=p4runtime_address,
        device_id=0,
        proto_dump_file='p4runtime-requests.txt')
    sw1.MasterArbitrationUpdate()
    sw1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                    bmv2_json_file_path=bmv2_file_path)


    while 1:
        line = fil.readline(8192)
        splt = line.split(" ")
        print "rx: ", splt


        if splt[0] == "route4_add":
            addr = splt[1].split("/");
            writeForwardRules4(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "route4_mod":
            addr = splt[1].split("/");
            writeForwardRules4(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "route4_del":
            addr = splt[1].split("/");
            writeForwardRules4(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue

        if splt[0] == "labroute4_add":
            addr = splt[1].split("/");
            writeForwardRules4(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "labroute4_mod":
            addr = splt[1].split("/");
            writeForwardRules4(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "labroute4_del":
            addr = splt[1].split("/");
            writeForwardRules4(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue

        if splt[0] == "srvroute4_add":
            addr = splt[1].split("/");
            writeSrvRules4(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),splt[5])
            continue
        if splt[0] == "srvroute4_mod":
            addr = splt[1].split("/");
            writeSrvRules4(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),splt[5])
            continue
        if splt[0] == "srvroute4_del":
            addr = splt[1].split("/");
            writeSrvRules4(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),splt[5])
            continue

        if splt[0] == "vpnroute4_add":
            addr = splt[1].split("/");
            writeVpnRules4(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "vpnroute4_mod":
            addr = splt[1].split("/");
            writeVpnRules4(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "vpnroute4_del":
            addr = splt[1].split("/");
            writeVpnRules4(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue

        if splt[0] == "myaddr4_add":
            addr = splt[1].split("/");
            writeMyaddrRules4(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[3]))
            continue
        if splt[0] == "myaddr4_mod":
            addr = splt[1].split("/");
            writeMyaddrRules4(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[3]))
            continue
        if splt[0] == "myaddr4_del":
            addr = splt[1].split("/");
            writeMyaddrRules4(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[3]))
            continue

        if splt[0] == "copp4_add":
            writeCoppRules4(1,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]),int(splt[4]),splt[5],splt[6],splt[7],splt[8],int(splt[9]),int(splt[10]),int(splt[11]),int(splt[12]))
            continue
        if splt[0] == "copp4_mod":
            writeCoppRules4(2,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]),int(splt[4]),splt[5],splt[6],splt[7],splt[8],int(splt[9]),int(splt[10]),int(splt[11]),int(splt[12]))
            continue
        if splt[0] == "copp4_del":
            writeCoppRules4(3,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]),int(splt[4]),splt[5],splt[6],splt[7],splt[8],int(splt[9]),int(splt[10]),int(splt[11]),int(splt[12]))
            continue

        if splt[0] == "copp6_add":
            writeCoppRules6(1,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]),int(splt[4]),splt[5],splt[6],splt[7],splt[8],int(splt[9]),int(splt[10]),int(splt[11]),int(splt[12]))
            continue
        if splt[0] == "copp6_mod":
            writeCoppRules6(2,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]),int(splt[4]),splt[5],splt[6],splt[7],splt[8],int(splt[9]),int(splt[10]),int(splt[11]),int(splt[12]))
            continue
        if splt[0] == "copp6_del":
            writeCoppRules6(3,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]),int(splt[4]),splt[5],splt[6],splt[7],splt[8],int(splt[9]),int(splt[10]),int(splt[11]),int(splt[12]))
            continue

        if splt[0] == "label4_add":
            writeMplsRules(1,p4info_helper,sw1,int(splt[1]),int(splt[4]),int(splt[2]))
            continue
        if splt[0] == "label4_mod":
            writeMplsRules(2,p4info_helper,sw1,int(splt[1]),int(splt[4]),int(splt[2]))
            continue
        if splt[0] == "label4_del":
            writeMplsRules(3,p4info_helper,sw1,int(splt[1]),int(splt[4]),int(splt[2]))
            continue

        if splt[0] == "mylabel4_add":
            writeMyMplsRules(1,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "mylabel4_mod":
            writeMyMplsRules(2,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "mylabel4_del":
            writeMyMplsRules(3,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue

        if splt[0] == "neigh4_add":
            writeNexthopRules(1,p4info_helper,sw1,int(splt[1]),splt[3],splt[5])
            writeNeighborRules4(1,p4info_helper,sw1,splt[2],int(splt[1]),int(splt[4]))
            continue
        if splt[0] == "neigh4_mod":
            writeNexthopRules(2,p4info_helper,sw1,int(splt[1]),splt[3],splt[5])
            writeNeighborRules4(2,p4info_helper,sw1,splt[2],int(splt[1]),int(splt[4]))
            continue
        if splt[0] == "neigh4_del":
            writeNexthopRules(3,p4info_helper,sw1,int(splt[1]),splt[3],splt[5])
            writeNeighborRules4(3,p4info_helper,sw1,splt[2],int(splt[1]),int(splt[4]))
            continue


        if splt[0] == "portvrf_add":
            writeVrfRules(1,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "portvrf_mod":
            writeVrfRules(2,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "portvrf_del":
            writeVrfRules(3,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue

        if splt[0] == "portvlan_add":
            writeVlanRules(1,p4info_helper,sw1,int(splt[1]),int(splt[2]),int(splt[3]))
            continue
        if splt[0] == "portvrf_mod":
            writeVlanRules(2,p4info_helper,sw1,int(splt[1]),int(splt[2]),int(splt[3]))
            continue
        if splt[0] == "portvrf_del":
            writeVlanRules(3,p4info_helper,sw1,int(splt[1]),int(splt[2]),int(splt[3]))
            continue

        if splt[0] == "xconnect_add":
            writeXconnRules(1,p4info_helper,sw1,int(splt[1]),int(splt[3]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "xconnect_mod":
            writeXconnRules(2,p4info_helper,sw1,int(splt[1]),int(splt[3]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "xconnect_del":
            writeXconnRules(3,p4info_helper,sw1,int(splt[1]),int(splt[3]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue

        if splt[0] == "portbridge_add":
            writeBrprtRules(1,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "portbridge_mod":
            writeBrprtRules(2,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "portbridge_del":
            writeBrprtRules(3,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue

        if splt[0] == "bridgemac_add":
            writeBrmacRules(1,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue
        if splt[0] == "bridgemac_mod":
            writeBrmacRules(2,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue
        if splt[0] == "bridgemac_del":
            writeBrmacRules(3,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue

        if splt[0] == "bridgelabel_add":
            writeBrlabRules(1,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "bridgelabel_mod":
            writeBrlabRules(2,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "bridgelabel_del":
            writeBrlabRules(3,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue

        if splt[0] == "bridgevpls_add":
            writeBrvplsRules(1,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "bridgevpls_mod":
            writeBrvplsRules(2,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "bridgevpls_del":
            writeBrvplsRules(3,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[4]),int(splt[5]),int(splt[6]))
            continue

        if splt[0] == "bridgesrv_add":
            writeBrsrvRules(1,p4info_helper,sw1,int(splt[2]),splt[3],int(splt[1]))
            continue
        if splt[0] == "bridgesrv_mod":
            writeBrsrvRules(2,p4info_helper,sw1,int(splt[2]),splt[3],int(splt[1]))
            continue
        if splt[0] == "bridgesrv_del":
            writeBrsrvRules(3,p4info_helper,sw1,int(splt[2]),splt[3],int(splt[1]))
            continue

        if splt[0] == "bridgesrv6_add":
            writeBrsrv6rules(1,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[4]),splt[5])
            continue
        if splt[0] == "bridgesrv6_mod":
            writeBrsrv6rules(2,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[4]),splt[5])
            continue
        if splt[0] == "bridgesrv6_del":
            writeBrsrv6rules(3,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[4]),splt[5])
            continue

        if splt[0] == "route6_add":
            addr = splt[1].split("/");
            writeForwardRules6(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "route6_mod":
            addr = splt[1].split("/");
            writeForwardRules6(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "route6_del":
            addr = splt[1].split("/");
            writeForwardRules6(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue

        if splt[0] == "labroute6_add":
            addr = splt[1].split("/");
            writeForwardRules6(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "labroute6_mod":
            addr = splt[1].split("/");
            writeForwardRules6(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue
        if splt[0] == "labroute6_del":
            addr = splt[1].split("/");
            writeForwardRules6(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]))
            continue

        if splt[0] == "srvroute6_add":
            addr = splt[1].split("/");
            writeSrvRules6(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),splt[5])
            continue
        if splt[0] == "srvroute6_mod":
            addr = splt[1].split("/");
            writeSrvRules6(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),splt[5])
            continue
        if splt[0] == "srvroute6_del":
            addr = splt[1].split("/");
            writeSrvRules6(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),splt[5])
            continue

        if splt[0] == "vpnroute6_add":
            addr = splt[1].split("/");
            writeVpnRules6(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "vpnroute6_mod":
            addr = splt[1].split("/");
            writeVpnRules6(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue
        if splt[0] == "vpnroute6_del":
            addr = splt[1].split("/");
            writeVpnRules6(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[2]),int(splt[4]),int(splt[5]),int(splt[6]))
            continue

        if splt[0] == "myaddr6_add":
            addr = splt[1].split("/");
            writeMyaddrRules6(1,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[3]))
            continue
        if splt[0] == "myaddr6_mod":
            addr = splt[1].split("/");
            writeMyaddrRules6(2,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[3]))
            continue
        if splt[0] == "myaddr6_del":
            addr = splt[1].split("/");
            writeMyaddrRules6(3,p4info_helper,sw1,addr[0],int(addr[1]),int(splt[3]))
            continue

        if splt[0] == "label6_add":
            writeMplsRules(1,p4info_helper,sw1,int(splt[1]),int(splt[4]),int(splt[2]))
            continue
        if splt[0] == "label6_mod":
            writeMplsRules(2,p4info_helper,sw1,int(splt[1]),int(splt[4]),int(splt[2]))
            continue
        if splt[0] == "label6_del":
            writeMplsRules(3,p4info_helper,sw1,int(splt[1]),int(splt[4]),int(splt[2]))
            continue

        if splt[0] == "mysrv4_add":
            writeMySrv4rules(1,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue
        if splt[0] == "mysrv4_mod":
            writeMySrv4rules(2,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue
        if splt[0] == "mysrv4_del":
            writeMySrv4rules(3,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue

        if splt[0] == "mysrv6_add":
            writeMySrv6rules(1,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue
        if splt[0] == "mysrv6_mod":
            writeMySrv6rules(2,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue
        if splt[0] == "mysrv6_del":
            writeMySrv6rules(3,p4info_helper,sw1,int(splt[1]),splt[2],int(splt[3]))
            continue

        if splt[0] == "mylabel6_add":
            writeMyMplsRules(1,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "mylabel6_mod":
            writeMyMplsRules(2,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue
        if splt[0] == "mylabel6_del":
            writeMyMplsRules(3,p4info_helper,sw1,int(splt[1]),int(splt[2]))
            continue

        if splt[0] == "neigh6_add":
#            writeNexthopRules(1,p4info_helper,sw1,int(splt[1]),splt[3],splt[5])
            writeNeighborRules6(1,p4info_helper,sw1,splt[2],int(splt[1]),int(splt[4]))
            continue
        if splt[0] == "neigh6_mod":
#            writeNexthopRules(2,p4info_helper,sw1,int(splt[1]),splt[3],splt[5])
            writeNeighborRules6(2,p4info_helper,sw1,splt[2],int(splt[1]),int(splt[4]))
            continue
        if splt[0] == "neigh6_del":
#            writeNexthopRules(3,p4info_helper,sw1,int(splt[1]),splt[3],splt[5])
            writeNeighborRules6(3,p4info_helper,sw1,splt[2],int(splt[1]),int(splt[4]))
            continue






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')

    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
            type=str, action="store", required=False,
            default="../build/router.txt")
    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
            type=str, action="store", required=False,
            default="../build/router.json")
    parser.add_argument('--p4runtime_address', help='p4 runtime address',
            type=str, action="store", required=False,
            default="127.0.0.1:50051")
    parser.add_argument('--freerouter_address', help='freerouter address',
            type=str, action="store", required=False,
            default="10.10.10.227")
    parser.add_argument('--freerouter_port', help='freerouter port',
            type=str, action="store", required=False,
            default="9080")
    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print "p4info file not found."
        parser.exit(1)
    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print "BMv2 JSON file not found."
        parser.exit(1)

    main(args.p4info, args.bmv2_json, args.p4runtime_address, args.freerouter_address, args.freerouter_port)
