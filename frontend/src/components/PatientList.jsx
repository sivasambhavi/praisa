import React from 'react';
import PatientCard from './PatientCard';

const PatientList = ({ patients, loading, onMatchClick, onHistoryClick }) => {
    // Loading skeleton
    if (loading) {
        return (
            <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="glass-card p-6 animate-pulse">
                        <div className="flex items-start gap-4">
                            <div className="w-16 h-16 rounded-full bg-white/20"></div>
                            <div className="flex-1 space-y-3">
                                <div className="h-6 bg-white/20 rounded w-1/3"></div>
                                <div className="h-4 bg-white/20 rounded w-1/2"></div>
                                <div className="h-4 bg-white/20 rounded w-2/3"></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    // Empty state
    if (!patients || patients.length === 0) {
        return (
            <div className="glass-card p-12 text-center animate-fade-in">
                <div className="max-w-md mx-auto">
                    {/* Empty State Illustration */}
                    <div className="w-32 h-32 mx-auto mb-6 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-full flex items-center justify-center">
                        <svg className="w-16 h-16 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </div>
                    
                    <h3 className="text-2xl font-bold text-white mb-3">
                        No Patients Found
                    </h3>
                    <p className="text-white/70 mb-6">
                        We couldn't find any patients matching your search criteria. 
                        Try adjusting your search parameters or use a different search type.
                    </p>
                    
                    <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                        <p className="text-sm text-white/80 flex items-start">
                            <svg className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                            </svg>
                            <span>
                                <strong>Tip:</strong> Use partial names for broader results, or try searching by ABHA number for exact matches.
                            </span>
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    // Results display
    return (
        <div className="animate-fade-in-up">
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                        {patients.length}
                    </div>
                    <div>
                        <h3 className="text-xl font-bold text-white">
                            {patients.length === 1 ? 'Patient Found' : 'Patients Found'}
                        </h3>
                        <p className="text-white/70 text-sm">
                            Click on a patient card to view details and match
                        </p>
                    </div>
                </div>
            </div>

            {/* Patient Cards Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {patients.map((patient, index) => (
                    <div 
                        key={patient.id || patient.patient_id || index}
                        style={{ animationDelay: `${index * 100}ms` }}
                    >
                        <PatientCard
                            patient={patient}
                            onMatchClick={onMatchClick}
                            onHistoryClick={onHistoryClick}
                        />
                    </div>
                ))}
            </div>

            {/* Results Footer */}
            {patients.length > 5 && (
                <div className="mt-6 text-center">
                    <p className="text-white/60 text-sm">
                        Showing all {patients.length} results
                    </p>
                </div>
            )}
        </div>
    );
};

export default PatientList;
