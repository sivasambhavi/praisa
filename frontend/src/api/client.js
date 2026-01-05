import axios from 'axios';

const client = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Data Transformers
const transformPatient = (data) => {
    if (!data) return null;
    return {
        ...data,
        id: data.patient_id, // Map backend 'patient_id' to frontend 'id'
    };
};

const transformVisit = (data, hospitalLabel) => {
    if (!data) return null;
    // Backend: admission_date (datetime), visit_type, doctor_name
    // Frontend: date, type, doctor, department, hospital, notes
    return {
        ...data,
        date: data.admission_date ? data.admission_date.split('T')[0] : '', // Extract YYYY-MM-DD
        type: data.visit_type || 'OPD',
        doctor: data.doctor_name || 'Unknown',
        department: 'General', // Default
        hospital: hospitalLabel || 'A', // Default is A, but can be overridden
        notes: data.diagnosis || '', // Use diagnosis as notes
        diagnosis: data.diagnosis || 'Unknown' // Ensure diagnosis is top-level
    };
};

// API Methods
<<<<<<< HEAD
export const searchPatients = async (criteria) => {
    try {
        // Handle multiple input formats:
        // 1. { name: "...", hospital: "..." } (from App.jsx cross-hospital matching)
        // 2. { type: "name"|"abha"|"phone"|"aadhar", value: "...", hospital: "..." } (from AdvancedSearch)
=======
export const searchPatients = async ({ type = 'name', value, hospital }) => {
    try {
        console.log(`Searching for ${value} (type: ${type}) in ${hospital}`);
>>>>>>> 38769de8184de3ce0d956291ae1d59443dea845b

        const searchType = criteria.type || 'name';
        const searchValue = criteria.value || criteria.name;
        const hospital = criteria.hospital;

        console.log(`[Frontend] Search type: ${searchType}, value: ${searchValue}, hospital: ${hospital || 'all'}`);

        // Prepare hospital_id for backend
        const hospital_id = hospital ? `hospital_${hospital.toLowerCase()}` : undefined;

<<<<<<< HEAD
        // Build API parameters based on search type
        let params = {};

        if (searchType === 'abha') {
            // ABHA search - searches ALL hospitals automatically
            params = { abha: searchValue };
            console.log('[Frontend] ABHA search (cross-hospital)');
        } else if (searchType === 'phone') {
            // Phone search - searches ALL hospitals automatically
            params = { phone: searchValue };
            console.log('[Frontend] Phone search (cross-hospital)');
        } else if (searchType === 'aadhar') {
            // Aadhar not implemented - treat as name for now
            console.warn('[Frontend] Aadhar search not implemented, using name search');
            params = { name: searchValue, hospital_id };
        } else {
            // Name search (default) - respects hospital filter
            params = { name: searchValue, hospital_id };
            console.log(`[Frontend] Name search in ${hospital_id || 'all hospitals'}`);
        }

        // Call  backend API
        const response = await client.get('/api/patients/search', { params });

        console.log(`[Frontend] Response: ${response.data.count} results`);
=======
        // Map search type to appropriate query parameter
        const params = { hospital_id };
        
        switch (type) {
            case 'name':
                params.name = value;
                break;
            case 'abha':
                params.abha = value;
                break;
            case 'aadhar':
                params.aadhar = value;
                break;
            case 'phone':
                params.phone = value;
                break;
            default:
                params.name = value;
        }

        // Endpoint: GET /api/patients/search with appropriate params
        const response = await client.get('/api/patients/search', { params });
>>>>>>> 38769de8184de3ce0d956291ae1d59443dea845b

        const patients = response.data.results || [];
        return patients.map(transformPatient);
    } catch (error) {
        console.error("[Frontend] Search failed:", error);
        console.error("[Frontend] Error details:", error.response?.data || error.message);
        throw error;
    }
};

export const getPatient = async (id) => {
    try {
        const response = await client.get(`/api/patients/${id}`);
        return transformPatient(response.data);
    } catch (error) {
        console.error(`Get patient ${id} failed:`, error);
        throw error;
    }
};

export const matchPatients = async (sourceId, targetId) => {
    try {
        // Fetch full patient records first
        const [p1, p2] = await Promise.all([
            getPatient(sourceId),
            getPatient(targetId)
        ]);

        console.log("Matching:", p1, p2);

        const response = await client.post('/api/match', {
            patient_a: p1,
            patient_b: p2
        });
        return response.data;
    } catch (error) {
        console.error("Match failed:", error);
        throw error;
    }
};

export const getPatientHistory = async (id, hospitalLabel) => {
    try {
        const response = await client.get(`/api/patients/${id}/history`);
        // Response: { patient: {}, visits: [], visit_count: 0 }
        return (response.data.visits || []).map(v => transformVisit(v, hospitalLabel));
    } catch (error) {
        console.error(`Get history for ${id} failed:`, error);
        throw error;
    }
};

export default client;
