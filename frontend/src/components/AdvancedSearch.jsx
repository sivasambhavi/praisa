import React, { useState } from 'react';

const AdvancedSearch = ({ onSearch, isLoading }) => {
    const [searchType, setSearchType] = useState('name');
    const [searchValue, setSearchValue] = useState('');
    const [hospital, setHospital] = useState('A');
    const [error, setError] = useState('');

    const searchTypes = [
        { id: 'name', label: 'Patient Name', icon: '👤', placeholder: 'e.g. Ramesh Singh' },
        { id: 'abha', label: 'ABHA Number', icon: '🆔', placeholder: 'e.g. 12-3456-7890-1234' },
        { id: 'aadhar', label: 'Aadhar Number', icon: '🔢', placeholder: 'e.g. 1234-5678-9012' },
        { id: 'phone', label: 'Phone Number', icon: '📱', placeholder: 'e.g. 9876543210' }
    ];

    const validateInput = (type, value) => {
        setError('');
        
        if (!value.trim()) {
            setError('Please enter a search value');
            return false;
        }

        switch (type) {
            case 'abha':
                if (value.length < 14) {
                    setError('ABHA number must be at least 14 characters');
                    return false;
                }
                break;
            case 'aadhar':
                const aadharDigits = value.replace(/\D/g, '');
                if (aadharDigits.length !== 12) {
                    setError('Aadhar number must be 12 digits');
                    return false;
                }
                break;
            case 'phone':
                const phoneDigits = value.replace(/\D/g, '');
                if (phoneDigits.length !== 10) {
                    setError('Phone number must be 10 digits');
                    return false;
                }
                break;
            case 'name':
                if (value.length < 2) {
                    setError('Name must be at least 2 characters');
                    return false;
                }
                break;
        }
        
        return true;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (!validateInput(searchType, searchValue)) {
            return;
        }

        onSearch({ 
            type: searchType, 
            value: searchValue.trim(),
            hospital 
        });
    };

    const handleSearchTypeChange = (type) => {
        setSearchType(type);
        setSearchValue('');
        setError('');
    };

    const currentSearchType = searchTypes.find(t => t.id === searchType);

    return (
        <div className="w-full max-w-4xl mx-auto px-4">
            {/* Glassmorphic Card */}
            <div className="bg-white/10 backdrop-blur-2xl rounded-3xl p-8 shadow-2xl border border-white/20">
                
                {/* Header */}
                <div className="mb-6">
                    <h2 className="text-xl font-bold text-white">
                        Advanced Patient Search
                    </h2>
                </div>

                {/* Search Type Tabs */}
                <div className="flex gap-2 mb-6 flex-wrap">
                    {searchTypes.map((type) => (
                        <button
                            key={type.id}
                            type="button"
                            onClick={() => handleSearchTypeChange(type.id)}
                            className={`flex-1 min-w-[140px] px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200 flex items-center justify-center ${
                                searchType === type.id
                                    ? 'bg-gradient-to-r from-cyan-400 to-cyan-500 text-white shadow-lg'
                                    : 'bg-purple-500/50 text-white/90 hover:bg-purple-500/70'
                            }`}
                        >
                            <span>{type.label}</span>
                        </button>
                    ))}
                </div>

                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Input Row */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Search Input - 2 columns */}
                        <div className="md:col-span-2">
                            <label className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wide">
                                {currentSearchType.label}
                            </label>
                            <div className="relative">
                                <input
                                    type="text"
                                    className="w-full bg-white/95 border-0 text-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-all placeholder-gray-400 font-normal shadow-md"
                                    placeholder={currentSearchType.placeholder}
                                    value={searchValue}
                                    onChange={(e) => {
                                        setSearchValue(e.target.value);
                                        setError('');
                                    }}
                                    disabled={isLoading}
                                />
                            </div>
                            {error && (
                                <p className="mt-2 text-sm text-red-200 flex items-center gap-1">
                                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                    </svg>
                                    {error}
                                </p>
                            )}
                        </div>

                        {/* Hospital Selector - 1 column */}
                        <div>
                            <label className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wide">
                                Hospital Source
                            </label>
                            <div className="relative">
                                <select
                                    className="w-full bg-white/95 border-0 text-gray-700 rounded-lg px-4 py-3 pr-10 focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-all appearance-none cursor-pointer shadow-md font-normal"
                                    value={hospital}
                                    onChange={(e) => setHospital(e.target.value)}
                                    disabled={isLoading}
                                >
                                    <option value="A">Hospital A (Apollo)</option>
                                    <option value="B">Hospital B (Max)</option>
                                </select>
                                <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-gray-500">
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full bg-gradient-to-r from-lime-400 via-lime-500 to-green-500 text-white px-6 py-3.5 rounded-lg shadow-xl hover:shadow-2xl hover:-translate-y-0.5 transition-all duration-200 text-base font-bold flex items-center justify-center gap-2 ${
                            isLoading ? 'opacity-75 cursor-not-allowed' : ''
                        }`}
                        style={{
                            boxShadow: '0 0 30px rgba(132, 204, 22, 0.5), 0 10px 25px rgba(0, 0, 0, 0.3)'
                        }}
                    >
                        {isLoading ? (
                            <>
                                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                                </svg>
                                Searching...
                            </>
                        ) : (
                            <>
                                Search Patient Records
                            </>
                        )}
                    </button>
                </form>

                {/* Search Tips */}
                <div className="mt-5 p-3 bg-white/10 rounded-lg border border-white/20">
                    <p className="text-xs text-white/70">
                        <strong className="text-white">Search Tips:</strong> Use patient name for fuzzy matching, or use ABHA/Aadhar/Phone for exact matches. Select the hospital source to narrow your search results.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AdvancedSearch;
