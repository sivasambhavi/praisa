import React, { useState } from 'react';

const SearchForm = ({ onSearch, isLoading }) => {
    const [name, setName] = useState('');
    const [hospital, setHospital] = useState('A');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch({ name, hospital });
    };

    return (

        <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl border border-white/20 mb-10 transition-all hover:shadow-2xl">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 tracking-tight">Search Patient Records</h2>
            <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-6 items-end">
                <div className="flex-1 w-full">
                    <label className="block text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wider">Patient Name</label>
                    <input
                        type="text"
                        className="w-full bg-gray-50 border border-gray-200 text-gray-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 transition-all text-lg placeholder-gray-400"
                        placeholder="e.g. Ramesh Singh"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        disabled={isLoading}
                    />
                </div>
                <div className="w-full md:w-64">
                    <label className="block text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wider">Hospital Source</label>
                    <div className="relative">
                        <select
                            className="w-full bg-gray-50 border border-gray-200 text-gray-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 transition-all appearance-none cursor-pointer"
                            value={hospital}
                            onChange={(e) => setHospital(e.target.value)}
                            disabled={isLoading}
                        >
                            <option value="A">Hospital A (Apollo)</option>
                            <option value="B">Hospital B (Max)</option>
                            <option value="C">Hospital C (Fortis)</option>
                            <option value="D">Hospital D (Manipal)</option>
                            <option value="E">Hospital E (Cloudnine)</option>
                        </select>
                        <div className="absolute inset-y-0 right-0 flex items-center px-4 pointer-events-none text-gray-500">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                        </div>
                    </div>
                </div>
                <button
                    type="submit"
                    disabled={isLoading}
                    className={`w-full md:w-auto bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-3 rounded-xl shadow-lg hover:shadow-blue-500/30 hover:-translate-y-0.5 transition-all text-lg font-bold flex items-center justify-center gap-2 ${isLoading ? 'opacity-75 cursor-not-allowed' : ''}`}
                >
                    {isLoading ? (
                        <>
                            <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                            Searching...
                        </>
                    ) : (
                        'Run Search'
                    )}
                </button>
            </form>
        </div>
    );
};

export default SearchForm;
