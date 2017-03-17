# Pour exécuter les commandes suivantes
# Il est nécessaire d'avoir obtenu les
# Informations grâce aux trois commandes
# ci-dessous
# df -h
# cat /proc/partitions
# ll /dev/disk/by-id

#xe sr-create content-type=user device-config:device=/dev/disk/by-id/<scsi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx> host-uuid=<host-uuid> name-label="Local Storage" shared=false type=<ext|lvm>