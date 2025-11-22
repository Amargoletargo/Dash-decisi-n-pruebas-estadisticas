import streamlit as st
import json

# Configuración de la página
st.set_page_config(
    page_title="Selector de Pruebas Estadísticas",
    page_icon="📊",
    layout="wide"
)

# Datos de las pruebas estadísticas
pruebas_estadisticas = {
    "t_student_independientes": {
        "nombre": "t de Student (independientes)",
        "tipo": "Paramétrica",
        "supuestos": [
            "La variable es numérica",
            "Los datos siguen una distribución normal",
            "La variabilidad en ambos grupos es similar"
        ],
        "uso": "Se comparan dos grupos distintos y se necesita que los datos sean 'ordenados' y comparables."
    },
    "t_student_relacionadas": {
        "nombre": "t de Student (relacionadas)",
        "tipo": "Paramétrica",
        "supuestos": [
            "Datos emparejados (misma persona antes-después)",
            "Variable numérica",
            "Las diferencias entre mediciones siguen una distribución normal",
            "No hay valores extremos raros"
        ],
        "uso": "Se analiza el cambio dentro del mismo individuo."
    },
    "u_mann_whitney": {
        "nombre": "U de Mann-Whitney",
        "tipo": "No paramétrica",
        "supuestos": [
            "Las muestras se seleccionan aleatoriamente",
            "Observaciones independientes",
            "Variable ordinal o numérica",
            "No muchos empates al ordenar los datos"
        ],
        "uso": "Compara dos grupos sin requerir normalidad, usando el orden de los datos."
    },
    "chi_cuadrada": {
        "nombre": "Chi cuadrada",
        "tipo": "No paramétrica",
        "supuestos": [
            "Datos categóricos",
            "Observaciones independientes",
            "La mayoría de las celdas con frecuencias esperadas ≥ 5"
        ],
        "uso": "Se analiza si dos categorías están relacionadas."
    },
    "wilcoxon": {
        "nombre": "Wilcoxon",
        "tipo": "No paramétrica",
        "supuestos": [
            "Datos emparejados",
            "Variable ordinal o continua",
            "Diferencias distribuidas de forma más o menos simétrica"
        ],
        "uso": "Sustituto de la t relacionada cuando no hay normalidad."
    },
    "anova_un_factor": {
        "nombre": "ANOVA de un factor",
        "tipo": "Paramétrica",
        "supuestos": [
            "Variable numérica",
            "Datos normales en cada grupo",
            "Varianzas similares",
            "Observaciones independientes"
        ],
        "uso": "Compara 3 o más grupos distintos."
    },
    "kruskal_wallis": {
        "nombre": "Kruskal-Wallis",
        "tipo": "No paramétrica",
        "supuestos": [
            "Observaciones independientes",
            "Variable ordinal o superior",
            "Grupos con distribuciones similares"
        ],
        "uso": "Versión no paramétrica del ANOVA."
    },
    "correlacion_pearson": {
        "nombre": "Correlación de Pearson",
        "tipo": "Paramétrica",
        "supuestos": [
            "Variables numéricas continuas",
            "Relación lineal",
            "Distribución normal conjunta",
            "Varianza similar a lo largo de los valores"
        ],
        "uso": "Mide relación lineal entre dos variables."
    },
    "correlacion_spearman": {
        "nombre": "Correlación de Spearman",
        "tipo": "No paramétrica",
        "supuestos": [
            "Variables ordinales o continuas",
            "Relación monotónica (si una sube, la otra sube o baja constantemente)",
            "Datos independientes"
        ],
        "uso": "Mide relación sin requerir linealidad ni normalidad."
    },
    "regresion_lineal": {
        "nombre": "Regresión lineal simple",
        "tipo": "Paramétrica",
        "supuestos": [
            "Relación lineal clara entre variables",
            "Errores independientes entre sí",
            "Variabilidad constante de los errores",
            "Errores con distribución normal",
            "Muestra seleccionada aleatoriamente"
        ],
        "uso": "Permite predecir una variable según la otra."
    }
}

def mostrar_resultado(prueba_key):
    """Muestra el resultado final con la prueba recomendada"""
    prueba = pruebas_estadisticas[prueba_key]
    
    st.success("✅ Prueba estadística recomendada")
    st.markdown(f"## 🎯 {prueba['nombre']}")
    st.markdown(f"**Tipo:** {prueba['tipo']}")
    
    st.markdown("### 📋 Supuestos que debe cumplir:")
    for supuesto in prueba['supuestos']:
        st.markdown(f"- {supuesto}")
    
    st.info(f"**📖 Cuándo usar:** {prueba['uso']}")

def main():
    st.title("📊 Selector de Pruebas Estadísticas")
    st.markdown("---")
    st.markdown("### Responde las siguientes preguntas para determinar la prueba estadística adecuada")
    
    # Inicializar session state
    if 'paso' not in st.session_state:
        st.session_state.paso = 1
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}
    
    # Paso 1: Objetivo del análisis
    if st.session_state.paso == 1:
        st.markdown("#### Paso 1: ¿Cuál es tu objetivo de análisis?")
        objetivo = st.radio(
            "Selecciona una opción:",
            [
                "Comparar grupos",
                "Analizar relaciones entre variables",
                "Predecir una variable"
            ],
            key="objetivo"
        )
        
        if st.button("Siguiente →"):
            st.session_state.respuestas['objetivo'] = objetivo
            st.session_state.paso = 2
            st.rerun()
    
    # Paso 2: Preguntas según objetivo
    elif st.session_state.paso == 2:
        objetivo = st.session_state.respuestas['objetivo']
        
        if objetivo == "Comparar grupos":
            st.markdown("#### Paso 2: Características de tus datos")
            
            tipo_dato = st.radio(
                "¿Qué tipo de datos tienes?",
                ["Numéricos/Continuos", "Categóricos/Nominales", "Ordinales"],
                key="tipo_dato"
            )
            
            if tipo_dato == "Categóricos/Nominales":
                if st.button("Ver resultado"):
                    mostrar_resultado("chi_cuadrada")
                    if st.button("🔄 Reiniciar"):
                        st.session_state.paso = 1
                        st.session_state.respuestas = {}
                        st.rerun()
            else:
                cuantos_grupos = st.radio(
                    "¿Cuántos grupos vas a comparar?",
                    ["2 grupos", "3 o más grupos"],
                    key="cuantos_grupos"
                )
                
                if st.button("Siguiente →"):
                    st.session_state.respuestas['tipo_dato'] = tipo_dato
                    st.session_state.respuestas['cuantos_grupos'] = cuantos_grupos
                    st.session_state.paso = 3
                    st.rerun()
        
        elif objetivo == "Analizar relaciones entre variables":
            st.markdown("#### Paso 2: Tipo de variables")
            
            tipo_variables = st.radio(
                "¿Qué tipo de variables tienes?",
                ["Ambas numéricas continuas", "Ordinales o mixtas"],
                key="tipo_variables"
            )
            
            if st.button("Siguiente →"):
                st.session_state.respuestas['tipo_variables'] = tipo_variables
                st.session_state.paso = 3
                st.rerun()
        
        elif objetivo == "Predecir una variable":
            st.markdown("#### Paso 2: Características de la predicción")
            
            st.info("Para predicción, necesitas una relación lineal clara entre variables")
            
            if st.button("Ver resultado"):
                mostrar_resultado("regresion_lineal")
                if st.button("🔄 Reiniciar"):
                    st.session_state.paso = 1
                    st.session_state.respuestas = {}
                    st.rerun()
        
        if st.button("← Atrás"):
            st.session_state.paso = 1
            st.rerun()
    
    # Paso 3: Preguntas adicionales
    elif st.session_state.paso == 3:
        objetivo = st.session_state.respuestas['objetivo']
        
        if objetivo == "Comparar grupos":
            tipo_dato = st.session_state.respuestas['tipo_dato']
            cuantos_grupos = st.session_state.respuestas['cuantos_grupos']
            
            if cuantos_grupos == "2 grupos":
                st.markdown("#### Paso 3: Relación entre grupos")
                
                relacion = st.radio(
                    "¿Los grupos son?",
                    ["Independientes (diferentes personas/sujetos)", "Relacionados/Emparejados (mismas personas antes-después)"],
                    key="relacion"
                )
                
                if st.button("Siguiente →"):
                    st.session_state.respuestas['relacion'] = relacion
                    st.session_state.paso = 4
                    st.rerun()
            
            else:  # 3 o más grupos
                st.markdown("#### Paso 3: Distribución de datos")
                
                normalidad = st.radio(
                    "¿Tus datos siguen una distribución normal y tienen varianzas similares?",
                    ["Sí", "No o no estoy seguro/a"],
                    key="normalidad"
                )
                
                if st.button("Ver resultado"):
                    if normalidad == "Sí":
                        mostrar_resultado("anova_un_factor")
                    else:
                        mostrar_resultado("kruskal_wallis")
                    
                    if st.button("🔄 Reiniciar"):
                        st.session_state.paso = 1
                        st.session_state.respuestas = {}
                        st.rerun()
        
        elif objetivo == "Analizar relaciones entre variables":
            tipo_variables = st.session_state.respuestas['tipo_variables']
            
            st.markdown("#### Paso 3: Características de la relación")
            
            if tipo_variables == "Ambas numéricas continuas":
                normalidad = st.radio(
                    "¿Tus variables siguen una distribución normal y tienen relación lineal?",
                    ["Sí", "No o no estoy seguro/a"],
                    key="normalidad_correlacion"
                )
                
                if st.button("Ver resultado"):
                    if normalidad == "Sí":
                        mostrar_resultado("correlacion_pearson")
                    else:
                        mostrar_resultado("correlacion_spearman")
                    
                    if st.button("🔄 Reiniciar"):
                        st.session_state.paso = 1
                        st.session_state.respuestas = {}
                        st.rerun()
            
            else:  # Ordinales o mixtas
                if st.button("Ver resultado"):
                    mostrar_resultado("correlacion_spearman")
                    if st.button("🔄 Reiniciar"):
                        st.session_state.paso = 1
                        st.session_state.respuestas = {}
                        st.rerun()
        
        if st.button("← Atrás"):
            st.session_state.paso = 2
            st.rerun()
    
    # Paso 4: Decisión final para comparación de 2 grupos
    elif st.session_state.paso == 4:
        relacion = st.session_state.respuestas['relacion']
        
        st.markdown("#### Paso 4: Supuestos paramétricos")
        
        normalidad = st.radio(
            "¿Tus datos cumplen con normalidad y varianzas similares?",
            ["Sí", "No o no estoy seguro/a"],
            key="normalidad_final"
        )
        
        if st.button("Ver resultado"):
            if relacion == "Independientes (diferentes personas/sujetos)":
                if normalidad == "Sí":
                    mostrar_resultado("t_student_independientes")
                else:
                    mostrar_resultado("u_mann_whitney")
            else:  # Relacionados
                if normalidad == "Sí":
                    mostrar_resultado("t_student_relacionadas")
                else:
                    mostrar_resultado("wilcoxon")
            
            if st.button("🔄 Reiniciar"):
                st.session_state.paso = 1
                st.session_state.respuestas = {}
                st.rerun()
        
        if st.button("← Atrás"):
            st.session_state.paso = 3
            st.rerun()
    
    # Sidebar con información
    with st.sidebar:
        st.markdown("### 📚 Información")
        st.markdown("""
        Este dashboard te ayuda a seleccionar la prueba estadística correcta según:
        - Tu objetivo de análisis
        - Tipo de datos
        - Número de grupos
        - Supuestos estadísticos
        
        **Tipos de pruebas:**
        - ✅ Paramétricas: requieren normalidad
        - ✅ No paramétricas: más flexibles
        """)
        
        st.markdown("---")
        st.markdown("### 🔍 Todas las pruebas disponibles")
        for key, prueba in pruebas_estadisticas.items():
            with st.expander(f"{prueba['nombre']}"):
                st.markdown(f"**Tipo:** {prueba['tipo']}")
                st.markdown(f"**Uso:** {prueba['uso']}")

if __name__ == "__main__":
    main()
