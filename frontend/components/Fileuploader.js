import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileUploader({ onSubmit, loading }) {
  const [pdfFile, setPdfFile] = useState(null);
  const [rulesFile, setRulesFile] = useState(null);

  const onPdfDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setPdfFile(acceptedFiles[0]);
    }
  }, []);

  const onRulesDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setRulesFile(acceptedFiles[0]);
    }
  }, []);

  const {
    getRootProps: getPdfRootProps,
    getInputProps: getPdfInputProps,
    isDragActive: isPdfDragActive,
  } = useDropzone({
    onDrop: onPdfDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: false,
  });

  const {
    getRootProps: getRulesRootProps,
    getInputProps: getRulesInputProps,
    isDragActive: isRulesDragActive,
  } = useDropzone({
    onDrop: onRulesDrop,
    accept: {
      'text/plain': ['.txt'],
    },
    multiple: false,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (pdfFile && rulesFile && !loading) {
      onSubmit(pdfFile, rulesFile);
    }
  };

  const canSubmit = pdfFile && rulesFile && !loading;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* PDF Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            PDF Document
          </label>
          <div
            {...getPdfRootProps()}
            className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
              isPdfDragActive
                ? 'border-blue-400 bg-blue-50'
                : pdfFile
                ? 'border-green-400 bg-green-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getPdfInputProps()} />
            <svg
              className="mx-auto h-12 w-12 text-gray-400 mb-4"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            {pdfFile ? (
              <p className="text-green-600 font-medium">{pdfFile.name}</p>
            ) : (
              <div>
                <p className="text-gray-600">
                  {isPdfDragActive
                    ? 'Drop the PDF file here'
                    : 'Drag & drop PDF file here, or click to select'}
                </p>
                <p className="text-xs text-gray-500 mt-1">PDF files only</p>
              </div>
            )}
          </div>
        </div>

        {/* Rules Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Rules File
          </label>
          <div
            {...getRulesRootProps()}
            className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
              isRulesDragActive
                ? 'border-blue-400 bg-blue-50'
                : rulesFile
                ? 'border-green-400 bg-green-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getRulesInputProps()} />
            <svg
              className="mx-auto h-12 w-12 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            {rulesFile ? (
              <p className="text-green-600 font-medium">{rulesFile.name}</p>
            ) : (
              <div>
                <p className="text-gray-600">
                  {isRulesDragActive
                    ? 'Drop the rules file here'
                    : 'Drag & drop rules file here, or click to select'}
                </p>
                <p className="text-xs text-gray-500 mt-1">TXT files only</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          type="submit"
          disabled={!canSubmit}
          className={`px-6 py-3 rounded-md font-medium transition-colors ${
            canSubmit
              ? 'bg-blue-600 hover:bg-blue-700 text-white'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {loading ? 'Processing...' : 'Check Compliance'}
        </button>
      </div>
    </form>
  );
}