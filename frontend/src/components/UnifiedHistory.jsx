import React from 'react';

const UnifiedHistory = ({ history }) => {
    return (

        <div className="bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-2xl border border-white/50 mt-10 animate-fade-in-up">

            <div className="flex items-center justify-between mb-8">
                <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">Unified Medical History</h2>
                <div className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-xs font-bold px-4 py-2 rounded-full uppercase tracking-wider shadow-lg">
                    Live Data Integration
                </div>
            </div>

            <div className="bg-amber-50/80 backdrop-blur-sm border-l-4 border-amber-400 p-6 rounded-r-xl mb-12 shadow-sm">
                <div className="flex items-start">
                    <div className="flex-shrink-0 mt-0.5">
                        <svg className="h-6 w-6 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div className="ml-4">
                        <h3 className="text-lg font-bold text-amber-800">Interoperability Active</h3>
                        <p className="text-amber-700 mt-1">
                            Dr. Sharma (Hospital B) can now access <strong>Diabetes History</strong> from Apollo Hospital (Hospital A). This prevents medication errors.
                        </p>
                    </div>
                </div>
            </div>

            <div className="relative pl-8 border-l-2 border-dashed border-gray-300 space-y-12">
                {history.map((visit, index) => (
                    <div key={index} className="relative group">
                        {/* Timeline Dot */}
                        <div className={`absolute -left-[41px] top-6 w-5 h-5 rounded-full border-4 border-white shadow-md z-10 ${visit.hospital === 'A' ? 'bg-blue-500 ring-4 ring-blue-100' : 'bg-green-500 ring-4 ring-green-100'}`}></div>

                        <div className={`bg-white p-6 rounded-2xl shadow-sm border transition-all hover:shadow-lg hover:-translate-y-1 ${visit.hospital === 'A' ? 'border-blue-100 hover:border-blue-200' : 'border-green-100 hover:border-green-200'}`}>
                            <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-4 mb-4">
                                <div>
                                    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide mb-3 ${visit.hospital === 'A' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'}`}>
                                        <div className={`w-2 h-2 rounded-full ${visit.hospital === 'A' ? 'bg-blue-500' : 'bg-green-500'}`}></div>
                                        Hospital {visit.hospital}
                                    </div>
                                    <h3 className="text-xl font-bold text-gray-900">{visit.diagnosis}</h3>
                                </div>
                                <div className="text-right">
                                    <div className="text-2xl font-mono font-bold text-gray-700">{visit.date}</div>
                                    <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">{visit.type}</div>
                                </div>
                            </div>

                            <p className="text-gray-600 mb-6 leading-relaxed bg-gray-50 p-4 rounded-lg italic">"{visit.notes}"</p>

                            <div className="flex items-center gap-4 text-sm font-medium text-gray-500 pt-4 border-t border-gray-100">
                                <div className="flex items-center gap-2">
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                                    {visit.doctor}
                                </div>
                                <div className="w-1 h-1 bg-gray-300 rounded-full"></div>
                                <div className="flex items-center gap-2">
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                                    {visit.department}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* End of Timeline */}
            <div className="relative pl-8 pt-4">
                <div className="absolute -left-[35px] top-0 w-2 h-2 bg-gray-300 rounded-full"></div>
                <div className="text-sm text-gray-400 font-medium italic">End of records</div>
            </div>
        </div>
    );
};

export default UnifiedHistory;
