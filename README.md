# LabMec2025
Progetto per esame di laboratorio di meccatronica 2025

Questo repositorio contiene i file relativi al progetto di laboritorio di meccatronica del 2025

Link modello catamarano: https://github.com/Intelligent-Quads/iq_sim

comando primo terminale 
gz sim /home/gelatocotonato/prog_mec/src/world/simple_baylands.sdf

comando secondo terminale
gz service -s /world/simple_baylands/create --reqtype gz.msgs.EntityFactory --reptype gz.msgs.Boolean --timeout 1000 --req 'sdf_filename: "/home/gelatocotonato/prog_mec/src/boat_description/boat/model.sdf"'

link per aggiungere sensore: https://gazebosim.org/docs/harmonic/sensors/

esempio utile per prendere i modelli: https://github.com/osrf/vrx.git
