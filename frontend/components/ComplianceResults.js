// export default function ComplianceResults({ results }) {
//   if (!results || !results.results) {
//     return null;
//   }

//   const { results: complianceResults, pdf_filename, rules_filename } = results;

//   return (
//     <div className="bg-white rounded-lg shadow-md p-6">
//       <div className="mb-6">
//         <h2 className="text-2xl font-bold text-gray-900 mb-2">
//           Compliance Check Results
//         </h2>
//         <div className="text-sm text-gray-600">
//           <p><strong>PDF:</strong> {pdf_filename}</p>
//           <p><strong>Rules:</strong> {rules_filename}</p>
//         </div>
//       </div>

//       <div className="space-y-4">
//         {Object.entries(complianceResults).map(([rule, answer], index) => (
//           <div
//             key={index}
//             className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
//           >
//             <div className="mb-3">
//               <h3 className="font-semibold text-gray-900 mb-2">
//                 Rule {index + 1}:
//               </h3>
//               <p className="text-gray-700 bg-gray-50 p-3 rounded border-l-4 border-blue-500">
//                 {rule}
//               </p>
//             </div>
//             <div>
//               <h4 className="font-medium text-gray-900 mb-2">Assessment:</h4>
//               <div className="prose max-w-none">
//                 <p className="text-gray-700 leading-relaxed">{answer}</p>
//               </div>
//             </div>
//           </div>
//         ))}
//       </div>

//       <div className="mt-6 pt-4 border-t border-gray-200">
//         <p className="text-sm text-gray-500 text-center">
//           Compliance check completed for {Object.keys(complianceResults).length} rules
//         </p>
//       </div>
//     </div>
//   );
// }

export default function ComplianceResults({ results }) {
  if (!results || !results.results) {
    return null;
  }

  const { results: complianceResults, pdf_filename, rules_filename } = results;

  // Function to render formatted text with bullet points
  const renderFormattedText = (text) => {
    // Split by newlines to handle bullet points
    const lines = text.split('\n').filter(line => line.trim());
    
    return lines.map((line, index) => {
      const trimmedLine = line.trim();
      
      // Check if line starts with bullet point
      if (trimmedLine.match(/^[•·▪▫‣⁃\-*]\s/)) {
        return (
          <div key={index} className="flex items-start mb-2">
            <span className="text-blue-600 mr-2 mt-1 flex-shrink-0">•</span>
            <span className="text-gray-700 leading-relaxed">
              {trimmedLine.replace(/^[•·▪▫‣⁃\-*]\s/, '')}
            </span>
          </div>
        );
      }
      
      // Check if line starts with number
      if (trimmedLine.match(/^\d+\.\s/)) {
        const match = trimmedLine.match(/^(\d+)\.\s(.+)/);
        return (
          <div key={index} className="flex items-start mb-2">
            <span className="text-blue-600 mr-2 mt-1 flex-shrink-0 font-medium">
              {match[1]}.
            </span>
            <span className="text-gray-700 leading-relaxed">{match[2]}</span>
          </div>
        );
      }
      
      // Regular line
      return (
        <p key={index} className="text-gray-700 leading-relaxed mb-2">
          {trimmedLine}
        </p>
      );
    });
  };

  // Function to determine compliance status from text
  const getComplianceStatus = (text) => {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('yes') || lowerText.includes('compliant') || lowerText.includes('met') || lowerText.includes('satisfied')) {
      return 'compliant';
    } else if (lowerText.includes('no') || lowerText.includes('not compliant') || lowerText.includes('not met') || lowerText.includes('violation')) {
      return 'non-compliant';
    } else if (lowerText.includes('partial') || lowerText.includes('some') || lowerText.includes('limited')) {
      return 'partial';
    }
    
    return 'unclear';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'compliant':
        return 'border-green-500 bg-green-50';
      case 'non-compliant':
        return 'border-red-500 bg-red-50';
      case 'partial':
        return 'border-yellow-500 bg-yellow-50';
      default:
        return 'border-blue-500 bg-blue-50';
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      compliant: <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">✓ Compliant</span>,
      'non-compliant': <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">✗ Non-Compliant</span>,
      partial: <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">⚠ Partial</span>,
      unclear: <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">? Unclear</span>
    };
    return badges[status] || badges.unclear;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Compliance Check Results
        </h2>
        <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded-md">
          <p><strong>PDF Document:</strong> {pdf_filename}</p>
          <p><strong>Rules File:</strong> {rules_filename}</p>
          <p><strong>Total Rules Checked:</strong> {Object.keys(complianceResults).length}</p>
        </div>
      </div>

      <div className="space-y-6">
        {Object.entries(complianceResults).map(([rule, answer], index) => {
          const status = getComplianceStatus(answer);
          const statusColor = getStatusColor(status);
          
          return (
            <div
              key={index}
              className={`border-l-4 rounded-lg p-4 hover:shadow-sm transition-shadow ${statusColor}`}
            >
              <div className="mb-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 text-lg">
                    Rule {index + 1}
                  </h3>
                  {getStatusBadge(status)}
                </div>
                <div className="bg-white p-3 rounded border border-gray-200">
                  <p className="text-gray-800 font-medium">{rule}</p>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-3 flex items-center">
                  <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Assessment:
                </h4>
                <div className="bg-white p-4 rounded-md border border-gray-200">
                  {renderFormattedText(answer)}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div className="bg-green-50 p-3 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {Object.values(complianceResults).filter(answer => 
                getComplianceStatus(answer) === 'compliant'
              ).length}
            </div>
            <div className="text-sm text-green-800">Compliant</div>
          </div>
          <div className="bg-red-50 p-3 rounded-lg">
            <div className="text-2xl font-bold text-red-600">
              {Object.values(complianceResults).filter(answer => 
                getComplianceStatus(answer) === 'non-compliant'
              ).length}
            </div>
            <div className="text-sm text-red-800">Non-Compliant</div>
          </div>
          <div className="bg-yellow-50 p-3 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">
              {Object.values(complianceResults).filter(answer => 
                getComplianceStatus(answer) === 'partial'
              ).length}
            </div>
            <div className="text-sm text-yellow-800">Partial</div>
          </div>
          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="text-2xl font-bold text-gray-600">
              {Object.values(complianceResults).filter(answer => 
                getComplianceStatus(answer) === 'unclear'
              ).length}
            </div>
            <div className="text-sm text-gray-800">Unclear</div>
          </div>
        </div>
      </div>
    </div>
  );
}