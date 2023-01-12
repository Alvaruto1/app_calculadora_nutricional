from constants import NUTRICIONALES, SITUACION, OBJETIVOS

class CalculadorNutricional:
    
    @classmethod
    def solucion(cls, edad: int, peso: float):
        if not(5<=edad<=17):
            return {'message': 'la edad debe estar entre 5 y 17'}
        if peso<=0:
            return {'message': 'el peso debe ser un valor mayor a 0'}
        situacion_nutricional = cls.obtener_estado_nutricional(edad=edad, peso=peso)
        formula = cls.obtner_formula_necesarios_objetivo_nutricional(estado_nutricional_dict=situacion_nutricional, peso= peso)
        return {'dias': formula['dias'], 'situacion_nutricional_actual': situacion_nutricional, 'receta': formula['receta']}

    @classmethod
    def obtener_estado_nutricional(cls, edad: int, peso: float) -> dict:
        estado_nutricional = {}
        objetivo_dict = list(filter(lambda objetivo: objetivo['rango_edad'][0]<=edad<=objetivo['rango_edad'][1] ,OBJETIVOS))[0]
        if peso < objetivo_dict['desnutricion']:
            estado_nutricional = {'tipo' : 'desnutricion', 'objetivo': objetivo_dict['objetivo']['A']}
        elif peso > objetivo_dict['sobrepeso']:
            estado_nutricional = {'tipo' : 'sobrepeso', 'objetivo': objetivo_dict['objetivo']['B']}
        else:
            estado_nutricional = {'tipo' : 'peso saludable', 'objetivo': objetivo_dict['objetivo']['C']}        

        return estado_nutricional

    @classmethod
    def formula_composicion_nutricional(cls, estado_nutricional: str) -> dict:
        situacion_nutricional = list(filter(lambda situacion: situacion['situacion'] == estado_nutricional, SITUACION))[0]    
        return {'valor': situacion_nutricional['pp']*NUTRICIONALES['p']+situacion_nutricional['pc']*NUTRICIONALES['c']+situacion_nutricional['pv']*NUTRICIONALES['v'], 'receta': {'porciones': situacion_nutricional, 'cantidad': NUTRICIONALES}}

    @classmethod
    def obtner_formula_necesarios_objetivo_nutricional(cls, estado_nutricional_dict: dict, peso: float) -> dict:
        total_peso = peso
        dias = 0
        situacion_nutricional = list(filter(lambda situacion: situacion['situacion'] == 'peso saludable', SITUACION))[0] 
        receta = {'porciones': situacion_nutricional, 'cantidad': NUTRICIONALES}
        while (estado_nutricional_dict['objetivo'] > total_peso and estado_nutricional_dict['tipo']=='desnutricion') or (estado_nutricional_dict['objetivo'] < total_peso and estado_nutricional_dict['tipo']=='sobrepeso'):
            formula = cls.formula_composicion_nutricional(estado_nutricional=estado_nutricional_dict['tipo'])
            total_peso += formula['valor']
            dias += 1
            receta = formula['receta']
        return {'dias': dias, 'receta': receta} 