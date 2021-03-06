# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
#  Copyright © 2015-2016 VMware, Inc. All Rights Reserved.                    #
#                                                                             #
#  Licensed under the BSD 2-Clause License (the “License”); you may not use   #
#  this file except in compliance with the License.                           #
#                                                                             #
#  The BSD 2-Clause License                                                   #
#                                                                             #
#  Redistribution and use in source and binary forms, with or without         #
#  modification, are permitted provided that the following conditions are met:#
#                                                                             #
#  - Redistributions of source code must retain the above copyright notice,   #
#      this list of conditions and the following disclaimer.                  #
#                                                                             #
#  - Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#                                                                             #
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"#
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  #
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE #
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  #
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR        #
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF       #
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS   #
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN    #
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)    #
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF     #
#  THE POSSIBILITY OF SUCH DAMAGE.                                            #
# ----------------------------------------------------------------------------#

from liota.core.package_manager import LiotaPackage

dependencies = ["edge_systems/dell5k/edge_system"]


class PackageClass(LiotaPackage):
    """
    This package creates a IoTControlCenter DCC object and registers edge system on
    IoTCC to acquire "registered edge system", i.e. iotcc_edge_system.
    """

    def run(self, registry):
        import copy
        from liota.dccs.iotcc import IotControlCenter
        from liota.dcc_comms.websocket_dcc_comms import WebSocketDccComms
        from liota.dccs.dcc import RegistrationFailure

        # Acquire resources from registry
        # Creating a copy of edge_system object to keep original object "clean"
        edge_system = copy.copy(registry.get("edge_system"))

        # Get values from configuration file
        config_path = registry.get("package_conf")
        config = {}
        execfile(config_path + '/sampleProp.conf', config)

        # Initialize DCC object with transport
        self.iotcc = IotControlCenter(
            config['IotCCUID'], config['IotCCPassword'],
            WebSocketDccComms(url=config['WebSocketUrl'])
        )

        try:
            # Register edge system (gateway)
            iotcc_edge_system = self.iotcc.register(edge_system)

            registry.register("iotcc", self.iotcc)
            registry.register("iotcc_edge_system", iotcc_edge_system)
        except RegistrationFailure:
            print "EdgeSystem registration to IOTCC failed"

    def clean_up(self):
        self.iotcc.comms.wss.close()
