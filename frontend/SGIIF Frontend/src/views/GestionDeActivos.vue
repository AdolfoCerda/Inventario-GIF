<template>
  <Header />

  <div class="add-asset">
    <h2>Agregar/Editar/Eliminar Activo</h2>
    <form @submit.prevent="handleSubmit">
      <!-- Sección 1: Datos Generales -->
      <div class="form-section">
        <h2>Datos Generales</h2>
        <!-- Fila 1 -->
        <div class="form-row">
          <!-- Campo: Número de Serie -->
          <div class="form-group">
            <label for="serialNumber">Número de Serie:</label>
            <input type="text" id="serialNumber" v-model="asset.Serial" @blur="buscarActivo" required />
          </div>

          <!-- Campo: Nombre -->
          <div class="form-group">
            <label for="name">Nombre:</label>
            <input type="text" id="name" v-model="asset.Nombre" required />
          </div>

          <!-- Campo: Sitio (Catálogo) -->
          <div class="form-group">
            <label for="site">Sitio:</label>
            <select id="site" v-model="asset.Sitio" required>
              <option v-for="option in catalogOptions.Sitios" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Ambiente (Catálogo) -->
          <div class="form-group">
            <label for="ambiente">Ambiente:</label>
            <select id="ambiente" v-model="asset.Ambiente" required>
              <option v-for="option in catalogOptions.Ambientes" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Tipo (Catálogo) -->
          <div class="form-group">
            <label for="tipo">Tipo:</label>
            <select id="tipo" v-model="asset.Tipo" required>
              <option v-for="option in catalogOptions.Tipos" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Bahia -->
          <div class="form-group">
            <label for="bahia">Bahia:</label>
            <input type="text" id="bahia" v-model="asset.Bahia" required />
          </div>

        </div>

        <!-- Fila 2 -->
        <div class="form-row">
          <!-- Campo: Estatus -->
          <div class="form-group">
            <label for="status">Estatus:</label>
            <input type="text" id="status" v-model="asset.Estatus" readonly required />
          </div>

          <!-- Campo: Encendido (Catálogo) -->
          <div class="form-group">
              <label for="powerStatus">Encendido:</label>
              <select id="powerStatus" v-model="asset.Encendido" required>
                <option v-for="option in catalogOptions.Encendido" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
          </div>

          <!-- Campo: Marca (Catálogo) -->
          <div class="form-group">
            <label for="marca">Marca:</label>
            <select id="marca" v-model="asset.Marca" required>
              <option v-for="option in catalogOptions.Marcas" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Modelo -->
          <div class="form-group">
            <label for="modelo">Modelo:</label>
            <input type="text" id="modelo" v-model="asset.Modelo" required />
          </div>

          <!-- Campo: Cluster -->
          <div class="form-group">
            <label for="cluster">Cluster:</label>
            <input type="text" id="cluster" v-model="asset.Cluster" required />
          </div>

          <!-- Campo: Chassis -->
          <div class="form-group">
            <label for="chassis">Chassis:</label>
            <input type="text" id="chassis" v-model="asset.Chassis" required />
          </div>

        </div>

        <!-- Filas Servicios -->
        <div class="form-row servicios-row">
          <label>Servicios:</label>
        </div>
        <div class="form-row servicios-row">
          <div class="form-group servicio-check">
            <input type="checkbox" id="afore" v-model="asset.Afore"/>
            <label for="afore">Afore</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="bancoppel" v-model="asset.BanCoppel"/>
            <label for="bancoppel">BanCoppel</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="cartera" v-model="asset.Cartera"/>
            <label for="cartera">Cartera en Línea</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="ETL" v-model="asset.ETL"/>
            <label for="ETL">ETL</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="huellas" v-model="asset.Huellas"/>
            <label for="huellas">Huellas</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="HVafore" v-model="asset.HVAfore"/>
            <label for="HVafore">Hypervisor Afore</label>
          </div>


        </div>
        <div class="form-row servicios-row">
          <div class="form-group servicio-check">
            <input type="checkbox" id="almacenamiento" v-model="asset.Almacenamiento"/>
            <label for="almacenamiento">Almacenamiento</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="biometrico" v-model="asset.Biometrico"/>
            <label for="biometrico">Biométrico</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="servchassis" v-model="asset.ServChassis"/>
            <label for="servchassis">Chassis</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="fabric" v-model="asset.Fabric"/>
            <label for="fabric">Fabric</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="hypervisor" v-model="asset.Hypervisor"/>
            <label for="hypervisor">HYPERVISOR</label>
          </div>
          <div class="form-group servicio-check">
            <input type="checkbox" id="switchMDS" v-model="asset.SwitchMDS"/>
            <label for="switchMDS">Switch MDS</label>
          </div>
        </div>

      </div>

      <!-- Sección 2: Fechas -->
      <div class="form-section">
        <h2>Fechas</h2>
        <div class="form-row">
          <!-- Campo: Fecha de Estatus -->
          <div class="form-group">
            <label for="statusDate">Fecha de Estatus:</label>
            <input type="date" id="statusDate" v-model="asset.FechaEstatus" required />
          </div>

          <!-- Campo: Fecha Inicio Soporte -->
          <div class="form-group">
            <label for="fechaInicioSoporte">Fecha de Inicio de Soporte:</label>
            <input type="date" id="fechaInicioSoporte" v-model="asset.FechaInicioSoporte" required />
          </div>

          <!-- Campo: Fecha Fin Soporte -->
          <div class="form-group">
            <label for="fechaFinSoporte">Fecha de Fin de Soporte:</label>
            <input type="date" id="fechaFinSoporte" v-model="asset.FechaFinSoporte" required />
          </div>

          <!-- Campo: Fecha Fin Vida -->
          <div class="form-group">
            <label for="fechaFinVida">Fecha de Fin de Vida:</label>
            <input type="date" id="fechaFinVida" v-model="asset.FechaFinVida" required />
          </div>
        </div>
      </div>

      <!-- Sección 3: Características del Activo -->
      <div class="form-section">
        <h2>Características del Activo</h2>
        <!-- Fila 1 -->
        <div class="form-row">
          
          <!-- Campo: Rack -->
          <div class="form-group">
            <label for="rack">Rack:</label>
            <select id="rack" v-model="asset.Rack" required>
              <option v-for="option in catalogOptions.Racks" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Unidad de Rack -->
          <div class="form-group">
            <label for="unidadRack">Unidad de Rack:</label>
            <input type="text" id="unidadRack" v-model="asset.UnidadRack" required />
          </div>

          <!-- Campo: Sistema Operativo -->
          <div class="form-group">
            <label for="sistema">Sistema Operativo:</label>
            <select id="sistema" v-model="asset.Sistema" required>
              <option v-for="option in catalogOptions.OSs" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Procesador -->
          <div class="form-group">
            <label for="cpu">Procesador:</label>
            <select id="cpu" v-model="asset.Procesador" required>
              <option v-for="option in catalogOptions.CPUs" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Cantidad de Procesadores -->
          <div class="form-group">
            <label for="cantCpus">Cantidad de Procesadores:</label>
            <select id="cantCpus" v-model="asset.CantCPUs" required>
              <option v-for="option in catalogOptions.CantCPUs" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Nucleos por Procesador -->
          <div class="form-group">
            <label for="nucleos">Nucleos por Procesador:</label>
            <select id="nucleos" v-model="asset.Nucleos" required>
              <option v-for="option in catalogOptions.Nucleos" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

        </div>

        <!-- Fila 2 -->
        <div class="form-row">

          <!-- Campo: Unidad de Almacenamiento -->
          <div class="form-group">
            <label for="unidadAlmac">Unidad de Almacenamiento:</label>
            <select id="unidadAlmac" v-model="asset.UnidadAlmac" required>
              <option v-for="option in catalogOptions.UnidsAlmac" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Cantidad de Unidades -->
          <div class="form-group">
            <label for="cantUnids">Cantidad de Unidades:</label>
            <select id="cantUnids" v-model="asset.CantUnids" required>
              <option v-for="option in catalogOptions.CantUnidAlmac" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Capacidad por Unidad -->
          <div class="form-group">
            <label for="capacUnidad">Capacidad por Unidad:</label>
            <select id="capacUnidad" v-model="asset.CapacidadAlmac" required>
              <option v-for="option in catalogOptions.CapacidadAlmac" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Cantidad de Modulos RAM -->
          <div class="form-group">
            <label for="cantRAM">Cantidad de Módulos RAM:</label>
            <select id="cantRAM" v-model="asset.CantRAM" required>
              <option v-for="option in catalogOptions.CantRAM" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Capacidad por Modulo -->
          <div class="form-group">
            <label for="capacRAM">Capacidad por Módulo:</label>
            <select id="capacRAM" v-model="asset.CapacidadRAM" required>
              <option v-for="option in catalogOptions.CapacidadRAM" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <!-- Campo: Tipo de RAM -->
          <div class="form-group">
            <label for="tipoRAM">Tipo de Módulos:</label>
            <select id="tipoRAM" v-model="asset.TipoRAM" required>
              <option v-for="option in catalogOptions.TipoRAM" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>
        </div>

        <!-- Fila 3 -->
        <div class="form-row">

          <!-- Campo: IP Red -->
          <div class="form-group">
            <label for="ipRed">IP Red:</label>
            <input type="text" id="ipRed" v-model="asset.IpRed" required />
          </div>
          
          <!-- Campo: IP ILO -->
          <div class="form-group">
            <label for="ipILO">IP ILO:</label>
            <input type="text" id="ipILO" v-model="asset.IpILO" required />
          </div>

          <!-- Campo: Dueño (Catálogo) -->
          <div class="form-group">
            <label for="dueño">Dueño:</label>
            <select id="dueño" v-model="asset.Dueño" required>
              <option v-for="option in catalogOptions.Dueños" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

        </div>

      </div>

      <!-- Botones de Acción -->
      <div class="form-actions">
        <button style="background-color: rgb(0, 180, 0);" type="button" class="massive-load-button" @click="redirectToMassiveLoad">Carga Masiva</button>
        <button type="button" @click="deleteAsset" :disabled="!activo" >Eliminar Activo</button>
        <button type="submit" @click="submit">{{ existe ? 'Actualizar' : 'Agregar' }} Activo</button>
      </div>
    </form>
  </div>

</template>

<script>
  import Header from "@/components/Header.vue";
  import axios from 'axios';

   export default {
    components: {
    Header,
    },
    data() {
      return {
        existe: false,
        activo: false,
        asset: {
        Id: null,
        Serial: '',
        Nombre: '',
        Encendido: '',
        Estatus: '',
        FechaEstatus: '',
        Cluster: '',
        Chassis: '',
        Bahia: '',
        Modelo: '',
        Servicio: 'Afore',
        FechaInicioSoporte: '',
        FechaFinSoporte: '',
        FechaFinVida: '',
        IpRed: '',
        IpILO: '',
        CantCPUs: '',
        Nucleos: '',
        CantUnids: '',
        CapacidadAlmac: '',
        CantRAM: '',
        CapacidadRAM: '',
        TipoRAM: '',
        UnidadRack: '',
        Sitio: '',
        Ambiente: '',
        Tipo: '',
        Marca: '',
        Dueño: '',
        Procesador: '',
        UnidadAlmac: '',
        Sistema: '',
        Rack: '',
        Afore: '',
        BanCoppel: '',
        Cartera: '',
        ETL: '',
        Huellas: '',
        HVAfore: '',
        Almacenamiento: '',
        Biometrico: '',
        ServChassis: '',
        Fabric: '',
        Hypervisor: '',
        SwitchMDS: '',
        Afore: '',
        BanCoppel: '',
        Cartera: '',
        ETL: '',
        Huellas: '',
        HVAfore: '',
        Almacenamiento: '',
        Biometrico: '',
        ServChassis: '',
        Fabric: '',
        Hypervisor: '',
        SwitchMDS: '',
        },
      catalogOptions: {
        CantCPUs: [1, 2, 3, 4, 5, 6],
        Nucleos: [1, 2, 4, 6, 8, 12, 16, 24, 32],
        CantUnidAlmac: [1, 2, 3, 4, 5, 6, 7, 8],
        CapacidadAlmac: ["500GB", "1TB", "2TB", "4TB", "8TB"],
        CantRAM: [1, 2, 3, 4, 5, 6, 7, 8],
        CapacidadRAM: ["4GB", "8GB", "16GB", "32GB", "64GB", "128GB"],
        TipoRAM: ["DDR3", "DDR4", "DDR5"],
        Encendido: ["Si", "No"],
        Sitios: [],
        Ambientes: [],
        Tipos: [],
        Marcas: [],
        Dueños: [],
        UnidsAlmac: [],
        CPUs: [],
        OSs: [],
        Racks: [],
      }
      };
    },
    async mounted() {
      await this.loadCatalogOptions('Sitios', 'Sitios');
      await this.loadCatalogOptions('Ambientes', 'Ambientes');
      await this.loadCatalogOptions('Tipos', 'Tipos');
      await this.loadCatalogOptions('Marcas', 'Marcas');
      await this.loadCatalogOptions('Dueños', 'Dueños');
      await this.loadCatalogOptions('Procesadores', 'CPUs');
      await this.loadCatalogOptions('UnidadesAlmac', 'UnidsAlmac');
      await this.loadCatalogOptions('SisOperativos', 'OSs');
      await this.loadCatalogOptions('Racks', 'Racks');
    },
    methods: {
      async loadCatalogOptions(tabla, key) {
        try {
          const response = await axios.get(`http://localhost:5000/api/options/${tabla}`);
          this.catalogOptions[key] = response.data;
          console.log(`Opciones de ${tabla} cargadas correctamente`);
          console.log(response.data);
        } catch (error) {
          console.error(`Error al cargar opciones de ${tabla}:`, error);
        }
      },
      // Verifica si el activo ya existe
      async buscarActivo() {
      try {
        if (this.asset.Serial) {
          const response = await axios.post('http://localhost:5000/api/activo', {
            serial: this.asset.Serial
          });

          const assetData = response.data;
          console.log(assetData);

          if (assetData && assetData.length > 0) {
            // Obtiene los campos del activo (0 es la primer y unica fila)

            this.asset.Id = assetData[0][0];
            this.asset.Nombre = assetData[0][2];
            this.asset.Encendido = assetData[0][3];
            if (assetData[0][3]) {
              this.asset.Encendido = "Si";
            } else {
              this.asset.Encendido = "No";
            }
            this.asset.Estatus = assetData[0][4];
            const fechaEstatus = new Date(assetData[0][5]);
            this.asset.FechaEstatus = fechaEstatus.toISOString().split('T')[0];
            this.asset.Cluster = assetData[0][8];
            this.asset.Chassis = assetData[0][9];
            this.asset.Bahia = assetData[0][10];
            this.asset.Modelo = assetData[0][12];
            const fechaInicioSoporte = new Date(assetData[0][15]);
            this.asset.FechaInicioSoporte = fechaInicioSoporte.toISOString().split('T')[0];
            const fechaFinSoporte = new Date(assetData[0][16]);
            this.asset.FechaFinSoporte = fechaFinSoporte.toISOString().split('T')[0];
            const fechaFinVida = new Date(assetData[0][17]);
            this.asset.FechaFinVida = fechaFinVida.toISOString().split('T')[0];
            this.asset.IpRed = assetData[0][18];
            this.asset.IpILO = assetData[0][19];
            this.asset.CantCPUs = assetData[0][22];
            this.asset.Nucleos = assetData[0][23];
            this.asset.CantUnids = assetData[0][25];
            this.asset.CapacidadAlmac = assetData[0][26];
            this.asset.CantRAM = assetData[0][27];
            this.asset.CapacidadRAM = assetData[0][28];
            this.asset.TipoRAM = assetData[0][29];
            this.asset.UnidadRack = assetData[0][32];


            this.asset.Sitio = assetData[0][33];
            this.asset.Ambiente = assetData[0][34];
            this.asset.Tipo = assetData[0][35];
            this.asset.Marca = assetData[0][36];
            //this.asset.Servicio = assetData[0][37];
            this.asset.Dueño = assetData[0][38];
            this.asset.Procesador = assetData[0][39];
            this.asset.UnidadAlmac = assetData[0][40];
            this.asset.Sistema = assetData[0][41];
            this.asset.Rack = assetData[0][42];

            this.existe = true;
            if (this.asset.Estatus === "Activo") {
              this.activo = true;
            }

          } else {
            console.log("No se encontró el activo");
            this.existe = false;
            this.activo = false;
          }

          this.buscarServicios();
        }
      } catch (error) {
        console.error("Error al obtener el activo:", error);
      }
    },
    async buscarServicios() {
      try {
        if (this.asset.Serial) {
          const response = await axios.post('http://localhost:5000/api/servicios', {
            serial: this.asset.Serial
          });
          
          response.data;

          this.asset.Afore = response.data.afore;
          this.asset.BanCoppel = response.data.bancoppel;
          this.asset.Cartera = response.data.cartera;
          this.asset.ETL = response.data.etl;
          this.asset.Huellas = response.data.huellas;
          this.asset.HVAfore = response.data.hvafore;
          this.asset.Almacenamiento = response.data.almacenamiento;
          this.asset.Biometrico = response.data.biometrico;
          this.asset.ServChassis = response.data.chassis;
          this.asset.Fabric = response.data.fabric;
          this.asset.Hypervisor = response.data.hypervisor;
          this.asset.SwitchMDS = response.data.switchmds;
        }
      } catch (error) {
        console.error("Error al obtener el activo:", error);
      }
    },
  async deleteAsset() {
    // Confirmación antes de eliminar
    if (!confirm("¿Está seguro de que desea eliminar el activo?")) {
      return; // Si el usuario elige "No", se cancela la acción
    }

    try {
      if (this.asset.Serial) {
        const response = await axios.put('http://localhost:5000/api/activo/eliminar', {
          serial: this.asset.Serial
        });

        const assetData = response.data;
        console.log(assetData);

        if (response.data.status === "ok") {
          // Obtiene los campos del activo (0 es la primer y unica fila)
          console.log("Se eliminó el activo");
          alert("Activo eliminado correctamente");
          this.reiniciarFormulario();
        } else {
          console.log("No se encontró el activo a eliminar");
          alert("No se encontró el activo a eliminar");
        }
      }
    } catch (error) {
      console.error("Error al eliminar el activo:", error);
    }
  },
  async submit() {
    // Confirmación antes de agregar o actualizar
    const confirmMessage = this.existe
      ? "¿Está seguro de que desea actualizar el activo?"
      : "¿Desea agregar el activo?";

    if (!confirm(confirmMessage)) {
      return; // Si el usuario elige "No", se cancela la acción
    }

    try {
      const data = {
        serial: this.asset.Serial,
        nombre: this.asset.Nombre,
        encendido: this.asset.Encendido,
        cluster: this.asset.Cluster,
        chassis: this.asset.Chassis,
        bahia: this.asset.Bahia,
        modelo: this.asset.Modelo,
        nucleos: this.asset.Nucleos,
        fechaInicioSoporte: this.asset.FechaInicioSoporte,
        fechaFinSoporte: this.asset.FechaFinSoporte,
        fechaFinVida: this.asset.FechaFinVida,
        ipRed: this.asset.IpRed,
        ipILO: this.asset.IpILO,
        cantCpus: this.asset.CantCPUs,
        cantUnidades: this.asset.CantUnids,
        capacidadAlmac: this.asset.CapacidadAlmac,
        cantModulosRam: this.asset.CantRAM,
        capacidadRam: this.asset.CapacidadRAM,
        tipoRam: this.asset.TipoRAM,
        unidadRack: this.asset.UnidadRack,

        sitio: this.asset.Sitio,
        ambiente: this.asset.Ambiente,
        tipo: this.asset.Tipo,
        marca: this.asset.Marca,
        servicio: this.asset.Servicio,
        dueño: this.asset.Dueño,
        procesador: this.asset.Procesador,
        unidadAlmac: this.asset.UnidadAlmac,
        sistema: this.asset.Sistema,
        rack: this.asset.Rack,

        afore: this.asset.Afore,
        bancoppel: this.asset.BanCoppel,
        cartera: this.asset.Cartera,
        ETL: this.asset.ETL,
        huellas: this.asset.Huellas,
        HVafore: this.asset.HVAfore,
        almacenamiento: this.asset.Almacenamiento,
        biometrico: this.asset.Biometrico,
        servchassis: this.asset.ServChassis,
        fabric: this.asset.Fabric,
        hypervisor: this.asset.Hypervisor,
        switchMDS: this.asset.SwitchMDS

      };

      let url = '';
      let message = '';
      
      if (this.existe) {
        url = 'http://localhost:5000/api/activos/actualizar';
        message = 'Activo actualizado correctamente';
      } else {
        url = 'http://localhost:5000/api/activos/agregar';
        message = 'Activo agregado correctamente';
      }

      const response = await axios.post(url, data);

      if (response.data.status === "ok") {
        alert(message);
        this.reiniciarFormulario();
      } else {
        alert(response.data.mensaje);
      }

    } catch (error) {
      console.error('Error al procesar el activo:', error);
      alert('Error al procesar el activo');
    }
  },
  async redirectToMassiveLoad() {
    this.$router.push('/CargaMasiva');
  },
  reiniciarFormulario(){
    this.asset = {
      Id: null,
      Serial: '',
      Nombre: '',
      Encendido: '',
      Estatus: '',
      FechaEstatus: '',
      Cluster: '',
      Chassis: '',
      Bahia: '',
      Modelo: '',
      Servicio: 'Afore',
      FechaInicioSoporte: '',
      FechaFinSoporte: '',
      FechaFinVida: '',
      IpRed: '',
      IpILO: '',
      CantCPUs: '',
      Nucleos: '',
      CantUnids: '',
      CapacidadAlmac: '',
      CantRAM: '',
      CapacidadRAM: '',
      TipoRAM: '',
      UnidadRack: '',
      Sitio: '',
      Ambiente: '',
      Tipo: '',
      Marca: '',
      Dueño: '',
      Procesador: '',
      UnidadAlmac: '',
      Sistema: '',
      Rack: '',
      Afore: '',
      BanCoppel: '',
      Cartera: '',
      ETL: '',
      Huellas: '',
      HVAfore: '',
      Almacenamiento: '',
      Biometrico: '',
      ServChassis: '',
      Fabric: '',
      Hypervisor: '',
      SwitchMDS: '',
      Afore: '',
      BanCoppel: '',
      Cartera: '',
      ETL: '',
      Huellas: '',
      HVAfore: '',
      Almacenamiento: '',
      Biometrico: '',
      ServChassis: '',
      Fabric: '',
      Hypervisor: '',
      SwitchMDS: '',
    };
    this.existe = false;
    this.activo = false;
  }
    }
  };
</script>

<style>
  .add-asset {
    padding: 8px;
  }

  .form-actions button:disabled {
    background-color: #ccc; /* Fondo gris */
    color: #666; /* Texto gris oscuro */
    cursor: not-allowed; /* Cambia el cursor para indicar que no es clickeable */
  }

  .form-section {
    margin-bottom: 6px;
    padding: 4px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .form-section h2 {
    margin-bottom: 7px;
    font-size: 20px;
    color: #333;
  }

  .form-row {
    display: grid;
    width: 99%;
    grid-template-columns: repeat(6, 1fr); /* 6 columnas */
    gap: 20px; /* Espacio entre columnas */
    margin-left: 10px;
    margin-bottom: 10px; /* Espacio entre filas */
  }

  .form-group {
    margin-bottom: 0; /* Elimina el margen inferior */
  }

  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
  }

  input,
  select {
    width: 100%;
    padding: 7px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  input[readonly] {
    background-color: #f0f0f0; /* Fondo gris claro para campos de solo lectura */
    cursor: not-allowed; /* Cambia el cursor para indicar que no es editable */
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-top: 20px;
    position: relative;
  }

  button {
    margin-right: 10px;
    padding: 10px 20px;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .form-actions button {
    padding: 10px 20px;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    transition: background-color 0.3s ease;
    margin-left: 10px;
  }

  /* Estilo para el botón de Eliminar cuando está habilitado */
  .form-actions button[type="button"]:not(:disabled) {
    background-color: #ff4444; /* Fondo rojo */
    color: white; /* Texto blanco */
  }

  /* Estilo para el botón de Eliminar cuando está deshabilitado */
  .form-actions button[type="button"]:disabled {
    background-color: #ccc; /* Fondo gris */
    color: #666; /* Texto gris oscuro */
    cursor: not-allowed; /* Cambia el cursor para indicar que no es clickeable */
  }

  /* Estilo para el botón de Agregar/Actualizar (azul) */
  .form-actions button[type="submit"] {
    background-color: #007bff; /* Fondo azul */
    color: white; /* Texto blanco */
  }

  /* Estilos para el modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Fondo oscuro semitransparente */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000; /* Asegura que el modal esté por encima de todo */
  }

  .modal {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .modal p {
    margin-bottom: 20px;
    font-size: 18px;
  }

  .modal button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .modal button:hover {
    background-color: #0056b3;
  }

  /* Aumentamos la especificidad */
  .form-actions .massive-load-button {
    position: absolute;
    left: 0;
    padding: 10px 20px;
    background-color: #28a745; /* Verde */
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }

  .form-actions .massive-load-button:hover {
    background-color: #218838; /* Verde oscuro al pasar el mouse */
  }

  /* Estilo para la fila de servicios */
.servicios-row {
  grid-template-columns: repeat(6, 1fr); /* Alineación similar a otras filas */
  gap: 10px; /* Espacio entre columnas de servicios */
  width: 55%;
  height: 70%;
}

.servicio-check {
  display: flex;
  align-items: center;
}

.servicio-check input {
  margin-right: 5px; /* Espacio entre el checkbox y el texto */
}

/* estilo de los checkboxes */
input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 3px;
  background-color: #fff;
  transition: background-color 0.3s ease;
}

input[type="checkbox"]:checked {
  background-color: #007bff;
}
</style>