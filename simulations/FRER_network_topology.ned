//
// SPDX-License-Identifier: LGPL-3.0-or-later
//


package frer.simulations;

import inet.common.scenario.ScenarioManager;
import inet.networks.base.TsnNetworkBase;
import inet.node.ethernet.EthernetLink;
import inet.node.tsn.TsnDevice;
import inet.node.tsn.TsnSwitch;
import inet.queueing.common.PacketDelayer;
import ned.DatarateChannel;  // DelayChannel’s base




module LocalTsnSwitch extends TsnSwitch
{
    @defaultStatistic("gateStateChanged:vector"; module="eth[0].macLayer.queue.gate[0]");
}

network FRERnetwork extends TsnNetworkBase
{
    submodules:
        scenarioManager: ScenarioManager {
            @display("p=100,800;is=s");
        }
        source: TsnDevice {
            @display("p=300,200");
            numEthInterfaces = 1;
        }
        s1: LocalTsnSwitch {
            @display("p=431,199");
            numEthInterfaces = 3;
        }
        s2: LocalTsnSwitch {
            @display("p=678,199");
            numEthInterfaces = 3;
        }
        destination: TsnDevice {
            @display("p=880,200");
            numEthInterfaces = 1;
        }
    connections allowunconnected:
        source.ethg[0] <--> EthernetLink <--> s1.ethg[0];
        s2.ethg[0] <--> EthernetLink <--> destination.ethg[0];
        //link1
        s1.ethg[1] <--> EthernetLink {  delay = 0ms; } <--> s2.ethg[1];
        //link2
        s1.ethg[2] <--> EthernetLink {  delay = 0ms; } <--> s2.ethg[2];

}
