import { web3Auth } from "@/hooks/Wallet";
import { useNavigate } from "react-router-dom";

const AboutPage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    if (web3Auth.connected) {
      navigate("/upload");
    } else {
      alert("Please connect your wallet to get started.");
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      <h1 className="text-4xl font-bold text-center mb-6">About Us</h1>
      <p className="text-lg text-gray-400 text-center mb-12">
        We are pioneers in AI-driven security, ensuring trust and transparency
        in the digital world.
      </p>

      {/* Our Mission */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
        <p className="text-gray-400 leading-relaxed">
          At TrustGuard, our mission is to empower individuals, businesses, and
          organizations with cutting-edge AI-driven security audits. We believe
          that trust is the foundation of any successful digital interaction,
          and we are committed to ensuring that every smart contract, project,
          and system meets the highest security standards.
        </p>
        <p className="text-gray-400 leading-relaxed mt-4">
          Through our intelligent audit platform, we help clients identify
          vulnerabilities, assess risks, and implement solutions that foster
          transparency and security. Our goal is to create a safer and more
          reliable ecosystem for developers, investors, and users alike.
        </p>
      </section>

      {/* Our Vision */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Our Vision</h2>
        <p className="text-gray-400 leading-relaxed">
          We envision a digital future where security is not an afterthought but
          a fundamental pillar of every project. As blockchain technology, AI,
          and smart contracts continue to shape the world, our vision is to be
          the leading force in ensuring that these advancements are secure,
          transparent, and trustworthy.
        </p>
        <p className="text-gray-400 leading-relaxed mt-4">
          By leveraging artificial intelligence and data-driven insights, we
          strive to eliminate vulnerabilities before they become threats. We aim
          to be the go-to solution for businesses and developers who want to
          build with confidence.
        </p>
      </section>

      {/* Our Values */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Our Core Values</h2>
        <ul className="list-disc pl-6 text-gray-400 space-y-3">
          <li>
            <strong>Integrity:</strong> We prioritize honesty, transparency, and
            ethical practices in everything we do.
          </li>
          <li>
            <strong>Innovation:</strong> Our AI-driven approach ensures that we
            stay ahead of the curve in security technology.
          </li>
          <li>
            <strong>Trust:</strong> We are committed to fostering a secure
            digital environment where users can operate with confidence.
          </li>
          <li>
            <strong>Excellence:</strong> We strive for the highest standards in
            our audits, reports, and security solutions.
          </li>
          <li>
            <strong>Collaboration:</strong> We believe in the power of
            partnerships and community-driven solutions to build a safer
            ecosystem.
          </li>
        </ul>
      </section>

      {/* Our Team */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Meet Our Team</h2>
        <p className="text-gray-400 leading-relaxed">
          TrustGuard is powered by a dedicated team of security experts, AI
          engineers, and blockchain specialists who share a passion for
          protecting the digital landscape. Our team brings together years of
          experience in cybersecurity, AI development, and blockchain technology
          to deliver top-notch security solutions.
        </p>
        <p className="text-gray-400 leading-relaxed mt-4">
          We believe that collaboration and continuous learning are the keys to
          staying ahead of evolving security challenges. Our experts work
          tirelessly to ensure that our clients receive the most accurate and
          comprehensive security assessments available.
        </p>
      </section>

      {/* Call to Action */}
      <div className="mt-12 text-center">
        <h3 className="text-xl font-semibold mb-2">
          Join Us in Securing the Future
        </h3>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Whether you’re a developer, a business, or an organization looking to
          enhance your security, TrustGuard is here to help. Let’s work together
          to create a more transparent and secure digital world.
        </p>
        <button
          onClick={handleGetStarted}
          className="px-6 py-3  bg-blue-600 rounded-3xl hover:bg-blue-600 shadow-2xl text-lg mt-6"
        >
          Get Started
        </button>
      </div>
    </div>
  );
};

export default AboutPage;
