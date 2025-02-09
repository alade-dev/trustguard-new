const HowItWorksPage = () => {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold text-center mb-6">How It Works</h1>
      <p className="text-lg text-gray-400 text-center mb-12">
        TrustGuard ensures secure AI-powered audits and reputation security in a
        few simple steps.
      </p>

      <div className="space-y-8">
        {/* Step 1 */}
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-shrink-0 w-16 h-16 flex items-center justify-center bg-blue-600 text-white text-2xl font-bold rounded-full">
            1
          </div>
          <div>
            <h2 className="text-xl font-semibold">Upload Your Data</h2>
            <p className="text-gray-400">
              Securely upload your smart contract or project files for analysis.
              We support multiple formats to ensure compatibility.
            </p>
          </div>
        </div>

        {/* Step 2 */}
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-shrink-0 w-16 h-16 flex items-center justify-center bg-blue-600 text-white text-2xl font-bold rounded-full">
            2
          </div>
          <div>
            <h2 className="text-xl font-semibold">AI-Powered Audit</h2>
            <p className="text-gray-400">
              Our advanced AI scans and analyzes your data for vulnerabilities,
              security risks, and reputation threats.
            </p>
          </div>
        </div>

        {/* Step 3 */}
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-shrink-0 w-16 h-16 flex items-center justify-center bg-blue-600 text-white text-2xl font-bold rounded-full">
            3
          </div>
          <div>
            <h2 className="text-xl font-semibold">Get Your Report</h2>
            <p className="text-gray-400">
              Receive a comprehensive report detailing findings, risk levels,
              and recommendations to improve security.
            </p>
          </div>
        </div>

        {/* Step 4 */}
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-shrink-0 w-16 h-16 flex items-center justify-center bg-blue-600 text-white text-2xl font-bold rounded-full">
            4
          </div>
          <div>
            <h2 className="text-xl font-semibold">Enhance & Secure</h2>
            <p className="text-gray-400">
              Implement our AI-driven recommendations to strengthen your
              project’s security and build trust with users.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HowItWorksPage;
