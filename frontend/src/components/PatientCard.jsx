import React from 'react';

const PatientCard = ({ patient, onMatchClick, onHistoryClick }) => {
    if (!patient) return null;

    // Generate initials for avatar
    const getInitials = (name) => {
        if (!name) return '?';
        return name
            .split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);
    };

    // Format date
    const formatDate = (dateStr) => {
        if (!dateStr) return 'N/A';
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    // Get hospital badge color
    const getHospitalColor = (hospitalId) => {
        if (hospitalId?.includes('_a')) return 'from-cyan-500 to-blue-500';
        if (hospitalId?.includes('_b')) return 'from-purple-500 to-pink-500';
        return 'from-gray-500 to-gray-600';
    };

    const getHospitalName = (hospitalId) => {
        if (hospitalId?.includes('_a')) return 'Apollo';
        if (hospitalId?.includes('_b')) return 'Max';
        return 'Unknown';
    };

    return (
        <div className="glass-card p-6 animate-scale-in group">
            {/* Gradient Border Accent */}
            <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-cyan-500 via-blue-500 to-purple-500 rounded-l-xl"></div>

            <div className="flex items-start gap-4">
                {/* Avatar */}
                <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${getHospitalColor(patient.hospital_id)} flex items-center justify-center text-white text-xl font-bold shadow-lg flex-shrink-0`}>
                    {getInitials(patient.name)}
                </div>

                {/* Patient Info */}
                <div className="flex-1 min-w-0">
                    {/* Name and Hospital Badge */}
                    <div className="flex items-start justify-between gap-2 mb-3">
                        <h3 className="text-xl font-bold text-white truncate">
                            {patient.name || 'Unknown Patient'}
                        </h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold text-white bg-gradient-to-r ${getHospitalColor(patient.hospital_id)} whitespace-nowrap`}>
                            🏥 {getHospitalName(patient.hospital_id)}
                        </span>
                    </div>

                    {/* Demographics Grid */}
                    <div className="grid grid-cols-2 gap-3 mb-4">
                        {/* Patient ID */}
                        <div className="flex items-center gap-2 text-sm">
                            <span className="text-white/60">🆔</span>
                            <div>
                                <p className="text-white/80 text-xs">Patient ID</p>
                                <p className="text-white font-semibold">{patient.id || patient.patient_id || 'N/A'}</p>
                            </div>
                        </div>

                        {/* Date of Birth */}
                        <div className="flex items-center gap-2 text-sm">
                            <span className="text-white/60">🎂</span>
                            <div>
                                <p className="text-white/80 text-xs">Date of Birth</p>
                                <p className="text-white font-semibold">{formatDate(patient.dob)}</p>
                            </div>
                        </div>

                        {/* Gender */}
                        <div className="flex items-center gap-2 text-sm">
                            <span className="text-white/60">{patient.gender === 'M' ? '👨' : patient.gender === 'F' ? '👩' : '👤'}</span>
                            <div>
                                <p className="text-white/80 text-xs">Gender</p>
                                <p className="text-white font-semibold">
                                    {patient.gender === 'M' ? 'Male' : patient.gender === 'F' ? 'Female' : 'Other'}
                                </p>
                            </div>
                        </div>

                        {/* Phone */}
                        <div className="flex items-center gap-2 text-sm">
                            <span className="text-white/60">📱</span>
                            <div>
                                <p className="text-white/80 text-xs">Phone</p>
                                <p className="text-white font-semibold">{patient.mobile || 'N/A'}</p>
                            </div>
                        </div>
                    </div>

                    {/* ABHA Number */}
                    {patient.abha_number && (
                        <div className="mb-4 p-3 bg-white/15 rounded-lg border border-white/30">
                            <p className="text-white/80 text-xs mb-1">ABHA Health ID</p>
                            <p className="text-white font-mono font-semibold text-sm">{patient.abha_number}</p>
                        </div>
                    )}

                    {/* Address */}
                    {patient.address && (
                        <div className="mb-4 text-sm">
                            <p className="text-white/80 text-xs mb-1">📍 Address</p>
                            <p className="text-white">{patient.address}</p>
                        </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex gap-3 mt-4">
                        <button
                            onClick={() => onMatchClick(patient)}
                            className="flex-1 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2.5 rounded-lg font-semibold hover:shadow-lg hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            Match Patient
                        </button>
                        <button
                            onClick={() => onHistoryClick(patient)}
                            className="flex-1 bg-white/25 text-white px-4 py-2.5 rounded-lg font-semibold hover:bg-white/35 transition-all flex items-center justify-center gap-2 border border-white/40"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            View History
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PatientCard;