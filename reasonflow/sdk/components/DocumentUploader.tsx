import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { ReasonFlowSDK } from '../js_sdk';

interface DocumentUploaderProps {
    sdk: ReasonFlowSDK;
    onDocumentUploaded: (documentId: string) => void;
}

export const DocumentUploader: React.FC<DocumentUploaderProps> = ({ sdk, onDocumentUploaded }) => {
    const [uploading, setUploading] = useState(false);
    const [metadata, setMetadata] = useState({
        title: '',
        description: '',
        tags: []
    });
    
    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        try {
            setUploading(true);
            for (const file of acceptedFiles) {
                const documentId = await sdk.uploadDocument(file, {
                    ...metadata,
                    filename: file.name
                });
                onDocumentUploaded(documentId);
            }
        } catch (error) {
            console.error('Error uploading document:', error);
        } finally {
            setUploading(false);
        }
    }, [metadata, sdk, onDocumentUploaded]);
    
    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
    
    return (
        <div className="p-4 bg-white rounded-lg shadow">
            <h2 className="text-xl font-bold mb-4">Upload Documents</h2>
            
            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">
                        Title
                    </label>
                    <input
                        type="text"
                        value={metadata.title}
                        onChange={(e) => setMetadata({...metadata, title: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    />
                </div>
                
                <div>
                    <label className="block text-sm font-medium text-gray-700">
                        Description
                    </label>
                    <textarea
                        value={metadata.description}
                        onChange={(e) => setMetadata({...metadata, description: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    />
                </div>
                
                <div
                    {...getRootProps()}
                    className={`mt-4 p-6 border-2 border-dashed rounded-lg text-center cursor-pointer
                        ${isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300'}`}
                >
                    <input {...getInputProps()} />
                    {uploading ? (
                        <p>Uploading...</p>
                    ) : isDragActive ? (
                        <p>Drop the files here...</p>
                    ) : (
                        <p>Drag and drop files here, or click to select files</p>
                    )}
                </div>
            </div>
        </div>
    );
}; 