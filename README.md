# Amplificador de transimpedancia (TIA) paso banda de bajo ruido — LT1793

Repositorio público (`senisius/ao-low-noise-current-amplifier`) con las fuentes mínimas para abrir y compilar el proyecto jerárquico de simulación en **Keysight ADS 2027** y el proyecto de captura esquemática y librerías en **Altium Designer** (revisión 2).

- Proyecto ADS 2027 jerárquico: [`ads_migration/workspace/ao_bajo_ruido_real_wrk/`](ads_migration/workspace/ao_bajo_ruido_real_wrk/) ([`lib.defs`](ads_migration/workspace/ao_bajo_ruido_real_wrk/lib.defs))
- Proyecto Altium Designer rev. 2: [`altium_tia/TIA_LT1793.PrjPcb`](altium_tia/TIA_LT1793.PrjPcb) ([`TIA_LT1793.SchDoc`](altium_tia/TIA_LT1793.SchDoc))

---

## 1. Objetivo

Validar en simulación eléctrica el comportamiento en banda pasante, la respuesta en frecuencia y el efecto de componentes comerciales reales y parásitas de montaje de un **amplificador de transimpedancia (TIA) paso banda de bajo ruido** basado en el amplificador operacional JFET **LT1793** (`100 kΩ` / `100 dBΩ`), antes de pasar a diseño físico de placa (layout/PCB).

La ganancia de referencia en banda pasante está normalizada a `0 dB` para una corriente de entrada de `10 µA AC` sobre `100 kΩ` (`1 V` a la salida).

---

## 2. Topología y ajustes

El circuito consta de una etapa TIA inversora seguida de dos filtros pasivos en cascada (paso alto y paso bajo) con frecuencia de corte regulable mediante potenciómetros multivuelta conectados como reóstatos:

1. **Etapa TIA (`U1 = LT1793CS8#PBF`, alimentación `±15 V`):**
   - Realimentación principal: `R_F = 100 kΩ ±0,05 %` (`PTFR0805A100KN9`) en paralelo con `C_F = 4,7 pF` NP0 (`CC0603BRNPO9BN4R7`).
   - Parásita de placa modelada en ADS: `C_STRAY_F = 0,25 pF` en paralelo con `C_F`.
2. **Filtro paso alto pasivo (corte inferior `f_c_low`):**
   - Condensador de acoplo: `C_HP = C_HP1 // C_HP2 = 2 × 100 nF` C0G (`1206N104J500CT`, `200 nF` totales).
   - Rama serie a `GND`: `R_HP = 1,2 kΩ ±0,05 %` (`PTFR0603A1K20N9`) + potenciómetro reóstato `P_HP` (`Bourns 3224W-1-104E`, `0–100 kΩ`, resistencia residual modelada `R_end_hp = 50 Ω`, inductancia de pista/terminal `L_PHP = 5 nH`).
3. **Filtro paso bajo pasivo (corte superior `f_c_high`):**
   - Rama serie: `R_LP = 150 Ω ±0,05 %` (`PTFR0603A150RP9`) + potenciómetro reóstato `P_LP` (`Bourns 3224W-1-502E`, `0–5 kΩ`, `R_end_lp = 5 Ω`, `L_PLP = 5 nH`).
   - Condensador a `GND`: `C_LP = 820 pF ±1 %` C0G (`GCM1885C2A821FA16D`) con parásita de placa modelada `C_STRAY_LP = 1,0 pF`.
4. **Desacoplo de alimentación (`±15 V`):**
   - Por raíl (`VCC` y `VEE`): `100 nF` C0G (`1206N104J500CT`) + `10 µF / 35 V` tantalio (`KEMET T491D106K035AT`), con impedancia de pista compartida modelada en ADS (`Ltrk = 5 nH`, `Rtrk = 0,05 Ω`).
5. **Conectores y punto de prueba:**
   - Entrada y salida (`J_IN`, `J_OUT`): en Altium usan la huella dual `TRIAX_BNC_DUAL` compatible con conector BNC (`cntitle BNC-KWE-6`) / triaxial; en ADS la celda `CON_CNTITLE_BNC_KWE_6` modela continuidad ideal explícita (`ads_rflib:Short`) entre los nodos externos y la placa con blindajes a `GND`.
   - En [`altium_tia/TIA_LT1793.SchDoc`](altium_tia/TIA_LT1793.SchDoc) (hoja A3, rev. 2) hay **16 piezas de compra** (11 referencias MPN únicas) más un punto de prueba pasante metalizado `TP1` (`TP_PTH_D1R0_P2R0`, *Standard No BOM*, taladro `1,0 mm`, pad `2,0 mm`) conectado a la red `TIA_OUT`.

### Ajustes de potenciómetros (`VAR1` en ADS)

- **Punto nominal:** `P_HP = 10 kΩ`, `P_LP = 500 Ω`.
- **Rango de sintonía:** `P_HP ∈ [0, 100 kΩ]` (paso de tuning `500 Ω`) y `P_LP ∈ [0, 5 kΩ]` (paso de tuning `50 Ω`).

---

## 3. Resultados nominales simulados (ADS 2027 jerárquico)

Simulación AC pequeña señal y ruido en `ao_bajo_ruido_real_hier` (`0,1 Hz – 10 MHz`, `200 pts/década`, `1601` puntos, `Temp = 27 °C`, salida `out` en circuito abierto):

| Parámetro (`P_HP = 10 kΩ`, `P_LP = 500 Ω`) | Valor simulado |
|---|---|
| Ganancia máxima normalizada (`Vout_max`) | `-0,03866 dB` (~`3,94 kHz`) |
| Transimpedancia máxima (`Zmax`) | `99,961 dBΩ` (`~99,56 kΩ`) |
| Corte inferior `-3,01 dB` (`f_c_low`) | `70,715 Hz` |
| Corte superior `-3,01 dB` (`f_c_high`) | `200,969 kHz` |
| Ancho de banda (`BW`) | `200,898 kHz` |
| Densidad de ruido en banda (`out`, `1 kHz`, modelo conductual `U1`) | `~40,9 nV/√Hz` |
| Ruido RMS integrado (`10 Hz – 300 kHz`) | `18,306 µV` |
| Ruido RMS entre cortes `-3 dB` (`70,71 Hz – 200,97 kHz`) | `16,473 µV` |
| Ruido RMS en el barrido (`0,1 Hz – 10 MHz`) | `20,526 µV` |

### Rango simulado en esquinas de potenciómetros `(P_HP, P_LP)`

- `(0 Ω, 0 Ω)`: `Vout_max = -0,05474 dB`, `631,37 Hz .. 309,75 kHz`
- `(0 Ω, 5 kΩ)`: `Vout_max = -0,18338 dB`, `613,49 Hz .. 38,53 kHz`
- `(100 kΩ, 0 Ω)`: `Vout_max = -0,03591 dB`, `7,83 Hz .. 308,61 kHz`
- `(100 kΩ, 5 kΩ)`: `Vout_max = -0,03752 dB`, `7,83 Hz .. 37,32 kHz`

---

## 4. Límites y alcance

- **Contenido publicado:** este repositorio contiene **únicamente** los archivos fuente mínimos para abrir y compilar el workspace jerárquico de ADS 2027 y el proyecto esquemático de Altium rev. 2. **No** incluye archivos Data Display (`.dds`), datasets (`.ds`), configuraciones de preferencias de interfaz, listados BOM, documentos PDF ni capturas/renders.
- **Estado del diseño PCB:** **no** hay diseño de placa (`PcbDoc`), ruteado, archivos Gerber ni PCB fabricada en este repositorio. La alimentación (`VCC`, `VEE`, `GND`) está definida mediante puertos de esquema sin conector físico asignado todavía, y la revisión de huellas y reglas de máscara/pasta queda pendiente antes de generar la placa.
- **Aproximación del operacional `U1` en ADS:** la subcelda `LT1793CS8_APPROX_OPAMP5` utiliza el bloque conductual `ads_pelib:OpAmp5` (`GBW = 4,2 MHz`, polo único, ruido blanco plano `Vnoise = 5,9 nV/√Hz` e `Inoise = 1 fA/√Hz`). **No** es el modelo oficial de fabricante Analog Devices del LT1793: omite esquina `1/f`, corriente de ruido dependiente de la frecuencia, etapa de salida VDMOS, rangos reales de modo común y límites de saturación.
- **Condiciones de contorno no modeladas:** no se incluye capacidad parásita del sensor o cable a la entrada (`C_in`), la salida `out` se simula en circuito abierto (sin carga resistiva/capacitiva de instrumento o ADC ni terminación de `50 Ω`), y los conectores `J_IN`/`J_OUT` se modelan como cortos ideales sin parásitas de montaje. Por ello, el ancho de banda superior y el ruido RMS simulados representan una cota optimista del circuito aislado.

---

## 5. Carpetas y archivos publicados

| Ruta | Contenido |
|---|---|
| [`README.md`](README.md) | Documentación general del repositorio público (este archivo). |
| [`ads_migration/workspace/ao_bajo_ruido_real_wrk/`](ads_migration/workspace/ao_bajo_ruido_real_wrk/) | Workspace ADS 2027 (`67` archivos): [`lib.defs`](ads_migration/workspace/ao_bajo_ruido_real_wrk/lib.defs), [`cds.lib`](ads_migration/workspace/ao_bajo_ruido_real_wrk/cds.lib), [`de_sim.cfg`](ads_migration/workspace/ao_bajo_ruido_real_wrk/de_sim.cfg), [`hpeesofsim.cfg`](ads_migration/workspace/ao_bajo_ruido_real_wrk/hpeesofsim.cfg), metadatos de `ao_bajo_ruido_real_lib`, celda principal [`ao_bajo_ruido_real_hier`](ads_migration/workspace/ao_bajo_ruido_real_wrk/ao_bajo_ruido_real_lib/ao_bajo_ruido_real_hier/schematic/sch.oa) y sus `12` subceldas jerárquicas (`itemdef.py`, símbolos y esquemáticos `.oa`). |
| [`altium_tia/`](altium_tia/) | Proyecto Altium Designer rev. 2 (`6` archivos): [`TIA_LT1793.PrjPcb`](altium_tia/TIA_LT1793.PrjPcb), [`TIA_LT1793.PrjPcbStructure`](altium_tia/TIA_LT1793.PrjPcbStructure), [`TIA_LT1793.SchDoc`](altium_tia/TIA_LT1793.SchDoc), [`TIA_LT1793.SchLib`](altium_tia/TIA_LT1793.SchLib), [`TIA_LT1793.PcbLib`](altium_tia/TIA_LT1793.PcbLib) y [`TIA_LT1793_TP.PcbLib`](altium_tia/TIA_LT1793_TP.PcbLib) (con metadatos de rutas locales e impresora saneados para publicación). |
