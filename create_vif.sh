#!/bin/sh
xe vif-unplug uuid=18f686d9-fb28-5213-0b67-4625af1291b6 && xe vif-destroy uuid=18f686d9-fb28-5213-0b67-4625af1291b6
xe vif-plug uuid=$(xe vif-create network-uuid=34309e41-1604-db41-99af-9ee21425dfaf vm-uuid=b30cb151-e87c-bec5-988e-96298ddef9ee device=0)
