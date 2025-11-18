const API_BASE_URL = '/api/solicitudes';

const areas = [
    'SCC',
    'Psychology',
    'CC&C',
    "WAE's",
    'DCO',
    'Packets',
    "CA's",
    'Follow up',
    'Customer Service'
];

const urgencias = ['Baja', 'Media', 'Alta', 'Crítica'];
const impactos = ['Bajo', 'Medio', 'Alto'];
const estados = ['Recibido', 'En Análisis', 'En Desarrollo', 'Completado'];

let currentSolicitudes = [];

document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeForm();
    loadSolicitudes();
    loadEstadisticas();
});

function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const tabId = btn.dataset.tab;
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabId).classList.add('active');

            if (tabId === 'listado') {
                loadSolicitudes();
            }
        });
    });
}

function initializeForm() {
    const form = document.getElementById('solicitudForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitSolicitud();
    });
}

async function submitSolicitud() {
    const form = document.getElementById('solicitudForm');
    const submitBtn = form.querySelector('button[type="submit"]');

    const formData = {
        area_solicitante: document.getElementById('area').value,
        nombre_solicitante: document.getElementById('nombre').value,
        email_solicitante: document.getElementById('email').value,
        titulo_proceso: document.getElementById('titulo').value,
        descripcion_proceso: document.getElementById('descripcion').value,
        situacion_actual: document.getElementById('situacionActual').value,
        resultado_esperado: document.getElementById('resultadoEsperado').value,
        urgencia: document.getElementById('urgencia').value,
        impacto: document.getElementById('impacto').value,
        frecuencia_proceso: document.getElementById('frecuencia').value || null,
        tiempo_manual_estimado: document.getElementById('tiempoManual').value || null,
        sistemas_involucrados: document.getElementById('sistemas').value || null,
        enlaces_documentacion: document.getElementById('enlaces').value || null
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';

    try {
        const response = await fetch(API_BASE_URL + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al enviar la solicitud');
        }

        const result = await response.json();
        showToast(`Solicitud ${result.numero_solicitud} creada exitosamente`, 'success');
        form.reset();
        loadEstadisticas();

        document.querySelector('[data-tab="listado"]').click();

    } catch (error) {
        console.error('Error:', error);
        showToast(error.message || 'Error al enviar la solicitud', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar Solicitud';
    }
}

async function loadSolicitudes() {
    const tableBody = document.getElementById('solicitudesTableBody');
    const areaFilter = document.getElementById('filterArea').value;
    const estadoFilter = document.getElementById('filterEstado').value;

    tableBody.innerHTML = '<tr><td colspan="6" class="loading"><div class="spinner"></div></td></tr>';

    try {
        let url = API_BASE_URL + '/';
        const params = new URLSearchParams();

        if (areaFilter) params.append('area', areaFilter);
        if (estadoFilter) params.append('estado', estadoFilter);

        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error('Error al cargar solicitudes');

        currentSolicitudes = await response.json();
        renderSolicitudesTable(currentSolicitudes);

    } catch (error) {
        console.error('Error:', error);
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-state">
                    Error al cargar las solicitudes. Por favor, intente de nuevo.
                </td>
            </tr>
        `;
    }
}

function renderSolicitudesTable(solicitudes) {
    const tableBody = document.getElementById('solicitudesTableBody');

    if (solicitudes.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-state">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p>No hay solicitudes registradas</p>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = solicitudes.map(sol => `
        <tr onclick="viewSolicitudDetails(${sol.id})" style="cursor: pointer;">
            <td><strong>${sol.numero_solicitud}</strong></td>
            <td>${sol.area_solicitante}</td>
            <td>${sol.titulo_proceso}</td>
            <td><span class="urgencia-badge urgencia-${getUrgenciaClass(sol.urgencia)}">${sol.urgencia}</span></td>
            <td><span class="status-badge status-${getStatusClass(sol.estado)}">${sol.estado}</span></td>
            <td>${formatDate(sol.fecha_creacion)}</td>
        </tr>
    `).join('');
}

function getStatusClass(estado) {
    const map = {
        'Recibido': 'recibido',
        'En Análisis': 'analisis',
        'En Desarrollo': 'desarrollo',
        'Completado': 'completado'
    };
    return map[estado] || 'recibido';
}

function getUrgenciaClass(urgencia) {
    const map = {
        'Baja': 'baja',
        'Media': 'media',
        'Alta': 'alta',
        'Crítica': 'critica'
    };
    return map[urgencia] || 'media';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-MX', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

async function loadEstadisticas() {
    try {
        const response = await fetch(API_BASE_URL + '/estadisticas/resumen');
        if (!response.ok) throw new Error('Error al cargar estadísticas');

        const stats = await response.json();

        document.getElementById('statTotal').textContent = stats.total;
        document.getElementById('statRecibidas').textContent = stats.recibidas;
        document.getElementById('statAnalisis').textContent = stats.en_analisis;
        document.getElementById('statDesarrollo').textContent = stats.en_desarrollo;
        document.getElementById('statCompletadas').textContent = stats.completadas;

    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function viewSolicitudDetails(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/${id}`);
        if (!response.ok) throw new Error('Error al cargar detalles');

        const solicitud = await response.json();

        const modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = `
            <div class="detail-row">
                <div class="detail-label">Número de Solicitud</div>
                <div class="detail-value"><strong>${solicitud.numero_solicitud}</strong></div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Estado</div>
                <div class="detail-value">
                    <span class="status-badge status-${getStatusClass(solicitud.estado)}">${solicitud.estado}</span>
                </div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Área Solicitante</div>
                <div class="detail-value">${solicitud.area_solicitante}</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Solicitante</div>
                <div class="detail-value">${solicitud.nombre_solicitante} (${solicitud.email_solicitante})</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Título del Proceso</div>
                <div class="detail-value">${solicitud.titulo_proceso}</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Descripción</div>
                <div class="detail-value">${solicitud.descripcion_proceso}</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Situación Actual</div>
                <div class="detail-value">${solicitud.situacion_actual}</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Resultado Esperado</div>
                <div class="detail-value">${solicitud.resultado_esperado}</div>
            </div>
            <div class="detail-row">
                <div class="detail-label">Urgencia / Impacto</div>
                <div class="detail-value">
                    <span class="urgencia-badge urgencia-${getUrgenciaClass(solicitud.urgencia)}">${solicitud.urgencia}</span>
                    / ${solicitud.impacto}
                </div>
            </div>
            ${solicitud.frecuencia_proceso ? `
            <div class="detail-row">
                <div class="detail-label">Frecuencia del Proceso</div>
                <div class="detail-value">${solicitud.frecuencia_proceso}</div>
            </div>
            ` : ''}
            ${solicitud.tiempo_manual_estimado ? `
            <div class="detail-row">
                <div class="detail-label">Tiempo Manual Estimado</div>
                <div class="detail-value">${solicitud.tiempo_manual_estimado}</div>
            </div>
            ` : ''}
            ${solicitud.sistemas_involucrados ? `
            <div class="detail-row">
                <div class="detail-label">Sistemas Involucrados</div>
                <div class="detail-value">${solicitud.sistemas_involucrados}</div>
            </div>
            ` : ''}
            ${solicitud.enlaces_documentacion ? `
            <div class="detail-row">
                <div class="detail-label">Enlaces/Documentación</div>
                <div class="detail-value">${solicitud.enlaces_documentacion}</div>
            </div>
            ` : ''}
            <div class="detail-row">
                <div class="detail-label">Fecha de Creación</div>
                <div class="detail-value">${formatDate(solicitud.fecha_creacion)}</div>
            </div>
        `;

        document.getElementById('detailModal').classList.add('active');

    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar los detalles', 'error');
    }
}

function closeModal() {
    document.getElementById('detailModal').classList.remove('active');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

document.getElementById('detailModal').addEventListener('click', (e) => {
    if (e.target.id === 'detailModal') {
        closeModal();
    }
});
