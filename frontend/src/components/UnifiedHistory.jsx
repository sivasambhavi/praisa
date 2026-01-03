import React from 'react';

const UnifiedHistory = ({ history }) => {
    return (
        <div className="bg-white p-6 rounded-lg shadow-md mt-8">
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                    </div>
                    <div className="ml-3">
                        <p className="text-sm text-yellow-700">
                            <strong>Note:</strong> Hospital B doctors can now see diabetes history from Hospital A!
                        </p>
                    </div>
                </div>
            </div>

            <h2 className="text-2xl font-bold mb-6 text-gray-800">Unified Medical History</h2>

            <div className="relative border-l-4 border-gray-200 ml-4 space-y-8">
                {history.map((visit, index) => (
                    <div key={index} className="mb-8 ml-6 relative">
                        <div className={`absolute -left-10 w-8 h-8 rounded-full border-4 flex items-center justify-center bg-white ${visit.hospital === 'A' ? 'border-blue-500' : 'border-green-500'}`}>
                            <div className={`w-3 h-3 rounded-full ${visit.hospital === 'A' ? 'bg-blue-500' : 'bg-green-500'}`}></div>
                        </div>
                        <div className={`p-5 rounded-lg border shadow-sm ${visit.hospital === 'A' ? 'bg-blue-50 border-blue-100' : 'bg-green-50 border-green-100'}`}>
                            <div className="flex justify-between items-start mb-2">
                                <div>
                                    <span className={`inline-block px-2 py-1 text-xs font-semibold rounded-full mb-2 ${visit.hospital === 'A' ? 'bg-blue-200 text-blue-800' : 'bg-green-200 text-green-800'}`}>
                                        Hospital {visit.hospital}
                                    </span>
                                    <h3 className="text-lg font-bold text-gray-900">{visit.diagnosis}</h3>
                                </div>
                                <div className="text-right">
                                    <div className="text-lg font-mono font-semibold text-gray-600">{visit.date}</div>
                                    <div className="text-sm text-gray-500">{visit.type}</div>
                                </div>
                            </div>
                            <p className="text-gray-700 mb-2">{visit.notes}</p>
                            <div className="text-sm text-gray-500 font-medium border-t border-gray-200 pt-2 mt-2">
                                Dr. {visit.doctor} | {visit.department}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default UnifiedHistory;
