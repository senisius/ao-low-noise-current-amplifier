"""Definicion de parametros de celda (item definition) generada por build_ao_real_hier_workspace.py.

ADS ejecuta create_itemdef al abrir la celda (libreria con PYTHON_ENABLED=TRUE). Es lo que hace persistentes los
parametros de celda entre sesiones.
"""
from keysight.ads import de


def create_itemdef(cell: de.Cell) -> None:
    def P(name, default):
        p = de.db.ModelParam(name, name, unit_type=de.db.ModelUnitType.NO_UNIT, param_type=de.db.ModelParamType.REAL)
        p.default_value = de.db.std_string_param(default)
        return p

    m = de.db.ModelDef(cell.name, cell.name)
    m.inst_name_prefix = "X"
    m.is_sub_design = True
    m.parameters = [P(n, v) for n, v in [('Vdc', '15 V'), ('Ltrk', '5 nH'), ('Rtrk', '0.05 Ohm')]]
    de.add_model_definition(cell.library, m)
