import { useState } from "react";
import { ChevronDown } from "lucide-react";
import Aibg from "../assets/ai-bg.webp";

const faqs = [
  {
    question: "How does the AI-powered audit work?",
    answer:
      "Our AI analyzes your smart contracts and transactions, detecting vulnerabilities and security risks in real-time.",
  },
  {
    question: "What makes this different from traditional audits?",
    answer:
      "Unlike traditional audits, our AI-driven system continuously monitors and updates risk assessments, ensuring proactive security.",
  },
  {
    question: "Can I integrate this with my existing security framework?",
    answer:
      "Yes! Our solution provides APIs and plugins that can seamlessly integrate with your current security infrastructure.",
  },
  {
    question: "Is this suitable for enterprises?",
    answer:
      "Absolutely. We provide scalable solutions tailored for startups, enterprises, and Web3 projects of all sizes.",
  },
];

const FAQPage = () => {
  const [openIndex, setOpenIndex] = useState(null);

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center bg-black/60 bg-cover bg-no-repeat bg-center text-white p-8 relative"
      style={{ backgroundImage: `url(${Aibg})` }}
    >
      <div className="absolute top-0 left-0 w-full h-full bg-black/80 z-0"></div>
      <div className="max-w-5xl w-full relative z-10">
        <h1 className="text-5xl ffont-semibold shadow-lg leading-normal text-center mb-6">
          AI-Powered Audit & Reputation Security
        </h1>
        <p className="text-xl text-gray-400 text-center mb-8">
          Stay ahead of threats with our AI-driven security solution. Here are
          some common questions about our platform.
        </p>
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="border border-gray-800 rounded-lg overflow-hidden"
            >
              <button
                onClick={() => toggleFAQ(index)}
                className="w-full flex justify-between items-center p-4 bg-gray-900 text-left"
              >
                <span className="text-lg">{faq.question}</span>
                <ChevronDown
                  className={`w-5 h-5 transition-transform ${
                    openIndex === index ? "rotate-180" : ""
                  }`}
                />
              </button>
              {openIndex === index && (
                <div className="p-4 bg-gray-800 text-gray-300">
                  {faq.answer}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FAQPage;
