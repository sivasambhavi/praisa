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
export const searchPatients = async ({ type = 'name', value, hospital }) => {
    try {
        console.log(`Searching for ${value} by ${type} in hospital ${hospital}`);
        
        let patients = [];
        
        // Backend supports name and abha search directly
        if (type === 'name') {
            const response = await client.get('/api/patients/search', {
                params: { name: value }
            });
            patients = response.data.results || [];
        } else if (type === 'abha') {
            const response = await client.get('/api/patients/search', {
                params: { abha: value }
            });
            patients = response.data.results || [];
        } else {
            // For aadhar and phone, we need to fetch all patients and filter client-side
            // This is not optimal for production but works for demo purposes
            const response = await client.get('/api/patients/search', {
                params: { name: '' } // Get all patients with empty name
            });
            patients = response.data.results || [];
            
            // Client-side filtering
            if (type === 'aadhar') {
                const searchValue = value.replace(/\D/g, ''); // Remove non-digits
                patients = patients.filter(p => {
                    const aadhar = (p.aadhar_number || '').replace(/\D/g, '');
                    return aadhar.includes(searchValue);
                });
            } else if (type === 'phone') {
                const searchValue = value.replace(/\D/g, ''); // Remove non-digits
                patients = patients.filter(p => {
                    const mobile = (p.mobile || '').replace(/\D/g, '');
                    return mobile.includes(searchValue);
                });
            }
        }

        // Filter by hospital if specified
        const filtered = hospital
            ? patients.filter(p => p.hospital_id === `hospital_${hospital.toLowerCase()}`)
            : patients;

        return filtered.map(transformPatient);
    } catch (error) {
        console.error("Search failed:", error);
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
