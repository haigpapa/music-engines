import React, { useState, useRef } from 'react';

const UploadZone = ({ onFileSelected, isProcessing }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const fileInputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        if (!isProcessing) setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);

        if (isProcessing) return;

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            validateAndProcess(file);
        }
    };

    const handleFileInput = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            validateAndProcess(file);
        }
    };

    const validateAndProcess = (file) => {
        if (file.type.startsWith('audio/')) {
            setSelectedFile(file);
            onFileSelected(file);
        } else {
            alert('Please upload an audio file.');
        }
    };

    return (
        <div
            className={`relative h-64 rounded-xl flex flex-col items-center justify-center transition-all duration-300 cursor-pointer overflow-hidden group
        ${isDragging ? 'shadow-neu-flat border-2 border-neu-accent' : 'shadow-neu-pressed border border-transparent hover:border-gray-700'}
        ${isProcessing ? 'opacity-90 pointer-events-none' : ''}
      `}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => !isProcessing && fileInputRef.current?.click()}
        >
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileInput}
                accept="audio/*"
                className="hidden"
            />

            {/* Spectral Ripple Simulation (CSS Animation) */}
            <div className={`absolute inset-0 bg-neu-accent/5 rounded-lg transition-transform duration-700 ease-out pointer-events-none
        ${isDragging ? 'scale-110 opacity-100' : 'scale-0 opacity-0'}
      `}></div>

            {isProcessing ? (
                <div className="flex flex-col items-center z-10 space-y-3 w-full px-8">
                    <div className="flex items-center justify-between w-full mb-2">
                        <span className="text-xs text-neu-accent font-mono uppercase tracking-widest">Processing Input Vector</span>
                        <div className="w-4 h-4 border-t-2 border-neu-accent rounded-full animate-spin"></div>
                    </div>

                    {selectedFile && (
                        <div className="w-full bg-neu-bg p-3 rounded shadow-neu-flat flex items-center space-x-3">
                            <div className="text-neu-accent">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
                                </svg>
                            </div>
                            <div className="overflow-hidden">
                                <p className="text-sm font-bold text-neu-text truncate">{selectedFile.name}</p>
                                <p className="text-xs text-gray-500 font-mono">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                        </div>
                    )}

                    <div className="w-full h-2 rounded-full shadow-neu-pressed overflow-hidden mt-4">
                        <div className="h-full bg-neu-accent animate-pulse w-2/3"></div>
                    </div>
                </div>
            ) : (
                <div className="z-10 text-center pointer-events-none">
                    <div className={`w-12 h-12 mx-auto mb-4 text-neu-accent transition-transform duration-300 ${isDragging ? 'scale-110' : ''}`}>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75l3 3m0 0l3-3m-3 3v-7.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <p className="text-neu-text font-bold tracking-widest text-lg">DROP AUDIO SOURCE</p>
                    <p className="text-gray-500 text-xs mt-2 uppercase font-mono">WAV, MP3, AIFF</p>
                </div>
            )}
        </div>
    );
};

export default UploadZone;
