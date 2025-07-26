document.addEventListener('DOMContentLoaded', () => {
    // Obtener datos de la tarjeta
    const matchData = JSON.parse("{{MatchData}}");
    
    // Generar preguntas y comboboxes
    const container = document.getElementById('preguntas-container');
    matchData.preguntas.forEach((pregunta, index) => {
        const div = document.createElement('div');
        div.className = 'pregunta-item';
        div.innerHTML = `
            <label>${pregunta.texto}</label>
            <select id="select-${index}">
                <option value="">Seleccione...</option>
                ${pregunta.opciones.map((op, i) => 
                    `<option value="${i}">${op}</option>`).join('')}
            </select>
        `;
        container.appendChild(div);
    });
    
    // Verificar respuestas
    document.getElementById('verificar-btn').addEventListener('click', () => {
        const resultados = [];
        matchData.preguntas.forEach((_, index) => {
            const select = document.getElementById(`select-${index}`);
            resultados.push(select.value);
        });
        
        // Enviar a Python para verificación
        pycmd(`verificar:${JSON.stringify(resultados)}`);
    });
});